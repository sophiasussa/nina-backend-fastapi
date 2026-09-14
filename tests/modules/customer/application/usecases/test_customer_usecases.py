import asyncio
import unittest

from app.modules.customer.application.dtos.customer_dtos import (
    CreateCustomerInputDTO,
    UpdateCustomerInputDTO,
)
from app.modules.customer.application.usecases.create_customer_usecase import (
    CreateCustomerUseCase,
)
from app.modules.customer.application.usecases.toggle_customer_status_usecase import (
    DeactivateCustomerUseCase,
)
from app.modules.customer.application.usecases.update_customer_usecase import (
    UpdateCustomerUseCase,
)
from app.modules.customer.domain.exceptions.customers_exceptions import (
    CustomerStatusError,
    CustomerValidationError,
)


class InMemoryCustomerRepository:
    def __init__(self):
        self.customers = {}

    async def create(self, customer):
        self.customers[customer.id.value] = customer
        return customer

    async def get_by_id(self, customer_id):
        return self.customers.get(customer_id.value)

    async def exists_by_email(self, email):
        return any(item.email.value == email.value for item in self.customers.values())

    async def exists_by_document(self, document):
        return any(
            item.document and item.document.value == document.value
            for item in self.customers.values()
        )

    async def update(self, customer):
        self.customers[customer.id.value] = customer
        return customer


class CustomerUseCaseTests(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryCustomerRepository()

    def execute(self, coroutine):
        return asyncio.run(coroutine)

    def create_customer(self):
        return self.execute(
            CreateCustomerUseCase(self.repository).execute(
                CreateCustomerInputDTO(
                    name=" Maria Silva ",
                    email="MARIA@EXAMPLE.COM",
                    phone="(11) 99999-9999",
                    notes="Prefer gluten-free products",
                )
            )
        )

    def test_create_normalizes_contact_data(self):
        result = self.create_customer()

        self.assertEqual(result.name, "Maria Silva")
        self.assertEqual(result.email, "maria@example.com")
        self.assertEqual(result.phone, "11999999999")
        self.assertTrue(result.is_active)

    def test_update_can_explicitly_clear_phone_and_notes(self):
        created = self.create_customer()

        result = self.execute(
            UpdateCustomerUseCase(self.repository).execute(
                created.customer_id,
                UpdateCustomerInputDTO(phone=None, notes=None),
            )
        )

        self.assertIsNone(result.phone)
        self.assertIsNone(result.notes)

    def test_invalid_customer_id_is_a_domain_validation_error(self):
        with self.assertRaises(CustomerValidationError):
            self.execute(
                UpdateCustomerUseCase(self.repository).execute(
                    "not-a-uuid", UpdateCustomerInputDTO(name="Ana")
                )
            )

    def test_deactivating_an_inactive_customer_returns_domain_error(self):
        created = self.create_customer()
        use_case = DeactivateCustomerUseCase(self.repository)
        self.execute(use_case.execute(created.customer_id))

        with self.assertRaises(CustomerStatusError):
            self.execute(use_case.execute(created.customer_id))
