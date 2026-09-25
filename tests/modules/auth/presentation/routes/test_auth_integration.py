from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import replace
from time import monotonic

import pytest
from fastapi.testclient import TestClient

from app.infra.redis.dependencies import get_redis
from app.main import app
from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.read_models.user_credentials import UserCredentials
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.presentation.dependencies.auth_deps import (
    get_google_token_verifier,
    get_password_hasher,
    get_user_repository,
)
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name


class MemoryPipeline:
    def __init__(self, redis):
        self.redis = redis
        self.operations = []

    def __getattr__(self, operation):
        def enqueue(*args, **kwargs):
            self.operations.append((operation, args, kwargs))
            return self

        return enqueue

    def execute(self):
        results = []
        for operation, args, kwargs in self.operations:
            results.append(getattr(self.redis, operation)(*args, **kwargs))
        self.operations.clear()
        return results


class MemoryRedis:
    """Small deterministic Redis substitute for HTTP integration tests."""

    def __init__(self):
        self.values = {}
        self.sets = defaultdict(set)
        self.expirations = {}

    def pipeline(self):
        return MemoryPipeline(self)

    def incr(self, key):
        self.values[key] = int(self.values.get(key, 0)) + 1
        return self.values[key]

    def ttl(self, key):
        if key not in self.values:
            return -2
        expiration = self.expirations.get(key)
        if expiration is None:
            return -1
        return max(0, int(expiration - monotonic()))

    def expire(self, key, seconds):
        if key not in self.values:
            return False
        self.expirations[key] = monotonic() + seconds
        return True

    def setex(self, name, time, value):
        self.values[name] = value
        self.expirations[name] = monotonic() + time
        return True

    def exists(self, key):
        return int(key in self.values)

    def sadd(self, key, member):
        before = len(self.sets[key])
        self.sets[key].add(member)
        return len(self.sets[key]) - before

    def srem(self, key, member):
        before = len(self.sets[key])
        self.sets[key].discard(member)
        return before - len(self.sets[key])

    def smembers(self, key):
        return set(self.sets[key])

    def get(self, key):
        return self.values.get(key)

    def delete(self, *keys):
        deleted = 0
        for key in keys:
            deleted += int(key in self.values or key in self.sets)
            self.values.pop(key, None)
            self.sets.pop(key, None)
            self.expirations.pop(key, None)
        return deleted


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: dict[str, UserEntity] = {}

    async def create(self, user):
        self.users[user.email.value] = user
        return user

    async def get_by_id(self, user_id):
        return next((user for user in self.users.values() if user.id == user_id), None)

    async def get_by_email(self, email):
        return self.users.get(email.value)

    async def exists_by_email(self, email):
        return email.value in self.users

    async def update(self, user):
        self.users[user.email.value] = user
        return user

    async def delete(self, user_id):
        user = await self.get_by_id(user_id)
        if user is None:
            return None
        self.users.pop(user.email.value)

    async def get_credentials_by_email(self, email):
        user = await self.get_by_email(email)
        if user is None:
            return None
        return UserCredentials(user.id, user.password.value, user.is_active)

    async def update_password(self, user_id, password):
        user = await self.get_by_id(user_id)
        self.users[user.email.value] = replace(user, password=password)


class DeterministicHasher:
    @staticmethod
    def hash(plain_password):
        return "test$" + hashlib.sha256(plain_password.encode()).hexdigest()

    @classmethod
    def verify(cls, plain_password, password_hash):
        return cls.hash(plain_password) == password_hash


@pytest.fixture
def auth_system():
    repository = InMemoryUserRepository()
    redis = MemoryRedis()
    app.dependency_overrides[get_user_repository] = lambda: repository
    app.dependency_overrides[get_password_hasher] = DeterministicHasher
    app.dependency_overrides[get_redis] = lambda: redis

    try:
        with TestClient(app) as client:
            yield client, repository, redis
    finally:
        app.dependency_overrides.pop(get_user_repository, None)
        app.dependency_overrides.pop(get_password_hasher, None)
        app.dependency_overrides.pop(get_redis, None)


def register(client, email="ana@example.com", password="password123"):
    return client.post(
        "/api/v1/auth/register",
        json={"nome": "Ana Maria", "email": email, "senha": password},
    )


def test_register_login_and_access_protected_profile(auth_system):
    client, _, redis = auth_system

    created = register(client)
    assert created.status_code == 201
    registered = created.json()
    assert registered["user"]["email"] == "ana@example.com"
    assert registered["access_token"]
    assert registered["refresh_token"]

    profile = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {registered['access_token']}"},
    )
    assert profile.status_code == 200
    assert profile.json()["id"] == registered["user"]["id"]

    logged_in = client.post(
        "/api/v1/auth/login",
        json={"email": " ANA@example.com ", "senha": "password123"},
    )
    assert logged_in.status_code == 200
    assert logged_in.json()["user"]["email"] == "ana@example.com"
    assert len(redis.smembers(f"user_sessions:{registered['user']['id']}")) == 2


def test_register_rejects_duplicate_and_invalid_domain_password(auth_system):
    client, _, _ = auth_system
    assert register(client).status_code == 201

    duplicate = register(client)
    assert duplicate.status_code == 409

    weak_password = register(client, "another@example.com", "abc123")
    assert weak_password.status_code == 400


def test_refresh_rotates_token_and_detects_reuse(auth_system):
    client, _, redis = auth_system
    tokens = register(client).json()
    original_refresh = tokens["refresh_token"]

    rotated = client.post("/api/v1/auth/refresh", json={"refresh_token": original_refresh})
    assert rotated.status_code == 200
    next_refresh = rotated.json()["refresh_token"]
    assert next_refresh != original_refresh

    replay = client.post("/api/v1/auth/refresh", json={"refresh_token": original_refresh})
    assert replay.status_code == 401
    assert redis.smembers(f"user_sessions:{tokens['user']['id']}") == set()

    after_reuse = client.post("/api/v1/auth/refresh", json={"refresh_token": next_refresh})
    assert after_reuse.status_code == 401


def test_logout_revokes_refresh_and_blacklists_access_token(auth_system):
    client, _, _ = auth_system
    tokens = register(client).json()
    logout = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert logout.status_code == 204

    denied = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert denied.status_code == 401

    refresh = client.post(
        "/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert refresh.status_code == 401


def test_logout_all_revokes_every_session_and_rejects_refresh_token_as_access(auth_system):
    client, _, redis = auth_system
    first = register(client).json()
    second = client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "senha": "password123"},
    ).json()

    logout_all = client.post(
        "/api/v1/auth/logout-all",
        headers={"Authorization": f"Bearer {first['access_token']}"},
    )
    assert logout_all.status_code == 204
    assert redis.smembers(f"user_sessions:{first['user']['id']}") == set()

    for refresh_token in (first["refresh_token"], second["refresh_token"]):
        response = client.post(
            "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
        )
        assert response.status_code == 401

    wrong_token_type = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {second['access_token']}"},
    )
    assert wrong_token_type.status_code == 401


def test_current_user_rejects_malformed_token_and_inactive_user(auth_system):
    client, repository, _ = auth_system
    tokens = register(client).json()

    malformed = client.get(
        "/api/v1/auth/me", headers={"Authorization": "Bearer malformed.token"}
    )
    assert malformed.status_code == 401

    user = repository.users["ana@example.com"]
    repository.users[user.email.value] = user.deactivate()
    inactive = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert inactive.status_code == 403


def test_forgot_and_reset_password_then_authenticate_with_new_password(auth_system, capsys):
    client, _, _ = auth_system
    register(client)

    forgot = client.post(
        "/api/v1/auth/forgot-password", json={"email": "ana@example.com"}
    )
    assert forgot.status_code == 200
    assert forgot.json() == client.post(
        "/api/v1/auth/forgot-password", json={"email": "missing@example.com"}
    ).json()

    reset_output = capsys.readouterr().out
    reset_token = reset_output.split("token=", 1)[1].split()[0]
    reset = client.post(
        "/api/v1/auth/reset-password",
        json={"token": reset_token, "new_password": "newpassword123"},
    )
    assert reset.status_code == 200
    reused_token = client.post(
        "/api/v1/auth/reset-password",
        json={"token": reset_token, "new_password": "anotherpassword123"},
    )
    assert reused_token.status_code == 401

    old_password = client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "senha": "password123"},
    )
    assert old_password.status_code == 401

    new_password = client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "senha": "newpassword123"},
    )
    assert new_password.status_code == 200

def test_login_rate_limit_returns_429_after_five_failed_attempts(auth_system):
    client, _, _ = auth_system
    payload = {"email": "missing@example.com", "senha": "password123"}

    responses = [client.post("/api/v1/auth/login", json=payload) for _ in range(6)]

    assert [response.status_code for response in responses] == [401] * 5 + [429]


def test_google_login_route_creates_user_and_persists_refresh_session(auth_system):
    client, _, _ = auth_system

    class VerifiedGoogleToken:
        async def verify(self, token):
            assert token == "verified-by-google-provider"
            return Email("google@example.com"), Name("Google User")

    app.dependency_overrides[get_google_token_verifier] = VerifiedGoogleToken
    try:
        response = client.post(
            "/api/v1/auth/google-login",
            json={"id_token": "verified-by-google-provider"},
        )
    finally:
        app.dependency_overrides.pop(get_google_token_verifier, None)

    assert response.status_code == 200
    assert response.json()["user"]["email"] == "google@example.com"
    refresh = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": response.json()["refresh_token"]},
    )
    assert refresh.status_code == 200
    assert refresh.json()["refresh_token"]
