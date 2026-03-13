from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    """
    DTO para requisição de registro.
    
    Valida dados de entrada para criação de novo usuário.
    """
    
    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nome completo do usuário",
        example="João Silva"
    )
    email: EmailStr = Field(
        ...,
        description="Email do usuário",
        example="joao@example.com"
    )
    senha: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Senha do usuário",
        example="senha123"
    )
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v: str) -> str:
        """Valida e normaliza o nome."""
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Nome deve ter no mínimo 2 caracteres")
        return v
    
    @field_validator('senha')
    @classmethod
    def validate_senha(cls, v: str) -> str:
        """Valida força da senha."""
        if not any(c.isalpha() for c in v):
            raise ValueError("Senha deve conter pelo menos uma letra")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João Silva",
                "email": "joao@example.com",
                "senha": "senha123"
            }
        }
