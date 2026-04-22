from dataclasses import dataclass
from datetime import datetime

from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.shared.domain.value_objects.id_vo import UserId


@dataclass(frozen=True)
class CurrentUserResultDTO:
    user_id: UserId
    nome: Name
    email: Email
    is_active: bool
    created_at: datetime
