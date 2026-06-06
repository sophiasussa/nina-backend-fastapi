from app.modules.customer.domain.exceptions.customers_exceptions import CustomerNotFoundError
from app.modules.customer.domain.repositories.customer_repository import CustomerRepository
from app.modules.customer.domain.value_objects.customer_id import CustomerId


class DeleteCustomerUseCase:
    """
    Caso de uso: Remover permanentemente um cliente.

    Use com cautela — prefira DeactivateCustomerUseCase para
    preservar histórico de pedidos. Delete é para LGPD/exclusão total.

    Fluxo:
    1. Tenta deletar via repositório
    2. Lança exceção se não encontrado
    """

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    async def execute(self, customer_id: str) -> None:
        deleted = await self._repository.delete(CustomerId(value=customer_id))

        if not deleted:
            raise CustomerNotFoundError(identifier=customer_id)
