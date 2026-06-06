import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CustomerDocument:
    """
    Value Object que representa o CPF de um cliente.
    
    Valida o dígito verificador do CPF e armazena apenas os dígitos.
    """

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("CPF não pode ser vazio.")

        digits = re.sub(r"\D", "", self.value)

        if len(digits) != 11:
            raise ValueError(f"CPF inválido: '{self.value}'. Deve conter 11 dígitos.")

        if not self._validate_cpf(digits):
            raise ValueError(f"CPF inválido: '{self.value}'. Dígito verificador incorreto.")

        object.__setattr__(self, "value", digits)

    @staticmethod
    def _validate_cpf(cpf: str) -> bool:
        # Rejeita sequências repetidas (ex: 111.111.111-11)
        if len(set(cpf)) == 1:
            return False

        # Primeiro dígito verificador
        total = sum(int(cpf[i]) * (10 - i) for i in range(9))
        remainder = (total * 10) % 11
        if remainder == 10:
            remainder = 0
        if remainder != int(cpf[9]):
            return False

        # Segundo dígito verificador
        total = sum(int(cpf[i]) * (11 - i) for i in range(10))
        remainder = (total * 10) % 11
        if remainder == 10:
            remainder = 0
        return remainder == int(cpf[10])

    @property
    def formatted(self) -> str:
        """Retorna CPF formatado: 000.000.000-00."""
        v = self.value
        return f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def create_optional(cls, value: Optional[str]) -> Optional["CustomerDocument"]:
        """Cria um CustomerDocument ou retorna None se valor for None/vazio."""
        if not value or not value.strip():
            return None
        return cls(value=value)
