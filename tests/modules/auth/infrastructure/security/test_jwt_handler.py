import pytest

from app.core.constants import TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException
from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler


def test_access_and_refresh_tokens_include_expected_claims():
    handler = JWTHandler()
    subject = "user-123"

    access = handler.decode_token(
        handler.create_access_token(subject), expected_type=TOKEN_TYPE_ACCESS
    )
    refresh = handler.decode_token(
        handler.create_refresh_token(subject), expected_type=TOKEN_TYPE_REFRESH
    )

    assert access["sub"] == subject
    assert access["type"] == TOKEN_TYPE_ACCESS
    assert "jti" not in access
    assert refresh["sub"] == subject
    assert refresh["type"] == TOKEN_TYPE_REFRESH
    assert refresh["jti"]


def test_decode_rejects_wrong_type_tampered_and_expired_tokens():
    handler = JWTHandler()
    access_token = handler.create_access_token("user-123")

    with pytest.raises(InvalidTokenException):
        handler.decode_token(access_token, expected_type=TOKEN_TYPE_REFRESH)

    with pytest.raises(InvalidTokenException):
        handler.decode_token(access_token + "tampered")

    handler._access_token_expire = -1
    expired = handler.create_access_token("user-123")
    with pytest.raises(InvalidTokenException):
        handler.decode_token(expired)


def test_reserved_claims_cannot_be_overridden():
    handler = JWTHandler()

    with pytest.raises(ValueError, match="Claims reservados"):
        handler.create_access_token("user-123", {"sub": "attacker"})


def test_get_user_id_and_expiration_return_validated_claims():
    handler = JWTHandler()
    token = handler.create_access_token("user-123")

    assert handler.get_user_id_from_token(token) == "user-123"
    assert handler.get_token_expiration(token).tzinfo is not None
    assert handler.is_token_expired(token) is False
