from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class CustomerSummary:
    """
    Read Model com dados resumidos do cliente.
    
    Usado em listagens e buscas onde não é necessário carregar
    todos os dados da entidade completa.
    """

    customer_id: str
    name: str
    email: str
    phone: Optional[str]
    is_active: bool
    created_at: datetime


@dataclass(frozen=True)
class CustomerProfile:
    """
    Read Model com o perfil completo do cliente.
    
    Usado na visualização de detalhes de um cliente específico.
    Inclui endereço e observações internas.
    """

    customer_id: str
    name: str
    email: str
    phone: Optional[str]
    document: Optional[str]
    street: Optional[str]
    number: Optional[str]
    complement: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
