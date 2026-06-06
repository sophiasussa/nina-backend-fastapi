import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerEmail:
    """
    Value Object que representa o e-mail de um cliente.
    
    Valida o formato do e-mail e normaliza para minúsculas.
    """

    value: str

    _EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def __post_init__(self):
        normalized = self.value.strip().lower() if self.value else ""
        if not normalized:
            raise ValueError("E-mail do cliente não pode ser vazio.")
        if not self._EMAIL_REGEX.match(normalized):
            raise ValueError(f"E-mail inválido: '{normalized}'.")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
