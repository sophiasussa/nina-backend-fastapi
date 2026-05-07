from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class UserId:
    value: UUID

    def __post_init__(self):
        if isinstance(self.value, UUID):
            return

        try:
            object.__setattr__(self, "value", UUID(str(self.value)))
        except ValueError:
            raise ValueError("Id inválido")

    @staticmethod
    def new() -> "UserId":
        return UserId(uuid4())

    def __str__(self) -> str:
        return str(self.value)
