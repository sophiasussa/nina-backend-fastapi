from dataclasses import dataclass
from datetime import datetime

from domain.value_objects.user_id_vo import UserId
from domain.value_objects.name_vo import Name
from domain.value_objects.email_vo import Email


@dataclass(frozen=True)
class CurrentUserResultDTO:
    user_id: UserId
    nome: Name
    email: Email
    is_active: bool
    created_at: datetime
