import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CustomerPhone:
    """
    Value Object que representa o telefone de um cliente (formato brasileiro).
    
    Aceita formatos: (11) 99999-9999, 11999999999, +5511999999999.
    Armazena apenas os dígitos.
    """

    value: str

    # Aceita 10 (fixo) ou 11 (celular) dígitos
    _DIGITS_REGEX = re.compile(r"^\d{10,11}$")

    def __post_init__(self):
        if not self.value:
            raise ValueError("Telefone do cliente não pode ser vazio.")

        # Remove tudo que não for dígito
        digits_only = re.sub(r"\D", "", self.value)

        # Remove DDI do Brasil (+55) se presente
        if digits_only.startswith("55") and len(digits_only) in (12, 13):
            digits_only = digits_only[2:]

        if not self._DIGITS_REGEX.match(digits_only):
            raise ValueError(
                f"Telefone inválido: '{self.value}'. "
                "Informe DDD + número (10 ou 11 dígitos)."
            )

        object.__setattr__(self, "value", digits_only)

    @property
    def formatted(self) -> str:
        """Retorna o telefone formatado: (11) 99999-9999 ou (11) 9999-9999."""
        v = self.value
        if len(v) == 11:
            return f"({v[:2]}) {v[2:7]}-{v[7:]}"
        return f"({v[:2]}) {v[2:6]}-{v[6:]}"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def create_optional(cls, value: Optional[str]) -> Optional["CustomerPhone"]:
        """Cria um CustomerPhone ou retorna None se valor for None/vazio."""
        if not value or not value.strip():
            return None
        return cls(value=value)
