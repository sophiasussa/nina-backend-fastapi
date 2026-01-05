from dataclasses import dataclass

from domain.value_objects.email_vo import Email
from domain.value_objects.plain_password_vo import PlainPassword


@dataclass(frozen=True)
class LoginInputDTO:
    """
    DTO de entrada do caso de uso de login.

    Responsabilidades:
    ------------------
    - Transportar dados já validados da camada presentation
    - Utilizar Value Objects do domínio
    - Não conter lógica de negócio

    Observações:
    ------------
    - Este DTO é usado APENAS na camada application
    - A conversão de tipos primitivos (str) para VOs
      ocorre na camada presentation
    """

    email: Email
    password: PlainPassword
