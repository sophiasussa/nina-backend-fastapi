from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    """
    DTO para requisição de login.

    Valida dados de entrada usando Pydantic.
    """

    email: EmailStr = Field(
        ...,
        description="Email do usuário",
        json_schema_extra={"example": "joao@example.com"},
    )

    senha: str = Field(
        ...,
        min_length=6,
        description="Senha do usuário",
        json_schema_extra={"example": "senha123"},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "joao@example.com",
                "senha": "senha123",
            }
        }
    )
