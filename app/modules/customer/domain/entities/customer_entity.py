from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.modules.customer.domain.value_objects.customer_address import CustomerAddress
from app.modules.customer.domain.value_objects.customer_document import CustomerDocument
from app.modules.customer.domain.value_objects.customer_email import CustomerEmail
from app.modules.customer.domain.value_objects.customer_id import CustomerId
from app.modules.customer.domain.value_objects.customer_name import CustomerName
from app.modules.customer.domain.value_objects.customer_phone import CustomerPhone


@dataclass
class CustomerEntity:
    """
    Entidade que representa um Cliente no domínio.
    
    Encapsula todas as regras de negócio relacionadas ao cliente da confeitaria.
    Um cliente pode fazer pedidos, ter endereços de entrega e acumular histórico.
    """

    id: CustomerId
    name: CustomerName
    email: CustomerEmail
    phone: Optional[CustomerPhone]
    document: Optional[CustomerDocument]       # CPF (opcional)
    address: Optional[CustomerAddress]         # Endereço principal de entrega
    notes: Optional[str]                       # Observações internas (ex: alergias)
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        name: CustomerName,
        email: CustomerEmail,
        phone: Optional[CustomerPhone] = None,
        document: Optional[CustomerDocument] = None,
        address: Optional[CustomerAddress] = None,
        notes: Optional[str] = None,
    ) -> "CustomerEntity":
        """
        Factory method para criar um novo cliente.
        
        Gera ID automaticamente e define timestamps de criação.
        
        Args:
            name: Nome do cliente
            email: E-mail do cliente
            phone: Telefone (opcional)
            document: CPF (opcional)
            address: Endereço principal (opcional)
            notes: Observações internas (opcional)
            
        Returns:
            CustomerEntity: Nova entidade de cliente
        """
        now = datetime.utcnow()
        return cls(
            id=CustomerId.generate(),
            name=name,
            email=email,
            phone=phone,
            document=document,
            address=address,
            notes=notes,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def update_contact_info(
        self,
        name: Optional[CustomerName] = None,
        phone: Optional[CustomerPhone] = None,
    ) -> None:
        """
        Atualiza informações de contato do cliente.
        
        Args:
            name: Novo nome (se fornecido)
            phone: Novo telefone (se fornecido)
        """
        if name is not None:
            self.name = name
        if phone is not None:
            self.phone = phone
        self.updated_at = datetime.utcnow()

    def update_address(self, address: Optional[CustomerAddress]) -> None:
        """
        Atualiza o endereço principal de entrega.
        
        Args:
            address: Novo endereço ou None para remover
        """
        self.address = address
        self.updated_at = datetime.utcnow()

    def update_notes(self, notes: Optional[str]) -> None:
        """
        Atualiza as observações internas do cliente.
        
        Útil para registrar alergias, preferências e instruções especiais.
        
        Args:
            notes: Novas observações ou None para limpar
        """
        self.notes = notes
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Desativa o cliente, impedindo novos pedidos."""
        if not self.is_active:
            raise ValueError("Cliente já está inativo.")
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Reativa um cliente previamente desativado."""
        if self.is_active:
            raise ValueError("Cliente já está ativo.")
        self.is_active = True
        self.updated_at = datetime.utcnow()
