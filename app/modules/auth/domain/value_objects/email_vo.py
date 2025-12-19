import re
from dataclasses import dataclass

from app.core.constants import EMAIL_REGEX


@dataclass(frozen=True)
class Email:
    """
    Value Object que representa um email válido.
    
    Características:
    - Imutável (frozen=True)
    - Valida formato no __post_init__
    - Garante que email sempre esteja em lowercase
    """
    
    value: str
    
    def __post_init__(self):
        """Valida e normaliza o email."""
        # Normaliza para lowercase
        object.__setattr__(self, 'value', self.value.lower().strip())
        
        # Valida formato
        if not re.match(EMAIL_REGEX, self.value):
            raise ValueError(f"Email inválido: {self.value}")
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def domain(self) -> str:
        """Retorna o domínio do email."""
        return self.value.split('@')[1]
    
    @property
    def local_part(self) -> str:
        """Retorna a parte local do email (antes do @)."""
        return self.value.split('@')[0]
