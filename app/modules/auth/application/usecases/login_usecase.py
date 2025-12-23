from typing import Tuple

from app.modules.auth.application.dtos.login_dto import LoginInputDTO
from app.modules.auth.application.dtos.login_result_dto import LoginResultDTO
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
        try:
            email_vo = Email(input_dto.email)
        except ValueError:
            raise InvalidCredentialsException()
        
        user = await self._user_repository.get_by_email(email_vo)

        if not user:
            raise UserNotFoundException(email_vo.value)

        password_hash = user.password.hashed

        if not self._password_hasher.verify(input_dto.password, password_hash):
            raise InvalidCredentialsException()

        if not user.can_login():
            raise InactiveUserException()

        return LoginResultDTO(
            user_id=user.id,
            nome=user.nome,
            email=user.email,
            is_active=user.is_active,
        )
