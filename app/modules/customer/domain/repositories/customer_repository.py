from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.customer.domain.entities.customer_entity import CustomerEntity
from app.modules.customer.domain.read_models.customer_rm import (
    CustomerProfile,
    CustomerSummary,
)
from app.modules.customer.domain.value_objects.customer_document import CustomerDocument
from app.modules.customer.domain.value_objects.customer_email import CustomerEmail
from app.modules.customer.domain.value_objects.customer_id import CustomerId


class CustomerRepository(ABC):
    """
    Interface (porta) do repositório de clientes.
    
    Define o contrato que qualquer implementação de persistência deve seguir.
    A camada de domínio depende apenas desta abstração, nunca da implementação.
    """

    @abstractmethod
    async def create(self, customer: CustomerEntity) -> CustomerEntity:
        """
        Persiste um novo cliente.
        
        Args:
            customer: Entidade do cliente a ser criada
            
        Returns:
            CustomerEntity: Entidade persistida (com dados atualizados do banco)
        """
        ...

    @abstractmethod
    async def get_by_id(self, customer_id: CustomerId) -> Optional[CustomerEntity]:
        """
        Busca cliente pelo ID.
        
        Args:
            customer_id: ID do cliente
            
        Returns:
            Optional[CustomerEntity]: Entidade do cliente ou None se não encontrado
        """
        ...

    @abstractmethod
    async def get_by_email(self, email: CustomerEmail) -> Optional[CustomerEntity]:
        """
        Busca cliente pelo e-mail.
        
        Args:
            email: E-mail do cliente
            
        Returns:
            Optional[CustomerEntity]: Entidade do cliente ou None se não encontrado
        """
        ...

    @abstractmethod
    async def get_by_document(self, document: CustomerDocument) -> Optional[CustomerEntity]:
        """
        Busca cliente pelo CPF.
        
        Args:
            document: CPF do cliente
            
        Returns:
            Optional[CustomerEntity]: Entidade do cliente ou None se não encontrado
        """
        ...

    @abstractmethod
    async def exists_by_email(self, email: CustomerEmail) -> bool:
        """
        Verifica se já existe um cliente com o e-mail informado.
        
        Args:
            email: E-mail a verificar
            
        Returns:
            bool: True se o e-mail já está cadastrado
        """
        ...

    @abstractmethod
    async def exists_by_document(self, document: CustomerDocument) -> bool:
        """
        Verifica se já existe um cliente com o CPF informado.
        
        Args:
            document: CPF a verificar
            
        Returns:
            bool: True se o CPF já está cadastrado
        """
        ...

    @abstractmethod
    async def update(self, customer: CustomerEntity) -> CustomerEntity:
        """
        Atualiza os dados de um cliente existente.
        
        Args:
            customer: Entidade com dados atualizados
            
        Returns:
            CustomerEntity: Entidade atualizada
            
        Raises:
            CustomerNotFoundError: Se o cliente não existir
        """
        ...

    @abstractmethod
    async def delete(self, customer_id: CustomerId) -> bool:
        """
        Remove um cliente.
        
        Args:
            customer_id: ID do cliente a remover
            
        Returns:
            bool: True se removido com sucesso, False se não encontrado
        """
        ...

    # ─── Read Models (queries otimizadas) ────────────────────────────────────

    @abstractmethod
    async def list_summaries(
        self,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[CustomerSummary]:
        """
        Lista resumos de clientes com filtros opcionais.
        
        Retorna Read Model leve, sem carregar todos os dados da entidade.
        
        Args:
            is_active: Filtrar por status ativo/inativo (None = todos)
            search: Busca parcial por nome ou e-mail
            limit: Limite de registros por página
            offset: Deslocamento para paginação
            
        Returns:
            List[CustomerSummary]: Lista de resumos de clientes
        """
        ...

    @abstractmethod
    async def count(
        self,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> int:
        """
        Conta o total de clientes com filtros opcionais.
        
        Usado para calcular totais de paginação.
        
        Args:
            is_active: Filtrar por status ativo/inativo (None = todos)
            search: Busca parcial por nome ou e-mail
            
        Returns:
            int: Total de clientes que atendem ao filtro
        """
        ...

    @abstractmethod
    async def get_profile(self, customer_id: CustomerId) -> Optional[CustomerProfile]:
        """
        Busca o perfil completo do cliente como Read Model.
        
        Args:
            customer_id: ID do cliente
            
        Returns:
            Optional[CustomerProfile]: Perfil do cliente ou None
        """
        ...
