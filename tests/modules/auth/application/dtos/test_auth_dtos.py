from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.modules.auth.application.dtos.current_user_result_dto import (
    CurrentUserResultDTO,
)
from app.modules.auth.application.dtos.forgot_password_input_dto import (
    ForgotPasswordInputDTO,
)

from app.modules.auth.application.dtos.logininput_dto import LoginInputDTO
from app.modules.auth.application.dtos.loginresult_dto import LoginResultDTO
from app.modules.auth.application.dtos.refreshtokenrequest_dto import RefreshTokenRequestDTO
from app.modules.auth.application.dtos.refreshtokenresponse_dto import RefreshTokenResponseDTO
from app.modules.auth.application.dtos.registerinput_dto import RegisterInputDTO
from app.modules.auth.application.dtos.registerresult_dto import RegisterResultDTO
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.modules.auth.domain.value_objects.plain_password_vo import PlainPassword
from app.shared.domain.value_objects.id_vo import UserId


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def user_id() -> UserId:
    return UserId.new()


@pytest.fixture
def email() -> Email:
    return Email("usuario@email.com")


@pytest.fixture
def name() -> Name:
    return Name("João da Silva")


@pytest.fixture
def password() -> PlainPassword:
    return PlainPassword("senha123")


@pytest.fixture
def created_at() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# CurrentUserResultDTO
# ---------------------------------------------------------------------------


def test_current_user_result_dto_should_create_successfully(
    user_id: UserId,
    name: Name,
    email: Email,
    created_at: datetime,
):
    dto = CurrentUserResultDTO(
        user_id=user_id,
        nome=name,
        email=email,
        is_active=True,
        created_at=created_at,
    )

    assert dto.user_id is user_id
    assert dto.nome is name
    assert dto.email is email
    assert dto.is_active is True
    assert dto.created_at is created_at


def test_current_user_result_dto_should_be_immutable(
    user_id: UserId,
    name: Name,
    email: Email,
    created_at: datetime,
):
    dto = CurrentUserResultDTO(
        user_id=user_id,
        nome=name,
        email=email,
        is_active=True,
        created_at=created_at,
    )

    with pytest.raises(FrozenInstanceError):
        dto.is_active = False


# ---------------------------------------------------------------------------
# ForgotPasswordInputDTO
# ---------------------------------------------------------------------------


def test_forgot_password_input_dto_should_convert_email_to_value_object():
    dto = ForgotPasswordInputDTO("usuario@email.com")

    assert isinstance(dto.email, Email)
    assert dto.email.value == "usuario@email.com"


def test_forgot_password_input_dto_should_reject_invalid_email():
    with pytest.raises(ValueError):
        ForgotPasswordInputDTO("email-invalido")


# ---------------------------------------------------------------------------
# LoginInputDTO
# ---------------------------------------------------------------------------


def test_login_input_dto_should_create_successfully(
    email: Email,
    password: PlainPassword,
):
    dto = LoginInputDTO(
        email=email,
        password=password,
    )

    assert dto.email is email
    assert dto.password is password


def test_login_input_dto_should_be_immutable(
    email: Email,
    password: PlainPassword,
):
    dto = LoginInputDTO(
        email=email,
        password=password,
    )

    with pytest.raises(FrozenInstanceError):
        dto.email = Email("outro@email.com")


# ---------------------------------------------------------------------------
# LoginResultDTO
# ---------------------------------------------------------------------------


def test_login_result_dto_should_create_successfully(
    user_id: UserId,
    name: Name,
    email: Email,
):
    dto = LoginResultDTO(
        user_id=user_id,
        nome=name,
        email=email,
        is_active=True,
    )

    assert dto.user_id is user_id
    assert dto.nome is name
    assert dto.email is email
    assert dto.is_active is True


def test_login_result_dto_should_be_immutable(
    user_id: UserId,
    name: Name,
    email: Email,
):
    dto = LoginResultDTO(
        user_id=user_id,
        nome=name,
        email=email,
        is_active=True,
    )

    with pytest.raises(FrozenInstanceError):
        dto.is_active = False


# ---------------------------------------------------------------------------
# RefreshTokenRequestDTO
# ---------------------------------------------------------------------------


def test_refresh_token_request_dto_should_create_successfully():
    dto = RefreshTokenRequestDTO(
        refresh_token="refresh-token-123",
    )

    assert dto.refresh_token == "refresh-token-123"


def test_refresh_token_request_dto_should_require_refresh_token():
    with pytest.raises(ValidationError):
        RefreshTokenRequestDTO()


# ---------------------------------------------------------------------------
# RefreshTokenResponseDTO
# ---------------------------------------------------------------------------


def test_refresh_token_response_dto_should_create_successfully():
    dto = RefreshTokenResponseDTO(
        access_token="access-token-123",
        token_type="bearer",
        expires_in=3600,
    )

    assert dto.access_token == "access-token-123"
    assert dto.token_type == "bearer"
    assert dto.expires_in == 3600


def test_refresh_token_response_dto_should_require_all_fields():
    with pytest.raises(ValidationError):
        RefreshTokenResponseDTO(
            access_token="access-token-123",
        )


# ---------------------------------------------------------------------------
# RegisterInputDTO
# ---------------------------------------------------------------------------


def test_register_input_dto_should_create_successfully(
    name: Name,
    email: Email,
    password: PlainPassword,
):
    dto = RegisterInputDTO(
        nome=name,
        email=email,
        password=password,
    )

    assert dto.nome is name
    assert dto.email is email
    assert dto.password is password


def test_register_input_dto_should_be_immutable(
    name: Name,
    email: Email,
    password: PlainPassword,
):
    dto = RegisterInputDTO(
        nome=name,
        email=email,
        password=password,
    )

    with pytest.raises(FrozenInstanceError):
        dto.nome = Name("Outro Nome")


# ---------------------------------------------------------------------------
# RegisterResultDTO
# ---------------------------------------------------------------------------


def test_register_result_dto_should_create_successfully(
    user_id: UserId,
    name: Name,
    email: Email,
    created_at: datetime,
):
    dto = RegisterResultDTO(
        user_id=user_id,
        nome=name,
        email=email,
        is_active=True,
        created_at=created_at,
    )

    assert dto.user_id is user_id
    assert dto.nome is name
    assert dto.email is email
    assert dto.is_active is True
    assert dto.created_at is created_at


def test_register_result_dto_should_be_immutable(
    user_id: UserId,
    name: Name,
    email: Email,
    created_at: datetime,
):
    dto = RegisterResultDTO(
        user_id=user_id,
        nome=name,
        email=email,
        is_active=True,
        created_at=created_at,
    )

    with pytest.raises(FrozenInstanceError):
        dto.is_active = False
