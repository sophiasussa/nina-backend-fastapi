from pydantic import BaseModel, ConfigDict, Field


class RefreshTokenResponse(BaseModel):
    """
    Schema de resposta para renovação de access token.
    """

    access_token: str = Field(
        ...,
        description="Novo access token JWT"
    )

    refresh_token: str = Field(
        ...,
        description="Novo refresh token JWT"
    )

    token_type: str = Field(
        default="Bearer",
        description="Tipo do token"
    )

    expires_in: int = Field(
        ...,
        description="Tempo de expiração do token em segundos",
        json_schema_extra={"example": 3600},
    )

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_in": 3600
            }
        }
    )
