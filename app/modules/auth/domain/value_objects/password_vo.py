from dataclasses import dataclass


@dataclass(frozen=True)
class Password:
    """
    Value Object que representa uma senha segura já criptografada (hash).

    Características:
    - Imutável
    - Nunca armazena senha em texto plano
    - Contém apenas o hash final gerado pela infraestrutura
    """

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Hash de senha é obrigatório")

        if len(self.value) < 30:
            raise ValueError("Hash de senha inválido")

    def __str__(self) -> str:
        return "******"

    def __repr__(self) -> str:
        return "Password(******)"
