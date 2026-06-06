from app.modules.customer.application.dtos.customer_dtos import (
    CreateCustomerInputDTO,
    CustomerOutputDTO,
)
from app.modules.customer.domain.entities.customer_entity import CustomerEntity
from app.modules.customer.domain.exceptions.customers_exceptions import (
    CustomerAlreadyExistsError,
    CustomerDocumentAlreadyExistsError,
)
from app.modules.customer.domain.repositories.customer_repository import CustomerRepository
from app.modules.customer.domain.value_objects.customer_address import CustomerAddress
from app.modules.customer.domain.value_objects.customer_document import CustomerDocument
from app.modules.customer.domain.value_objects.customer_email import CustomerEmail
from app.modules.customer.domain.value_objects.customer_name import CustomerName
from app.modules.customer.domain.value_objects.customer_phone import CustomerPhone


class CreateCustomerUseCase:
    """
    Caso de uso: Criar novo cliente.

    Fluxo:
    1. Constrói os Value Objects (validação de formato)
    2. Verifica unicidade de e-mail e CPF
    3. Cria a entidade via factory method
    4. Persiste e retorna o DTO de saída
    """

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    async def execute(self, dto: CreateCustomerInputDTO) -> CustomerOutputDTO:
        # 1. Constrói Value Objects
        name = CustomerName(value=dto.name)
        email = CustomerEmail(value=dto.email)
        phone = CustomerPhone.create_optional(dto.phone)
        document = CustomerDocument.create_optional(dto.document)

        address = None
        if dto.address:
            address = CustomerAddress(
                street=dto.address.street,
                number=dto.address.number,
                complement=dto.address.complement,
                neighborhood=dto.address.neighborhood,
                city=dto.address.city,
                state=dto.address.state,
                zip_code=dto.address.zip_code,
            )

        # 2. Verifica unicidade
        if await self._repository.exists_by_email(email):
            raise CustomerAlreadyExistsError(email=email.value)

        if document and await self._repository.exists_by_document(document):
            raise CustomerDocumentAlreadyExistsError(document=document.value)

        # 3. Cria entidade
        customer = CustomerEntity.create(
            name=name,
            email=email,
            phone=phone,
            document=document,
            address=address,
            notes=dto.notes,
        )

        # 4. Persiste e retorna
        created = await self._repository.create(customer)
        return CustomerOutputDTO.from_entity(created)
