from dataclasses import dataclass
from datetime import datetime

from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.shared.domain.value_objects.id_vo import UserId


@dataclass(frozen=True)
class RegisterResultDTO:
    """
    DTO de saída do caso de uso de registro de usuário.

    Responsabilidades:
    ------------------
    - Transportar dados do usuário recém-criado
    - Garantir consistência usando Value Objects
    - Não expor detalhes de infraestrutura

    Observação:
    -----------
    - Conversão para tipos primitivos (str) ocorre
      na camada presentation
    """

    user_id: UserId
    nome: Name
    email: Email
    is_active: bool
    created_at: datetime
