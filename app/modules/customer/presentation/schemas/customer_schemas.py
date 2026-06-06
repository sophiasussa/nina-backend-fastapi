from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ─── Schemas de endereço ──────────────────────────────────────────────────────


class AddressSchema(BaseModel):
    """Endereço para criação ou atualização."""

    street: str = Field(..., min_length=2, max_length=150, examples=["Rua das Flores"])
    number: str = Field(..., min_length=1, max_length=20, examples=["123"])
    complement: Optional[str] = Field(None, max_length=100, examples=["Apto 12"])
    neighborhood: str = Field(..., min_length=2, max_length=100, examples=["Centro"])
    city: str = Field(..., min_length=2, max_length=100, examples=["São Paulo"])
    state: str = Field(..., min_length=2, max_length=2, examples=["SP"])
    zip_code: str = Field(..., examples=["01310100"], description="CEP (só dígitos ou formatado)")


class AddressResponseSchema(BaseModel):
    """Endereço na resposta."""

    model_config = ConfigDict(from_attributes=True)

    street: str
    number: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str
    zip_code: str


# ─── Schemas de request ───────────────────────────────────────────────────────


class CreateCustomerSchema(BaseModel):
    """Body para POST /customers."""

    name: str = Field(..., min_length=2, max_length=100, examples=["Maria Silva"])
    email: EmailStr = Field(..., examples=["maria@email.com"])
    phone: Optional[str] = Field(
        None, examples=["11999999999"], description="Telefone com DDD (10 ou 11 dígitos)"
    )
    document: Optional[str] = Field(
        None, examples=["12345678909"], description="CPF (somente dígitos ou formatado)"
    )
    address: Optional[AddressSchema] = None
    notes: Optional[str] = Field(
        None, max_length=1000, examples=["Alergia a amendoim"]
    )


class UpdateCustomerSchema(BaseModel):
    """Body para PATCH /customers/{id} — todos os campos são opcionais."""

    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(None, min_length=2, max_length=100, examples=["Maria Souza"])
    phone: Optional[str] = Field(None, examples=["11988887777"])
    notes: Optional[str] = Field(None, max_length=1000, examples=["Sem glúten"])


class UpdateAddressSchema(BaseModel):
    """Body para PATCH /customers/{id}/address — null remove o endereço."""

    model_config = ConfigDict(extra="forbid")

    address: Optional[AddressSchema] = Field(
        None, description="Novo endereço ou null para remover o existente"
    )


# ─── Schemas de response ──────────────────────────────────────────────────────


class CustomerResponseSchema(BaseModel):
    """Resposta completa de um cliente (criação, atualização, detalhes)."""

    model_config = ConfigDict(from_attributes=True)

    customer_id: str
    name: str
    email: str
    phone: Optional[str]
    document: Optional[str]
    address: Optional[AddressResponseSchema]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CustomerSummarySchema(BaseModel):
    """Item de listagem — sem endereço, notas nem documento."""

    model_config = ConfigDict(from_attributes=True)

    customer_id: str
    name: str
    email: str
    phone: Optional[str]
    is_active: bool
    created_at: datetime


class CustomerListSchema(BaseModel):
    """Resposta paginada da listagem de clientes."""

    items: list[CustomerSummarySchema]
    total: int
    limit: int
    offset: int
