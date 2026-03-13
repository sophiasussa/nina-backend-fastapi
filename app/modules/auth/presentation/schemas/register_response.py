from pydantic import BaseModel, Field
from .current_user_response_schema import CurrentUserResponse

class RegisterResponse(BaseModel):
    """
    DTO para resposta de registro.
    
    Retorna dados do usuário criado e tokens de autenticação.
    """
    
    user: CurrentUserResponse
    access_token: str = Field(..., description="Token de acesso JWT")
    refresh_token: str = Field(..., description="Token de refresh")
    token_type: str = Field(default="Bearer", description="Tipo do token")
    message: str = Field(default="Usuário criado com sucesso", description="Mensagem de sucesso")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "nome": "João Silva",
                    "email": "joao@example.com",
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00Z"
                },
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "message": "Usuário criado com sucesso"
            }
        }
