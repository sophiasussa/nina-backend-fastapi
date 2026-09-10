import pytest

from app.modules.auth.domain.value_objects.password_vo import Password


def test_should_create_valid_password_hash():
    password = Password("a" * 60)

    assert password.value == "a" * 60


def test_should_reject_empty_password_hash():
    with pytest.raises(
        ValueError,
        match="Hash de senha é obrigatório",
    ):
        Password("")


def test_should_reject_short_password_hash():
    with pytest.raises(
        ValueError,
        match="Hash de senha inválido",
    ):
        Password("a" * 29)


def test_should_accept_password_hash_with_30_characters():
    password = Password("a" * 30)

    assert password.value == "a" * 30


def test_should_hide_password_when_converted_to_string():
    password = Password("a" * 60)

    assert str(password) == "******"


def test_should_hide_password_in_repr():
    password = Password("a" * 60)

    assert repr(password) == "Password(******)"
