import pytest

from app.modules.auth.domain.value_objects.name_vo import Name


def test_should_create_valid_name():
    name = Name("Sophia")

    assert name.value == "Sophia"


def test_should_remove_spaces_from_name():
    name = Name("  Sophia  ")

    assert name.value == "Sophia"


def test_should_reject_name_with_less_than_5_characters():
    with pytest.raises(
        ValueError,
        match="Nome deve possuir entre 5 e 20 caracteres",
    ):
        Name("Ana")


def test_should_reject_name_with_more_than_20_characters():
    with pytest.raises(
        ValueError,
        match="Nome deve possuir entre 5 e 20 caracteres",
    ):
        Name("A" * 21)


def test_should_accept_name_with_exactly_5_characters():
    name = Name("Maria")

    assert name.value == "Maria"


def test_should_accept_name_with_exactly_20_characters():
    name = Name("A" * 20)

    assert name.value == "A" * 20


def test_should_return_name_as_string():
    name = Name("Sophia")

    assert str(name) == "Sophia"
