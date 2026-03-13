from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """
    DTO para requisição de login.
    
    Valida dados de entrada usando Pydantic.
    """
    
    email: EmailStr = Field(
        ...,
        description="Email do usuário",
        example="joao@example.com"
    )
    senha: str = Field(
        ...,
        min_length=6,
        description="Senha do usuário",
        example="senha123"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "joao@example.com",
                "senha": "senha123"
            }
        }
