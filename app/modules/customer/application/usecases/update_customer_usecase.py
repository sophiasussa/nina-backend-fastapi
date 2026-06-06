from app.modules.customer.application.dtos.customer_dtos import (
    UpdateCustomerInputDTO,
    CustomerOutputDTO,
)
from app.modules.customer.domain.exceptions.customers_exceptions import CustomerNotFoundError
from app.modules.customer.domain.repositories.customer_repository import CustomerRepository
from app.modules.customer.domain.value_objects.customer_id import CustomerId
from app.modules.customer.domain.value_objects.customer_name import CustomerName
from app.modules.customer.domain.value_objects.customer_phone import CustomerPhone


class UpdateCustomerUseCase:
    """
    Caso de uso: Atualizar contato e observações de um cliente (PATCH).

    Apenas os campos enviados no DTO são alterados.
    Campos None são ignorados — o valor atual é mantido.

    Fluxo:
    1. Busca a entidade existente
    2. Constrói VOs apenas dos campos fornecidos
    3. Delega a mutação à entidade
    4. Persiste e retorna o DTO de saída
    """

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    async def execute(self, customer_id: str, dto: UpdateCustomerInputDTO) -> CustomerOutputDTO:
        # 1. Busca entidade
        entity = await self._repository.get_by_id(CustomerId(value=customer_id))
        if not entity:
            raise CustomerNotFoundError(identifier=customer_id)

        # 2. Constrói VOs apenas dos campos enviados
        new_name = CustomerName(value=dto.name) if dto.name is not None else None
        new_phone = CustomerPhone.create_optional(dto.phone) if dto.phone is not None else None

        # 3. Delega mutações à entidade (preserva regras de negócio)
        entity.update_contact_info(name=new_name, phone=new_phone)

        if dto.notes is not None:
            entity.update_notes(notes=dto.notes)

        # 4. Persiste e retorna
        updated = await self._repository.update(entity)
        return CustomerOutputDTO.from_entity(updated)
