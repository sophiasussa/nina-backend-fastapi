from dataclasses import dataclass

from app.shared.domain.value_objects.id_vo import Id


@dataclass(frozen=True)
class UserCredentials:
    user_id: Id
    password_hash: str
    is_active: bool
