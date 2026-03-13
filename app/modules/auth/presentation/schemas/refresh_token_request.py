from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    """
    Schema de requisição para renovação de access token.
    """

    refresh_token: str = Field(
        ...,
        description="Refresh token JWT válido",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
