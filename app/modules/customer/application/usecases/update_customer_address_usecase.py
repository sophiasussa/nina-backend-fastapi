from app.modules.customer.application.dtos.customer_dtos import (
    UpdateAddressInputDTO,
    CustomerOutputDTO,
)
from app.modules.customer.domain.exceptions.customers_exceptions import CustomerNotFoundError
from app.modules.customer.domain.repositories.customer_repository import CustomerRepository
from app.modules.customer.domain.value_objects.customer_address import CustomerAddress
from app.modules.customer.domain.value_objects.customer_id import CustomerId


class UpdateCustomerAddressUseCase:
    """
    Caso de uso: Substituir ou remover o endereço principal de um cliente.

    Separado do UpdateCustomerUseCase porque o endereço tem
    seu próprio VO composto (CustomerAddress) e ciclo de vida.

    Enviar address=None remove o endereço existente.

    Fluxo:
    1. Busca a entidade existente
    2. Constrói o VO de endereço (ou None para remover)
    3. Delega a mutação à entidade
    4. Persiste e retorna o DTO de saída
    """

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    async def execute(self, customer_id: str, dto: UpdateAddressInputDTO) -> CustomerOutputDTO:
        # 1. Busca entidade
        entity = await self._repository.get_by_id(CustomerId(value=customer_id))
        if not entity:
            raise CustomerNotFoundError(identifier=customer_id)

        # 2. Constrói VO ou None
        address = None
        if dto.address is not None:
            address = CustomerAddress(
                street=dto.address.street,
                number=dto.address.number,
                complement=dto.address.complement,
                neighborhood=dto.address.neighborhood,
                city=dto.address.city,
                state=dto.address.state,
                zip_code=dto.address.zip_code,
            )

        # 3. Delega à entidade
        entity.update_address(address=address)

        # 4. Persiste e retorna
        updated = await self._repository.update(entity)
        return CustomerOutputDTO.from_entity(updated)
