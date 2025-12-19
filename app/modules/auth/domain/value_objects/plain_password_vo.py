from dataclasses import dataclass

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64


@dataclass(frozen=True)
class PlainPassword:
    """
    Value Object que representa uma senha em texto plano
    APENAS durante a criação ou alteração da senha.

    IMPORTANTE:
    - Nunca deve ser armazenada
    - Nunca deve ser logada
    - Existe apenas no domínio temporariamente
    """

    value: str

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
        if len(self.value) < PASSWORD_MIN_LENGTH:
            raise ValueError(
                f"Senha deve ter no mínimo {PASSWORD_MIN_LENGTH} caracteres"
            )

        if len(self.value) > PASSWORD_MAX_LENGTH:
            raise ValueError(
                f"Senha deve ter no máximo {PASSWORD_MAX_LENGTH} caracteres"
            )

        if not any(c.isalpha() for c in self.value):
            raise ValueError("Senha deve conter pelo menos uma letra")

        if not any(c.isdigit() for c in self.value):
            raise ValueError("Senha deve conter pelo menos um número")

    def __str__(self) -> str:
        return "******"

    def __repr__(self) -> str:
        return "PlainPassword(******)"
