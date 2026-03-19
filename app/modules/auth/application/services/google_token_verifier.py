from abc import ABC, abstractmethod
from typing import Tuple

from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name


class GoogleTokenVerifier(ABC):

    @abstractmethod
    async def verify(self, token: str) -> tuple[Email, Name]:
        """
        Valida o token do Google e retorna dados confiáveis do usuário
        """
        pass
