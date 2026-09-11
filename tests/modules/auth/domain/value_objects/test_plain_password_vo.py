import pytest

from app.modules.auth.domain.value_objects.plain_password_vo import (
    PlainPassword,
)


def test_should_create_valid_plain_password():
    password = PlainPassword("password123")

    assert password.value == "password123"


def test_should_reject_password_with_less_than_8_characters():
    with pytest.raises(
        ValueError,
        match="Senha deve ter no mínimo 8 caracteres",
    ):
        PlainPassword("abc123")


def test_should_reject_password_with_more_than_64_characters():
    password = "a" * 65

    with pytest.raises(
        ValueError,
        match="Senha deve ter no máximo 64 caracteres",
    ):
        PlainPassword(password)


def test_should_reject_password_without_letters():
    with pytest.raises(
        ValueError,
        match="Senha deve conter pelo menos uma letra",
    ):
        PlainPassword("12345678")


def test_should_reject_password_without_numbers():
    with pytest.raises(
        ValueError,
        match="Senha deve conter pelo menos um número",
    ):
        PlainPassword("abcdefgh")


def test_should_accept_password_with_exactly_8_characters():
    password = PlainPassword("abcde123")

    assert password.value == "abcde123"


def test_should_accept_password_with_exactly_64_characters():
    password = PlainPassword("a" * 63 + "1")

    assert len(password.value) == 64
