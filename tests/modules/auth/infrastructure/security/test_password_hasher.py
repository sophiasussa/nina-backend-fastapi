from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


def test_password_hash_is_verified_without_storing_plaintext(monkeypatch):
    monkeypatch.setattr(
        "app.modules.auth.infrastructure.security.password_hasher.settings.BCRYPT_ROUNDS",
        4,
    )
    hasher = PasswordHasher()
    plain_password = "strong-password-123"

    password_hash = hasher.hash(plain_password)

    assert password_hash != plain_password
    assert hasher.verify(plain_password, password_hash) is True
    assert hasher.verify("different-password-123", password_hash) is False
    assert hasher.needs_rehash(password_hash) is False
