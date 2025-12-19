from dataclasses import dataclass

@dataclass(frozen=True)
class Name:
    """
    Value Object que representa o nome do usuário.

    Regras de negócio:
    - Deve possuir entre 5 e 20 caracteres
    - Não pode conter apenas espaços
    """

    value: str

    def __post_init__(self):
        """
        Executado automaticamente após a criação do Value Object.

        Responsabilidades:
        - Normalizar o nome (remover espaços extras)
        - Garantir que o nome já nasça válido
        """
        normalized = self.value.strip()

        if len(normalized) < 5 or len(normalized) > 20:
            raise ValueError("Nome deve possuir entre 5 e 20 caracteres")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
