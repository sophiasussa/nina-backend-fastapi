import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CustomerAddress:
    """
    Value Object que representa o endereço de entrega de um cliente.
    
    Todos os campos são obrigatórios exceto complemento.
    """

    street: str        # Logradouro (ex: Rua das Flores)
    number: str        # Número (ex: 123 ou S/N)
    neighborhood: str  # Bairro
    city: str          # Cidade
    state: str         # UF (2 letras)
    zip_code: str      # CEP (8 dígitos)
    complement: Optional[str] = None  # Complemento (ex: Apto 12)

    _ZIP_REGEX = re.compile(r"^\d{8}$")
    _STATE_REGEX = re.compile(r"^[A-Z]{2}$")

    def __post_init__(self):
        self._validate_required("Logradouro", self.street)
        self._validate_required("Número", self.number)
        self._validate_required("Bairro", self.neighborhood)
        self._validate_required("Cidade", self.city)

        # Valida e normaliza UF
        state = self.state.strip().upper() if self.state else ""
        if not self._STATE_REGEX.match(state):
            raise ValueError(f"UF inválida: '{self.state}'. Use 2 letras maiúsculas (ex: SP).")
        object.__setattr__(self, "state", state)

        # Valida e normaliza CEP
        zip_digits = re.sub(r"\D", "", self.zip_code) if self.zip_code else ""
        if not self._ZIP_REGEX.match(zip_digits):
            raise ValueError(f"CEP inválido: '{self.zip_code}'. Deve conter 8 dígitos.")
        object.__setattr__(self, "zip_code", zip_digits)

    @staticmethod
    def _validate_required(field: str, value: Optional[str]) -> None:
        if not value or not value.strip():
            raise ValueError(f"{field} não pode ser vazio.")

    @property
    def zip_code_formatted(self) -> str:
        """Retorna CEP formatado: 00000-000."""
        return f"{self.zip_code[:5]}-{self.zip_code[5:]}"

    def full_address(self) -> str:
        """Retorna endereço completo como string."""
        parts = [
            f"{self.street}, {self.number}",
            self.complement or "",
            self.neighborhood,
            f"{self.city} - {self.state}",
            self.zip_code_formatted,
        ]
        return ", ".join(p for p in parts if p)
