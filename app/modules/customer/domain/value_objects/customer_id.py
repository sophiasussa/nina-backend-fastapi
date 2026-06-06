import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerId:
    """
    Value Object que representa o identificador único de um cliente.
    
    Imutável e com validação na criação.
    """

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("ID do cliente não pode ser vazio.")
        try:
            uuid.UUID(str(self.value))
        except ValueError:
            raise ValueError(f"ID inválido: '{self.value}'. Deve ser um UUID válido.")

    @classmethod
    def generate(cls) -> "CustomerId":
        """Gera um novo CustomerId com UUID v4."""
        return cls(value=str(uuid.uuid4()))

    def __str__(self) -> str:
        return self.value
