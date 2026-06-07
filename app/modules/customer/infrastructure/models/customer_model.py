from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.database.base import BaseModel

from app.modules.customer.domain.entities.customer_entity import CustomerEntity
from app.modules.customer.domain.value_objects.customer_id import CustomerId
from app.modules.customer.domain.value_objects.customer_name import CustomerName
from app.modules.customer.domain.value_objects.customer_email import CustomerEmail
from app.modules.customer.domain.value_objects.customer_phone import CustomerPhone
from app.modules.customer.domain.value_objects.customer_document import CustomerDocument
from app.modules.customer.domain.value_objects.customer_address import CustomerAddress


class CustomerModel(BaseModel):
    """
    Model ORM que representa a tabela 'customers' no banco de dados.

    Responsabilidades:
    - Mapear colunas do banco para atributos Python
    - Converter para/de CustomerEntity (domínio)

    O endereço é armazenado flat na mesma tabela (sem tabela separada),
    pois o cliente da confeitaria tem apenas um endereço principal.
    """

    __tablename__ = "customers"

    # ─── Identificação ────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    document: Mapped[Optional[str]] = mapped_column(String(11), nullable=True, unique=True, index=True)

    # ─── Endereço (flat) ─────────────────────────────────────────────────────
    address_street: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    address_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address_complement: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address_neighborhood: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address_city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address_state: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    address_zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    # ─── Metadados ───────────────────────────────────────────────────────────
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # ─── Conversões ──────────────────────────────────────────────────────────

    @classmethod
    def from_entity(cls, entity: CustomerEntity) -> "CustomerModel":
        """
        Converte uma CustomerEntity (domínio) em CustomerModel (ORM).

        Extrai os valores primitivos de cada Value Object para
        armazenar no banco de dados.
        """
        address = entity.address

        return cls(
            id=entity.id.value,
            name=entity.name.value,
            email=entity.email.value,
            phone=entity.phone.value if entity.phone else None,
            document=entity.document.value if entity.document else None,
            # Endereço flat — todos None se não houver endereço
            address_street=address.street if address else None,
            address_number=address.number if address else None,
            address_complement=address.complement if address else None,
            address_neighborhood=address.neighborhood if address else None,
            address_city=address.city if address else None,
            address_state=address.state if address else None,
            address_zip_code=address.zip_code if address else None,
            notes=entity.notes,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> CustomerEntity:
        """
        Converte um CustomerModel (ORM) em CustomerEntity (domínio).

        Reconstrói cada Value Object a partir dos valores primitivos do banco.
        O endereço só é reconstruído se todos os campos obrigatórios estiverem presentes.
        """
        address: Optional[CustomerAddress] = None
        if self.address_street and self.address_number and self.address_city:
            address = CustomerAddress(
                street=self.address_street,
                number=self.address_number,
                complement=self.address_complement,
                neighborhood=self.address_neighborhood or "",
                city=self.address_city,
                state=self.address_state or "",
                zip_code=self.address_zip_code or "",
            )

        return CustomerEntity(
            id=CustomerId(value=self.id),
            name=CustomerName(value=self.name),
            email=CustomerEmail(value=self.email),
            phone=CustomerPhone(value=self.phone) if self.phone else None,
            document=CustomerDocument(value=self.document) if self.document else None,
            address=address,
            notes=self.notes,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def update_from_entity(self, entity: CustomerEntity) -> None:
        """
        Atualiza os campos do model a partir de uma entidade.

        Usado no repositório para evitar deletar e recriar o registro,
        preservando assim o histórico de auditoria do SQLAlchemy.
        """
        address = entity.address

        self.name = entity.name.value
        self.email = entity.email.value
        self.phone = entity.phone.value if entity.phone else None
        self.document = entity.document.value if entity.document else None
        self.address_street = address.street if address else None
        self.address_number = address.number if address else None
        self.address_complement = address.complement if address else None
        self.address_neighborhood = address.neighborhood if address else None
        self.address_city = address.city if address else None
        self.address_state = address.state if address else None
        self.address_zip_code = address.zip_code if address else None
        self.notes = entity.notes
        self.is_active = entity.is_active
        self.updated_at = entity.updated_at
