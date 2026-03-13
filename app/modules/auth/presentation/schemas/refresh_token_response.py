from pydantic import BaseModel, Field


class RefreshTokenResponse(BaseModel):
    """
    Schema de resposta para renovação de access token.
    """

    access_token: str = Field(
        ...,
        description="Novo access token JWT"
    )

    token_type: str = Field(
        default="Bearer",
        description="Tipo do token"
    )

    expires_in: int = Field(
        ...,
        description="Tempo de expiração do token em segundos",
        example=3600
    )

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_in": 3600
            }
        }
