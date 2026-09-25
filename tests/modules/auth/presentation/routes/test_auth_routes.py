from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.modules.auth.domain.value_objects.password_vo import Password
from app.modules.auth.presentation.dependencies.auth_deps import get_current_user
from app.shared.domain.value_objects.id_vo import UserId


def test_current_user_endpoint_requires_bearer_token():
    with TestClient(app) as client:
        response = client.get("/api/v1/auth/me")

    assert response.status_code == 403


def test_current_user_endpoint_returns_authenticated_user():
    user = UserEntity(
        id=UserId.new(),
        nome=Name("Ana Maria"),
        email=Email("ana@example.com"),
        password=Password("x" * 60),
        created_at=datetime.now(timezone.utc),
    )

    async def authenticated_user():
        return user

    app.dependency_overrides[get_current_user] = authenticated_user
    try:
        with TestClient(app) as client:
            response = client.get(
                "/api/v1/auth/me",
                headers={"Authorization": "Bearer test-access-token"},
            )
    finally:
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json()["email"] == "ana@example.com"
    assert response.json()["nome"] == "Ana Maria"
