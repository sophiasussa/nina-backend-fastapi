from dataclasses import dataclass

from app.shared.domain.value_objects.id_vo import UserId


@dataclass(frozen=True)
class UserCredentials:
    user_id: UserId
    password_hash: str
    is_active: bool
