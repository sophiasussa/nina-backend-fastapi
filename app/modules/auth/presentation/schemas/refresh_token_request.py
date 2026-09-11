from pydantic import BaseModel, ConfigDict, Field


class RefreshTokenRequest(BaseModel):
    """
    Schema de requisição para renovação de access token.
    """

    refresh_token: str = Field(
        ...,
        description="Refresh token JWT válido",
        json_schema_extra={
            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        },
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    )
