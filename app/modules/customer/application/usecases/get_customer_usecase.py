from app.modules.customer.application.dtos.customer_dtos import CustomerOutputDTO
from app.modules.customer.domain.exceptions.customers_exceptions import CustomerNotFoundError
from app.modules.customer.domain.repositories.customer_repository import CustomerRepository
from app.modules.customer.domain.value_objects.customer_id import CustomerId


class GetCustomerUseCase:
    """
    Caso de uso: Buscar perfil completo de um cliente pelo ID.

    Usa o read model CustomerProfile para evitar reconstituir
    a entidade completa quando o objetivo é apenas leitura.

    Fluxo:
    1. Consulta o perfil via read model (query otimizada)
    2. Lança exceção se não encontrado
    3. Monta e retorna o DTO de saída
    """

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    async def execute(self, customer_id: str) -> CustomerOutputDTO:
        profile = await self._repository.get_profile(CustomerId(value=customer_id))

        if not profile:
            raise CustomerNotFoundError(identifier=customer_id)

        # Monta o endereço apenas se os campos obrigatórios existirem
        address = None
        if profile.street and profile.number and profile.city:
            from app.modules.customer.application.dtos.customer_dtos import AddressOutputDTO
            address = AddressOutputDTO(
                street=profile.street,
                number=profile.number,
                complement=profile.complement,
                neighborhood=profile.neighborhood or "",
                city=profile.city,
                state=profile.state or "",
                zip_code=profile.zip_code or "",
            )

        return CustomerOutputDTO(
            customer_id=profile.customer_id,
            name=profile.name,
            email=profile.email,
            phone=profile.phone,
            document=profile.document,
            address=address,
            notes=profile.notes,
            is_active=profile.is_active,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )
