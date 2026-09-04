from app.modules.customer.domain.exceptions.customers_exceptions import (
    CustomerNotFoundError,
    CustomerValidationError,
)
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
        try:
            customer_key = CustomerId(value=customer_id)
        except ValueError as exc:
            raise CustomerValidationError(field="customer_id", reason=str(exc)) from exc

        deleted = await self._repository.delete(customer_key)

        if not deleted:
            raise CustomerNotFoundError(identifier=customer_id)
