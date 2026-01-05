from app.modules.auth.domain.exceptions.auth_exceptions import UserNotFoundException
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.application.dtos.current_user_result_dto import (
    CurrentUserResultDTO
)
from app.modules.auth.domain.value_objects.user_id_vo import UserId


class GetCurrentUserUseCase:
    """
    Caso de uso: Obter o usuário atualmente autenticado.

    Papel na arquitetura:
    ---------------------
    - Camada: Application
    - Responsável por orquestrar a recuperação do usuário
    - Não conhece HTTP, JWT, FastAPI ou detalhes de autenticação

    Responsabilidades:
    ------------------
    - Converter o ID recebido em Value Object
    - Buscar o usuário no repositório
    - Garantir que o usuário exista
    - Retornar apenas os dados necessários via DTO

    Observações importantes:
    ------------------------
    - O ID chega como string (vindo do token ou camada de apresentação)
    - A validação semântica do ID ocorre no Value Object
    - A entidade de domínio NÃO é exposta diretamente
    """

    def __init__(self, user_repository: UserRepository):
        """
        Injeta as dependências necessárias ao caso de uso.

        Args:
            user_repository: Contrato de acesso aos dados do usuário
        """
        self._user_repository = user_repository

    async def execute(self, user_id: str) -> CurrentUserResultDTO:
        """
        Executa o fluxo para obter o usuário atual.

        Fluxo:
        ------
        1. Converte o ID primitivo em UserId (Value Object)
        2. Busca o usuário no repositório
        3. Valida a existência do usuário
        4. Retorna os dados através de um DTO de saída

        Args:
            user_id: ID do usuário (string vinda da camada de autenticação)

        Returns:
            CurrentUserResultDTO: Dados do usuário autenticado

        Raises:
            UserNotFoundException: Se o usuário não existir
            ValueError: Se o UserId for inválido
        """

        # 1. Converte para Value Object
        user_id_vo = UserId(user_id)

        # 2. Busca no repositório
        user = await self._user_repository.get_by_id(user_id_vo)

        # 3. Garante existência
        if not user:
            raise UserNotFoundException(user_id)

        # 4. Retorna DTO (não expõe entidade)
        return user
