from typing import List, Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.modules.customer.domain.entities.customer_entity import CustomerEntity
from app.modules.customer.domain.exceptions.customers_exceptions import CustomerNotFoundError
from app.modules.customer.domain.read_models.customer_rm import (
    CustomerProfile,
    CustomerSummary,
)
from app.modules.customer.domain.repositories.customer_repository import CustomerRepository
from app.modules.customer.domain.value_objects.customer_document import CustomerDocument
from app.modules.customer.domain.value_objects.customer_email import CustomerEmail
from app.modules.customer.domain.value_objects.customer_id import CustomerId
from app.modules.customer.infrastructure.models.customer_model import CustomerModel


class CustomerRepositoryImpl(CustomerRepository):
    """
    Implementação concreta do CustomerRepository usando SQLAlchemy.

    Responsabilidades:
    - Converter entre CustomerEntity (domínio) e CustomerModel (ORM)
    - Executar operações no banco de dados
    - Montar Read Models diretamente das queries (sem passar pela entidade)
    """

    def __init__(self, db: Session):
        self._db = db

    # ─── Comandos ─────────────────────────────────────────────────────────────

    async def create(self, customer: CustomerEntity) -> CustomerEntity:
        """
        Persiste um novo cliente no banco.

        Args:
            customer: Entidade do cliente

        Returns:
            CustomerEntity: Entidade persistida
        """
        model = CustomerModel.from_entity(customer)

        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)

        return model.to_entity()

    async def update(self, customer: CustomerEntity) -> CustomerEntity:
        """
        Atualiza os dados de um cliente existente.

        Atualiza in-place para preservar o objeto rastreado pelo SQLAlchemy.

        Args:
            customer: Entidade com dados atualizados

        Returns:
            CustomerEntity: Entidade atualizada

        Raises:
            CustomerNotFoundError: Se o cliente não existir no banco
        """
        stmt = select(CustomerModel).where(CustomerModel.id == customer.id.value)
        model = self._db.execute(stmt).scalar_one_or_none()

        if not model:
            raise CustomerNotFoundError(identifier=customer.id.value)

        model.update_from_entity(customer)

        self._db.commit()
        self._db.refresh(model)

        return model.to_entity()

    async def delete(self, customer_id: CustomerId) -> bool:
        """
        Remove um cliente do banco.

        Args:
            customer_id: ID do cliente a remover

        Returns:
            bool: True se removido com sucesso, False se não encontrado
        """
        stmt = select(CustomerModel).where(CustomerModel.id == customer_id.value)
        model = self._db.execute(stmt).scalar_one_or_none()

        if not model:
            return False

        self._db.delete(model)
        self._db.commit()

        return True

    # ─── Queries — Entidade completa ──────────────────────────────────────────

    async def get_by_id(self, customer_id: CustomerId) -> Optional[CustomerEntity]:
        """
        Busca cliente pelo ID.

        Args:
            customer_id: ID do cliente

        Returns:
            Optional[CustomerEntity]: Entidade do cliente ou None
        """
        stmt = select(CustomerModel).where(CustomerModel.id == customer_id.value)
        model = self._db.execute(stmt).scalar_one_or_none()

        return model.to_entity() if model else None

    async def get_by_email(self, email: CustomerEmail) -> Optional[CustomerEntity]:
        """
        Busca cliente pelo e-mail.

        Args:
            email: E-mail do cliente

        Returns:
            Optional[CustomerEntity]: Entidade do cliente ou None
        """
        stmt = select(CustomerModel).where(CustomerModel.email == email.value)
        model = self._db.execute(stmt).scalar_one_or_none()

        return model.to_entity() if model else None

    async def get_by_document(self, document: CustomerDocument) -> Optional[CustomerEntity]:
        """
        Busca cliente pelo CPF.

        Args:
            document: CPF do cliente

        Returns:
            Optional[CustomerEntity]: Entidade do cliente ou None
        """
        stmt = select(CustomerModel).where(CustomerModel.document == document.value)
        model = self._db.execute(stmt).scalar_one_or_none()

        return model.to_entity() if model else None

    # ─── Queries — Verificação de existência ─────────────────────────────────

    async def exists_by_email(self, email: CustomerEmail) -> bool:
        """
        Verifica se já existe um cliente com o e-mail informado.

        Args:
            email: E-mail a verificar

        Returns:
            bool: True se o e-mail já está cadastrado
        """
        stmt = select(CustomerModel.id).where(CustomerModel.email == email.value)
        return self._db.execute(stmt).scalar_one_or_none() is not None

    async def exists_by_document(self, document: CustomerDocument) -> bool:
        """
        Verifica se já existe um cliente com o CPF informado.

        Args:
            document: CPF a verificar

        Returns:
            bool: True se o CPF já está cadastrado
        """
        stmt = select(CustomerModel.id).where(CustomerModel.document == document.value)
        return self._db.execute(stmt).scalar_one_or_none() is not None

    # ─── Queries — Read Models ────────────────────────────────────────────────

    async def list_summaries(
        self,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[CustomerSummary]:
        """
        Lista resumos de clientes com filtros opcionais.

        Seleciona apenas as colunas necessárias para o Read Model,
        evitando carregar dados desnecessários (endereço, notes etc).

        Args:
            is_active: Filtrar por status ativo/inativo (None = todos)
            search: Busca parcial por nome ou e-mail (case-insensitive)
            limit: Limite de registros por página
            offset: Deslocamento para paginação

        Returns:
            List[CustomerSummary]: Lista de resumos de clientes
        """
        stmt = select(
            CustomerModel.id,
            CustomerModel.name,
            CustomerModel.email,
            CustomerModel.phone,
            CustomerModel.is_active,
            CustomerModel.created_at,
        )

        stmt = self._apply_filters(stmt, is_active=is_active, search=search)
        stmt = stmt.order_by(CustomerModel.name).limit(limit).offset(offset)

        rows = self._db.execute(stmt).all()

        return [
            CustomerSummary(
                customer_id=row.id,
                name=row.name,
                email=row.email,
                phone=row.phone,
                is_active=row.is_active,
                created_at=row.created_at,
            )
            for row in rows
        ]

    async def count(
        self,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> int:
        """
        Conta o total de clientes com filtros opcionais.

        Args:
            is_active: Filtrar por status ativo/inativo (None = todos)
            search: Busca parcial por nome ou e-mail

        Returns:
            int: Total de clientes que atendem ao filtro
        """
        stmt = select(func.count(CustomerModel.id))
        stmt = self._apply_filters(stmt, is_active=is_active, search=search)

        return self._db.execute(stmt).scalar_one()

    async def get_profile(self, customer_id: CustomerId) -> Optional[CustomerProfile]:
        """
        Busca o perfil completo do cliente como Read Model.

        Retorna todos os campos incluindo endereço, sem reconstituir VOs.

        Args:
            customer_id: ID do cliente

        Returns:
            Optional[CustomerProfile]: Perfil do cliente ou None
        """
        stmt = select(CustomerModel).where(CustomerModel.id == customer_id.value)
        model = self._db.execute(stmt).scalar_one_or_none()

        if not model:
            return None

        return CustomerProfile(
            customer_id=model.id,
            name=model.name,
            email=model.email,
            phone=model.phone,
            document=model.document,
            street=model.address_street,
            number=model.address_number,
            complement=model.address_complement,
            neighborhood=model.address_neighborhood,
            city=model.address_city,
            state=model.address_state,
            zip_code=model.address_zip_code,
            notes=model.notes,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # ─── Helpers privados ─────────────────────────────────────────────────────

    @staticmethod
    def _apply_filters(stmt, is_active: Optional[bool], search: Optional[str]):
        """
        Aplica filtros reutilizáveis de status e busca textual a um statement.

        Args:
            stmt: Statement SQLAlchemy base
            is_active: Filtro de status ativo/inativo
            search: Busca parcial por nome ou e-mail

        Returns:
            Statement com filtros aplicados
        """
        if is_active is not None:
            stmt = stmt.where(CustomerModel.is_active == is_active)

        if search:
            pattern = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    CustomerModel.name.ilike(pattern),
                    CustomerModel.email.ilike(pattern),
                )
            )

        return stmt
