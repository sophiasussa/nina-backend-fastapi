import asyncio

import pytest

from app.modules.auth.application.dtos.logininput_dto import LoginInputDTO
from app.modules.auth.application.dtos.registerinput_dto import RegisterInputDTO
from app.modules.auth.application.usecases.login_usecase import LoginUseCase
from app.modules.auth.application.usecases.getcurrentuser_usecase import GetCurrentUserUseCase
from app.modules.auth.application.usecases.register_usecase import RegisterUseCase
from app.modules.auth.application.usecases.reset_password_usecase import ResetPasswordUseCase
from app.modules.auth.domain.exceptions.auth_exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.modules.auth.domain.read_models.user_credentials import UserCredentials
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.modules.auth.domain.value_objects.plain_password_vo import PlainPassword
from app.shared.domain.value_objects.id_vo import UserId


class InMemoryUserRepository:
    def __init__(self):
        self.users = {}

    async def create(self, user):
        self.users[user.email.value] = user
        return user

    async def exists_by_email(self, email):
        return email.value in self.users

    async def get_by_email(self, email):
        return self.users.get(email.value)

    async def get_by_id(self, user_id):
        return next((user for user in self.users.values() if user.id == user_id), None)

    async def get_credentials_by_email(self, email):
        user = await self.get_by_email(email)
        if user is None:
            return None
        return UserCredentials(
            user_id=user.id,
            password_hash=user.password.value,
            is_active=user.is_active,
        )


class DeterministicPasswordHasher:
    def hash(self, plain_password):
        return "hashed:" + plain_password + ("x" * 40)

    def verify(self, plain_password, password_hash):
        return self.hash(plain_password) == password_hash


def run(coroutine):
    return asyncio.run(coroutine)


def registration_input(email="ana@example.com"):
    return RegisterInputDTO(
        nome=Name("Ana Maria"),
        email=Email(email),
        password=PlainPassword("password123"),
    )


def test_register_persists_user_with_hashed_password():
    repository = InMemoryUserRepository()
    result = run(RegisterUseCase(repository, DeterministicPasswordHasher()).execute(registration_input()))

    assert result.email.value == "ana@example.com"
    assert result.password.value != "password123"
    assert run(repository.exists_by_email(Email("ana@example.com")))


def test_register_rejects_an_existing_email():
    repository = InMemoryUserRepository()
    use_case = RegisterUseCase(repository, DeterministicPasswordHasher())
    run(use_case.execute(registration_input()))

    with pytest.raises(UserAlreadyExistsException):
        run(use_case.execute(registration_input()))


def test_login_returns_user_for_valid_credentials():
    repository = InMemoryUserRepository()
    hasher = DeterministicPasswordHasher()
    run(RegisterUseCase(repository, hasher).execute(registration_input()))
    login = LoginInputDTO(Email("ANA@example.com"), PlainPassword("password123"))

    result = run(LoginUseCase(repository, hasher).execute(login))

    assert result.email.value == "ana@example.com"
    assert result.nome.value == "Ana Maria"


def test_login_rejects_unknown_user_and_wrong_password():
    repository = InMemoryUserRepository()
    hasher = DeterministicPasswordHasher()
    use_case = LoginUseCase(repository, hasher)

    with pytest.raises(UserNotFoundException):
        run(use_case.execute(LoginInputDTO(Email("missing@example.com"), PlainPassword("password123"))))

    run(RegisterUseCase(repository, hasher).execute(registration_input()))
    with pytest.raises(InvalidCredentialsException):
        run(use_case.execute(LoginInputDTO(Email("ana@example.com"), PlainPassword("wrongpass1"))))


def test_login_rejects_inactive_user():
    repository = InMemoryUserRepository()
    hasher = DeterministicPasswordHasher()
    run(RegisterUseCase(repository, hasher).execute(registration_input()))
    user = repository.users["ana@example.com"]
    repository.users[user.email.value] = user.deactivate()

    with pytest.raises(InactiveUserException):
        run(LoginUseCase(repository, hasher).execute(
            LoginInputDTO(Email("ana@example.com"), PlainPassword("password123"))
        ))


def test_reset_password_rejects_missing_or_expired_token():
    class EmptyRedis:
        @staticmethod
        def get(key):
            return None

    use_case = ResetPasswordUseCase(
        user_repository=InMemoryUserRepository(),
        redis=EmptyRedis(),
        password_hasher=DeterministicPasswordHasher(),
    )

    with pytest.raises(InvalidTokenException):
        run(use_case.execute("expired-token", PlainPassword("newpass123")))


def test_reset_password_rejects_token_for_deleted_user():
    class RedisWithStaleResetToken:
        @staticmethod
        def get(key):
            return str(UserId.new().value)

    use_case = ResetPasswordUseCase(
        user_repository=InMemoryUserRepository(),
        redis=RedisWithStaleResetToken(),
        password_hasher=DeterministicPasswordHasher(),
    )

    with pytest.raises(InvalidTokenException):
        run(use_case.execute("stale-token", PlainPassword("newpass123")))


def test_get_current_user_returns_user_and_rejects_missing_user_or_invalid_id():
    repository = InMemoryUserRepository()
    user = run(RegisterUseCase(repository, DeterministicPasswordHasher()).execute(registration_input()))
    use_case = GetCurrentUserUseCase(repository)

    assert run(use_case.execute(str(user.id.value))).id == user.id

    with pytest.raises(UserNotFoundException):
        run(use_case.execute(str(UserId.new().value)))
    with pytest.raises(ValueError):
        run(use_case.execute("not-a-uuid"))
