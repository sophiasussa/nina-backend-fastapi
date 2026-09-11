from datetime import datetime, timezone
import pytest

from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.modules.auth.domain.value_objects.password_vo import Password
from app.shared.domain.value_objects.id_vo import UserId


def make_user() -> UserEntity:
    return UserEntity(
        id=UserId.new(),
        nome=Name("Sophia"),
        email=Email("sophia@example.com"),
        password=Password("a" * 60),
    )


def test_should_create_user():
    user = make_user()

    assert user.is_active is True
    assert user.nome.value == "Sophia"
    assert user.email.value == "sophia@example.com"
    assert user.can_login() is True

def test_should_deactivate_user():
    user = make_user()

    deactivated_user = user.deactivate()

    assert deactivated_user.is_active is False
    assert deactivated_user.can_login() is False

def test_should_return_same_user_when_deactivating_already_inactive_user():
    user = make_user()

    deactivated_user = user.deactivate()
    deactivated_again = deactivated_user.deactivate()

    assert deactivated_again is deactivated_user

def test_should_activate_user():
    user = make_user()

    deactivated_user = user.deactivate()
    activated_user = deactivated_user.activate()

    assert activated_user.is_active is True
    assert activated_user.can_login() is True


def test_should_not_change_name_when_user_is_inactive():
    user = make_user()

    user = user.deactivate()

    new_name = Name("Maria")

    with pytest.raises(
        ValueError,
        match="Usuário desativado não pode executar esta ação",
    ):
        user.change_name(new_name)

def test_should_change_name_when_user_is_active():
    user = make_user()

    new_name = Name("Maria")

    updated_user = user.change_name(new_name)

    assert updated_user.nome.value == "Maria"

def test_should_not_change_password_when_user_is_inactive():
    user = make_user()

    user = user.deactivate()

    with pytest.raises(
        ValueError,
        match="Usuário desativado não pode executar esta ação",
    ):
        user.change_password(Password("a" * 60))


def test_should_not_mutate_original_user():
    user = make_user()

    new_name = Name("Maria")

    updated_user = user.change_name(new_name)

    assert user.nome.value == "Sophia"
    assert updated_user.nome.value == "Maria"
    assert user is not updated_user

def test_should_set_created_at_when_user_is_created():
    before = datetime.now(timezone.utc)

    user = make_user()

    after = datetime.now(timezone.utc)

    assert before <= user.created_at <= after

def test_should_set_updated_at_when_user_is_deactivated():
    user = make_user()

    updated_user = user.deactivate()

    assert updated_user.updated_at is not None
