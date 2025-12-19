from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UserId:
    """
    Value Object que representa o identificador único de um usuário.

    No contexto de DDD, o `UserId`:
    ------------------------------
    - Identifica de forma única uma entidade `User`
    - Garante que o ID sempre esteja em um formato válido
    - Evita o uso de `str` solto espalhado pelo domínio
    - Facilita refactors (ex: mudar UUID para outro formato futuramente)

    Características:
    ----------------
    - Imutável (frozen=True)
    - Comparável por valor (Value Object)
    - Valida o formato UUID no momento da criação
    """

    value: str

    def __post_init__(self):
        """
        Executado automaticamente após a criação do Value Object.

        Responsabilidades:
        - Validar se o valor informado é um UUID válido
        """
        try:
            UUID(self.value)
        except ValueError:
            raise ValueError(f"UserId inválido: {self.value}")

    def __str__(self) -> str:
        """
        Retorna o identificador como string.
        """
        return self.value
