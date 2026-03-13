from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CurrentUserResponse(BaseModel):
    id: str
    nome: str
    email: str
    is_active: bool
    created_at: Optional[datetime] = None

    @classmethod
    def from_domain(cls, user):
        return cls(
            id=str(user.id.value),
            nome=user.nome.value,
            email=user.email.value,
            is_active=user.is_active,
            created_at=user.created_at,
        )
