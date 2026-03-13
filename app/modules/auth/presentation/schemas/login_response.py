from pydantic import BaseModel, Field

from app.modules.auth.presentation.schemas.current_user_response_schema import CurrentUserResponse


class LoginResponse(BaseModel):
    """
    DTO para resposta de login.
    
    Retorna dados do usuário e tokens de autenticação.
    """
    
    user: CurrentUserResponse
    access_token: str = Field(..., description="Token de acesso JWT")
    refresh_token: str = Field(..., description="Token de refresh")
    token_type: str = Field(default="Bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
    
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
                "expires_in": 1800
            }
        }
