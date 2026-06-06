from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerName:
    """
    Value Object que representa o nome completo de um cliente.
    
    Garante que o nome não está vazio e respeita tamanho mínimo/máximo.
    """

    value: str

    MIN_LENGTH = 2
    MAX_LENGTH = 100

    def __post_init__(self):
        stripped = self.value.strip() if self.value else ""
        if not stripped:
            raise ValueError("Nome do cliente não pode ser vazio.")
        if len(stripped) < self.MIN_LENGTH:
            raise ValueError(
                f"Nome muito curto. Mínimo de {self.MIN_LENGTH} caracteres."
            )
        if len(stripped) > self.MAX_LENGTH:
            raise ValueError(
                f"Nome muito longo. Máximo de {self.MAX_LENGTH} caracteres."
            )
        # Normaliza o valor com strip
        object.__setattr__(self, "value", stripped)

    def __str__(self) -> str:
        return self.value
