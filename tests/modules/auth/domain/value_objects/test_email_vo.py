import pytest

from app.modules.auth.domain.value_objects.email_vo import Email


def test_should_create_valid_email():
    email = Email("sophia@example.com")

    assert email.value == "sophia@example.com"


def test_should_normalize_email_to_lowercase():
    email = Email("Sophia@EXAMPLE.COM")

    assert email.value == "sophia@example.com"


def test_should_remove_spaces_from_email():
    email = Email("  sophia@example.com  ")

    assert email.value == "sophia@example.com"


def test_should_reject_invalid_email():
    with pytest.raises(ValueError, match="Email inválido"):
        Email("invalid-email")


def test_should_return_email_domain():
    email = Email("sophia@example.com")

    assert email.domain == "example.com"


def test_should_return_email_local_part():
    email = Email("sophia@example.com")

    assert email.local_part == "sophia"


def test_should_return_email_as_string():
    email = Email("sophia@example.com")

    assert str(email) == "sophia@example.com"
