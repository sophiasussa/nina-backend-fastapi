import asyncio

import pytest

from app.modules.auth.application.usecases.google_login_usecase import GoogleLoginUseCase
from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.exceptions.auth_exceptions import InactiveUserException
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.modules.auth.domain.value_objects.password_vo import Password
from app.shared.domain.value_objects.id_vo import UserId


class GoogleUserRepository:
    def __init__(self, existing_user=None):
        self.user = existing_user
        self.created = []

    async def get_by_email(self, email):
        return self.user if self.user and self.user.email == email else None

    async def create(self, user):
        self.created.append(user)
        self.user = user
        return user


class VerifiedGoogleToken:
    async def verify(self, token):
        assert token == "valid-google-token"
        return Email("google@example.com"), Name("Google User")


class RecordingJwtService:
    def create_access_token(self, subject):
        return f"access:{subject}"

    def create_refresh_token(self, subject):
        return f"refresh:{subject}"


class RecordingPasswordHasher:
    def hash(self, plain_password):
        self.received_password = plain_password
        return "hashed-google-password-" + "x" * 40


def make_use_case(repository):
    return GoogleLoginUseCase(
        repository,
        VerifiedGoogleToken(),
        RecordingJwtService(),
        RecordingPasswordHasher(),
    )


def test_google_login_creates_user_and_returns_application_tokens():
    repository = GoogleUserRepository()
    response = asyncio.run(make_use_case(repository).execute("valid-google-token"))

    assert len(repository.created) == 1
    assert response.user.email == "google@example.com"
    assert response.access_token == f"access:{repository.user.id.value}"
    assert response.refresh_token == f"refresh:{repository.user.id.value}"
    assert repository.user.password.value.startswith("hashed-google-password-")


def test_google_login_reuses_existing_user_without_creating_another():
    existing = UserEntity(
        id=UserId.new(),
        nome=Name("Google User"),
        email=Email("google@example.com"),
        password=Password("stored-password-hash-" + "x" * 40),
    )
    repository = GoogleUserRepository(existing)

    response = asyncio.run(make_use_case(repository).execute("valid-google-token"))

    assert repository.created == []
    assert response.user.id == str(existing.id.value)


def test_google_login_rejects_inactive_existing_account():
    existing = UserEntity(
        id=UserId.new(),
        nome=Name("Google User"),
        email=Email("google@example.com"),
        password=Password("stored-password-hash-" + "x" * 40),
    ).deactivate()

    with pytest.raises(InactiveUserException):
        asyncio.run(make_use_case(GoogleUserRepository(existing)).execute("valid-google-token"))
