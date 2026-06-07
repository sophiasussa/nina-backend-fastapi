from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.modules.auth.presentation.dependencies.auth_deps import CurrentUser

from app.modules.customer.application.dtos.customer_dtos import (
    CreateCustomerInputDTO,
    ListCustomersInputDTO,
    UpdateAddressInputDTO,
    UpdateCustomerInputDTO,
)

from app.modules.customer.application.usecases.create_customer_usecase import CreateCustomerUseCase
from app.modules.customer.application.usecases.update_customer_usecase import UpdateCustomerUseCase
from app.modules.customer.application.usecases.update_customer_address_usecase import UpdateCustomerAddressUseCase
from app.modules.customer.application.usecases.get_customer_usecase import GetCustomerUseCase
from app.modules.customer.application.usecases.list_customers_usecase import ListCustomersUseCase
from app.modules.customer.application.usecases.toggle_customer_status_usecase import (
    ActivateCustomerUseCase,
    DeactivateCustomerUseCase,
)
from app.modules.customer.application.usecases.delete_customer_usecase import DeleteCustomerUseCase

from app.modules.customer.domain.exceptions.customers_exceptions import (
    CustomerAlreadyExistsError,
    CustomerDocumentAlreadyExistsError,
    CustomerDomainError,
    CustomerInactiveError,
    CustomerNotFoundError,
)

from app.modules.customer.presentation.dependencies.customer_deps import (
    get_activate_customer_use_case,
    get_create_customer_use_case,
    get_customer_use_case,
    get_deactivate_customer_use_case,
    get_delete_customer_use_case,
    get_list_customers_use_case,
    get_update_customer_address_use_case,
    get_update_customer_use_case,
)

from app.modules.customer.presentation.schemas.customer_schemas import (
    CreateCustomerSchema,
    CustomerListSchema,
    CustomerResponseSchema,
    CustomerSummarySchema,
    UpdateAddressSchema,
    UpdateCustomerSchema,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _handle_domain_error(exc: CustomerDomainError) -> HTTPException:
    if isinstance(exc, CustomerNotFoundError):
        return HTTPException(status_code=404, detail=str(exc))

    if isinstance(exc, (CustomerAlreadyExistsError, CustomerDocumentAlreadyExistsError)):
        return HTTPException(status_code=409, detail=str(exc))

    if isinstance(exc, CustomerInactiveError):
        return HTTPException(status_code=422, detail=str(exc))

    return HTTPException(status_code=400, detail=str(exc))


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────

@router.post(
    "",
    response_model=CustomerResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    body: CreateCustomerSchema,
    current_user: CurrentUser,
    use_case: CreateCustomerUseCase = Depends(get_create_customer_use_case),
) -> CustomerResponseSchema:
    try:
        result = await use_case.execute(
            CreateCustomerInputDTO(
                name=body.name,
                email=body.email,
                phone=body.phone,
                document=body.document,
                address=body.address,
                notes=body.notes,
            )
        )
        return CustomerResponseSchema(**result.model_dump())

    except CustomerDomainError as exc:
        raise _handle_domain_error(exc)


@router.get("", response_model=CustomerListSchema)
async def list_customers(
    current_user: CurrentUser,
    search: str | None = Query(None, max_length=100),
    is_active: bool | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    use_case: ListCustomersUseCase = Depends(get_list_customers_use_case),
) -> CustomerListSchema:

    result = await use_case.execute(
        ListCustomersInputDTO(
            search=search,
            is_active=is_active,
            limit=limit,
            offset=offset,
        )
    )

    return CustomerListSchema(
        items=[CustomerSummarySchema(**item.model_dump()) for item in result.items],
        total=result.total,
        limit=result.limit,
        offset=result.offset,
    )


@router.get("/{customer_id}", response_model=CustomerResponseSchema)
async def get_customer(
    customer_id: str,
    current_user: CurrentUser,
    use_case: GetCustomerUseCase = Depends(get_customer_use_case),
) -> CustomerResponseSchema:

    try:
        result = await use_case.execute(customer_id)
        return CustomerResponseSchema(**result.model_dump())

    except CustomerDomainError as exc:
        raise _handle_domain_error(exc)


@router.patch("/{customer_id}", response_model=CustomerResponseSchema)
async def update_customer(
    customer_id: str,
    body: UpdateCustomerSchema,
    current_user: CurrentUser,
    use_case: UpdateCustomerUseCase = Depends(get_update_customer_use_case),
) -> CustomerResponseSchema:

    try:
        result = await use_case.execute(
            customer_id,
            UpdateCustomerInputDTO(
                name=body.name,
                phone=body.phone,
                notes=body.notes,
            ),
        )
        return CustomerResponseSchema(**result.model_dump())

    except CustomerDomainError as exc:
        raise _handle_domain_error(exc)


@router.patch("/{customer_id}/address", response_model=CustomerResponseSchema)
async def update_customer_address(
    customer_id: str,
    body: UpdateAddressSchema,
    current_user: CurrentUser,
    use_case: UpdateCustomerAddressUseCase = Depends(get_update_customer_address_use_case),
) -> CustomerResponseSchema:

    try:
        result = await use_case.execute(
            customer_id,
            UpdateAddressInputDTO(address=body.address),
        )
        return CustomerResponseSchema(**result.model_dump())

    except CustomerDomainError as exc:
        raise _handle_domain_error(exc)


@router.patch("/{customer_id}/activate", response_model=CustomerResponseSchema)
async def activate_customer(
    customer_id: str,
    current_user: CurrentUser,
    use_case: ActivateCustomerUseCase = Depends(get_activate_customer_use_case),
) -> CustomerResponseSchema:

    try:
        result = await use_case.execute(customer_id)
        return CustomerResponseSchema(**result.model_dump())

    except CustomerDomainError as exc:
        raise _handle_domain_error(exc)


@router.patch("/{customer_id}/deactivate", response_model=CustomerResponseSchema)
async def deactivate_customer(
    customer_id: str,
    current_user: CurrentUser,
    use_case: DeactivateCustomerUseCase = Depends(get_deactivate_customer_use_case),
) -> CustomerResponseSchema:

    try:
        result = await use_case.execute(customer_id)
        return CustomerResponseSchema(**result.model_dump())

    except CustomerDomainError as exc:
        raise _handle_domain_error(exc)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: str,
    current_user: CurrentUser,
    use_case: DeleteCustomerUseCase = Depends(get_delete_customer_use_case),
) -> None:

    try:
        await use_case.execute(customer_id)

    except CustomerDomainError as exc:
        raise _handle_domain_error(exc)
