from app.modules.auth.application.dtos.registerinput_dto import (
    RegisterInputDTO,
    RegisterResultDTO,
)
from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.domain.value_objects import (
    UserId,
    Name,
    Email,
    Password,
)
from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
)
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


class RegisterUseCase:
    """
    Caso de uso: Registrar um novo usuário no sistema.

    Camada: Application

    Responsabilidades:
    ------------------
    - Orquestrar regras do domínio
    - Coordenar serviços técnicos (hash)
    - Criar a entidade UserEntity
    - Persistir o usuário

    Importante:
    -----------
    - Senha em texto plano **não entra no domínio**
    - Domínio recebe apenas senha já em hash
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def execute(self, input_dto: RegisterInputDTO) -> RegisterResultDTO:
        """
        Executa o fluxo de registro de usuário.

        Fluxo:
        ------
        1. Verifica se email já existe
        2. Gera hash da senha
        3. Cria entidade UserEntity
        4. Persiste usuário
        5. Retorna DTO de saída
        """

        # 1. Verifica duplicidade de email
        if await self._user_repository.exists_by_email(input_dto.email):
            raise UserAlreadyExistsException(input_dto.email.value)

        # 2. Gera hash da senha (infra)
        password_hash = self._password_hasher.hash(
            input_dto.password.value
        )

        # 3. Cria Password (VO definitivo do domínio)
        password = Password(password_hash)

        # 4. Cria entidade de domínio
        user = UserEntity(
            id=UserId.new(),
            nome=input_dto.nome,
            email=input_dto.email,
            password=password,
        )

        # 5. Persiste
        created_user = await self._user_repository.create(user)

        # 6. Retorna DTO de saída
        return created_user
