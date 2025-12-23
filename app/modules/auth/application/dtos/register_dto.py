from dataclasses import dataclass

from domain.value_objects.email_vo import Email
from domain.value_objects.name_vo import Name
from domain.value_objects.plain_password_vo import PlainPassword


@dataclass(frozen=True)
class RegisterInputDTO:
    """
    DTO de entrada para o caso de uso de registro de usuário.

    Contém dados já representados como Value Objects,
    garantindo consistência antes de chegar ao domínio.
    """
    nome: Name
    email: Email
    password: PlainPassword
