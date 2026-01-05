from app.modules.auth.application.dtos.logininput_dto import LoginInputDTO
from app.modules.auth.application.dtos.loginresult_dto import LoginResultDTO
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
    InactiveUserException,
)
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


class LoginUseCase:
    """
    Caso de uso: Autenticar usuário.
    
    Responsabilidades:
    - Validar credenciais
    - Verificar status do usuário
    - Retornar entidade do usuário autenticado
    
    NÃO gera tokens JWT - isso é responsabilidade da camada de apresentação.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
    
    async def execute(self, input_dto: LoginInputDTO) -> LoginResultDTO:
        """
        Executa o caso de uso de login.
        
        Args:
            email: Email do usuário
            senha: Senha em texto plano
            
        Returns:
            UserEntity: Entidade do usuário autenticado
            
        Raises:
            InvalidCredentialsException: Credenciais inválidas
            InactiveUserException: Usuário inativo
            UserNotFoundException: Usuário não encontrado
        """                
        credentials = await self._user_repository.get_credentials_by_email(
            input_dto.email
        )

        if not credentials:
            raise UserNotFoundException(input_dto.email.value)

        if not self._password_hasher.verify(
            input_dto.password.value,
            credentials.password_hash,
        ):
            raise InvalidCredentialsException()

        if not credentials.is_active:
            raise InactiveUserException()

        user = await self._user_repository.get_by_id(credentials.user_id)

        return LoginResultDTO(
            user_id=user.id,
            nome=user.nome,
            email=user.email,
            is_active=user.is_active,
        )
