from app.modules.customer.application.dtos.customer_dtos import (
    CustomerListOutputDTO,
    CustomerSummaryOutputDTO,
    ListCustomersInputDTO,
)
from app.modules.customer.domain.repositories.customer_repository import CustomerRepository


class ListCustomersUseCase:
    """
    Caso de uso: Listar clientes com filtros e paginação.

    Usa o read model CustomerSummary (query leve) em vez da entidade completa,
    pois listagens não precisam de VOs nem regras de negócio.

    Fluxo:
    1. Executa a query de listagem e contagem em paralelo
    2. Converte cada read model em DTO de saída
    3. Retorna resposta paginada
    """

    def __init__(self, repository: CustomerRepository):
        self._repository = repository

    async def execute(self, dto: ListCustomersInputDTO) -> CustomerListOutputDTO:
        # 1. Busca itens e total (ambos usam os mesmos filtros)
        summaries = await self._repository.list_summaries(
            is_active=dto.is_active,
            search=dto.search,
            limit=dto.limit,
            offset=dto.offset,
        )
        total = await self._repository.count(
            is_active=dto.is_active,
            search=dto.search,
        )

        # 2. Converte read models em DTOs
        items = [CustomerSummaryOutputDTO.from_read_model(s) for s in summaries]

        # 3. Retorna resposta paginada
        return CustomerListOutputDTO(
            items=items,
            total=total,
            limit=dto.limit,
            offset=dto.offset,
        )
