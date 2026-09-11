from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="E-mail do usuário para recuperação de senha",
        json_schema_extra={"example": "usuario@email.com"},
    )
