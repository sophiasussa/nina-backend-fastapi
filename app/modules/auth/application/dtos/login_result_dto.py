from dataclasses import dataclass

from domain.value_objects.user_id_vo import UserId
from domain.value_objects.email_vo import Email
from domain.value_objects.name_vo import Name


@dataclass(frozen=True)
class LoginResultDTO:
    """
    DTO de saída do caso de uso de login.

    Responsabilidades:
    ------------------
    - Representar o resultado bem-sucedido do login
    - Transportar dados do domínio para a camada presentation
    - Não expor informações sensíveis (hash de senha, etc)

    Observações:
    ------------
    - Tokens ainda não são HTTP (cookies, headers)
    - Isso é responsabilidade da camada presentation
    """

    user_id: UserId
    nome: Name
    email: Email
    is_active: bool
