from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ─── Input DTOs (requests) ────────────────────────────────────────────────────


class AddressInputDTO(BaseModel):
    """Dados de endereço para criação ou atualização."""

    street: str = Field(..., min_length=2, max_length=150, description="Logradouro")
    number: str = Field(..., min_length=1, max_length=20, description="Número")
    complement: Optional[str] = Field(None, max_length=100, description="Complemento")
    neighborhood: str = Field(..., min_length=2, max_length=100, description="Bairro")
    city: str = Field(..., min_length=2, max_length=100, description="Cidade")
    state: str = Field(..., min_length=2, max_length=2, description="UF (ex: SP)")
    zip_code: str = Field(..., description="CEP (somente dígitos ou formatado)")


class CreateCustomerInputDTO(BaseModel):
    """
    Dados necessários para criar um novo cliente.

    Validações básicas de formato ficam aqui (Pydantic).
    Regras de negócio (unicidade de e-mail, CPF válido) ficam no use case.
    """

    name: str = Field(..., min_length=2, max_length=100, description="Nome completo")
    email: EmailStr = Field(..., description="E-mail do cliente")
    phone: Optional[str] = Field(None, description="Telefone com DDD (ex: 11999999999)")
    document: Optional[str] = Field(None, description="CPF (somente dígitos ou formatado)")
    address: Optional[AddressInputDTO] = Field(None, description="Endereço principal")
    notes: Optional[str] = Field(None, max_length=1000, description="Observações internas")


class UpdateCustomerInputDTO(BaseModel):
    """
    Dados para atualizar contato e observações de um cliente.

    Apenas os campos enviados são atualizados (PATCH semântico).
    Campos ausentes (None) são ignorados pelo use case.
    """

    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, description="Telefone com DDD")
    notes: Optional[str] = Field(None, max_length=1000)


class UpdateAddressInputDTO(BaseModel):
    """
    Dados para substituir o endereço principal de um cliente.

    Enviar None em address remove o endereço existente.
    """

    model_config = ConfigDict(extra="forbid")

    address: Optional[AddressInputDTO] = Field(
        None, description="Novo endereço ou null para remover"
    )


class ListCustomersInputDTO(BaseModel):
    """Parâmetros de filtro e paginação para listagem de clientes."""

    model_config = ConfigDict(extra="forbid")

    search: Optional[str] = Field(None, max_length=100, description="Busca por nome ou e-mail")
    is_active: Optional[bool] = Field(None, description="Filtrar por status")
    limit: int = Field(50, ge=1, le=200, description="Registros por página")
    offset: int = Field(0, ge=0, description="Deslocamento para paginação")


# ─── Output DTOs (responses) ──────────────────────────────────────────────────


class AddressOutputDTO(BaseModel):
    """Endereço do cliente na resposta."""

    model_config = ConfigDict(from_attributes=True)

    street: str
    number: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str
    zip_code: str


class CustomerOutputDTO(BaseModel):
    """
    Resposta completa após criar ou atualizar um cliente.

    Espelha CustomerProfile (read model), mas em formato Pydantic
    para serialização HTTP.
    """

    model_config = ConfigDict(from_attributes=True)

    customer_id: str
    name: str
    email: str
    phone: Optional[str]
    document: Optional[str]
    address: Optional[AddressOutputDTO]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity) -> "CustomerOutputDTO":
        """Constrói o DTO de saída a partir de uma CustomerEntity."""
        address = None
        if entity.address:
            address = AddressOutputDTO(
                street=entity.address.street,
                number=entity.address.number,
                complement=entity.address.complement,
                neighborhood=entity.address.neighborhood,
                city=entity.address.city,
                state=entity.address.state,
                zip_code=entity.address.zip_code,
            )
        return cls(
            customer_id=entity.id.value,
            name=entity.name.value,
            email=entity.email.value,
            phone=entity.phone.value if entity.phone else None,
            document=entity.document.value if entity.document else None,
            address=address,
            notes=entity.notes,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class CustomerSummaryOutputDTO(BaseModel):
    """Resposta resumida para listagens de clientes."""

    model_config = ConfigDict(from_attributes=True)

    customer_id: str
    name: str
    email: str
    phone: Optional[str]
    is_active: bool
    created_at: datetime

    @classmethod
    def from_read_model(cls, read_model) -> "CustomerSummaryOutputDTO":
        """Constrói o DTO a partir de um CustomerSummary (read model)."""
        return cls(
            customer_id=read_model.customer_id,
            name=read_model.name,
            email=read_model.email,
            phone=read_model.phone,
            is_active=read_model.is_active,
            created_at=read_model.created_at,
        )


class CustomerListOutputDTO(BaseModel):
    """Resposta paginada de listagem de clientes."""

    items: list[CustomerSummaryOutputDTO]
    total: int
    limit: int
    offset: int
