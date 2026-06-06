from app.modules.customer.application.dtos.customer_dtos import CustomerOutputDTO
from app.modules.customer.domain.exceptions.customers_exceptions import CustomerNotFoundError
from app.modules.customer.domain.repositories.customer_repository import CustomerRepository
from app.modules.customer.domain.value_objects.customer_id import CustomerId


class ActivateCustomerUseCase:
    """
    Caso de uso: Reativar um cliente inativo.

    A regra de negócio (não reativar se já ativo) fica na entidade.

    Fluxo:
    1. Busca a entidade
    2. Delega activate() à entidade (valida estado)
    3. Persiste e retorna o DTO de saída
    """

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    async def execute(self, customer_id: str) -> CustomerOutputDTO:
        entity = await self._repository.get_by_id(CustomerId(value=customer_id))
        if not entity:
            raise CustomerNotFoundError(identifier=customer_id)

        entity.activate()

        updated = await self._repository.update(entity)
        return CustomerOutputDTO.from_entity(updated)


class DeactivateCustomerUseCase:
    """
    Caso de uso: Desativar um cliente ativo.

    A regra de negócio (não desativar se já inativo) fica na entidade.

    Fluxo:
    1. Busca a entidade
    2. Delega deactivate() à entidade (valida estado)
    3. Persiste e retorna o DTO de saída
    """

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    async def execute(self, customer_id: str) -> CustomerOutputDTO:
        entity = await self._repository.get_by_id(CustomerId(value=customer_id))
        if not entity:
            raise CustomerNotFoundError(identifier=customer_id)

        entity.deactivate()

        updated = await self._repository.update(entity)
        return CustomerOutputDTO.from_entity(updated)
