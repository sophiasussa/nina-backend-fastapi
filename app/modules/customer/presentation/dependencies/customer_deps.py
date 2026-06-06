from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.infrastructure.database.session import get_db

from app.modules.customer.domain.repositories.customer_repository import CustomerRepository
from app.modules.customer.infrastructure.repositories.customer_repository_impl import (
    CustomerRepositoryImpl,
)
from app.modules.customer.application.usecases.create_customer_usecase import (
    CreateCustomerUseCase,
)
from app.modules.customer.application.usecases.update_customer_usecase import (
    UpdateCustomerUseCase,
)
from app.modules.customer.application.usecases.update_customer_address_usecase import (
    UpdateCustomerAddressUseCase,
)
from app.modules.customer.application.usecases.get_customer_usecase import (
    GetCustomerUseCase,
)
from app.modules.customer.application.usecases.list_customers_usecase import (
    ListCustomersUseCase,
)
from app.modules.customer.application.usecases.toggle_customer_status_usecase import (
    ActivateCustomerUseCase,
    DeactivateCustomerUseCase,
)
from app.modules.customer.application.usecases.delete_customer_usecase import (
    DeleteCustomerUseCase,
)


# ─── Infraestrutura ───────────────────────────────────────────────────────────


def get_customer_repository(db: Session = Depends(get_db)) -> CustomerRepository:
    """Dependency para obter CustomerRepository."""
    return CustomerRepositoryImpl(db)


# ─── Use Cases ────────────────────────────────────────────────────────────────


def get_create_customer_use_case(
    repository: CustomerRepository = Depends(get_customer_repository),
) -> CreateCustomerUseCase:
    """Dependency para obter CreateCustomerUseCase."""
    return CreateCustomerUseCase(repository)


def get_update_customer_use_case(
    repository: CustomerRepository = Depends(get_customer_repository),
) -> UpdateCustomerUseCase:
    """Dependency para obter UpdateCustomerUseCase."""
    return UpdateCustomerUseCase(repository)


def get_update_customer_address_use_case(
    repository: CustomerRepository = Depends(get_customer_repository),
) -> UpdateCustomerAddressUseCase:
    """Dependency para obter UpdateCustomerAddressUseCase."""
    return UpdateCustomerAddressUseCase(repository)


def get_customer_use_case(
    repository: CustomerRepository = Depends(get_customer_repository),
) -> GetCustomerUseCase:
    """Dependency para obter GetCustomerUseCase."""
    return GetCustomerUseCase(repository)


def get_list_customers_use_case(
    repository: CustomerRepository = Depends(get_customer_repository),
) -> ListCustomersUseCase:
    """Dependency para obter ListCustomersUseCase."""
    return ListCustomersUseCase(repository)


def get_activate_customer_use_case(
    repository: CustomerRepository = Depends(get_customer_repository),
) -> ActivateCustomerUseCase:
    """Dependency para obter ActivateCustomerUseCase."""
    return ActivateCustomerUseCase(repository)


def get_deactivate_customer_use_case(
    repository: CustomerRepository = Depends(get_customer_repository),
) -> DeactivateCustomerUseCase:
    """Dependency para obter DeactivateCustomerUseCase."""
    return DeactivateCustomerUseCase(repository)


def get_delete_customer_use_case(
    repository: CustomerRepository = Depends(get_customer_repository),
) -> DeleteCustomerUseCase:
    """Dependency para obter DeleteCustomerUseCase."""
    return DeleteCustomerUseCase(repository)
