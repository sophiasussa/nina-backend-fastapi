from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.read_models.user_credentials import UserCredentials
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.password_vo import Password
from app.modules.auth.infrastructure.models.user_model import UserModel
from app.shared.domain.value_objects.id_vo import UserId



class UserRepositoryImpl(UserRepository):
    """
    Implementação concreta do UserRepository usando SQLAlchemy.
    
    Responsabilidades:
    - Converter entre UserEntity (domínio) e UserModel (ORM)
    - Executar operações no banco de dados
    - Tratar erros de persistência
    """

    def __init__(self, db: Session):
        self._db = db

    async def create(self, user: UserEntity) -> UserEntity:
        """
        Cria um novo usuário no banco.
        
        Args:
            user: Entidade do usuário
            
        Returns:
            UserEntity: Entidade do usuário criado
        """
        # Converte entidade para model
        model = UserModel.from_entity(user)

        # Persiste no banco
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)

        # Converte model para entidade
        return model.to_entity()

    async def get_by_id(self, user_id: UserId) -> Optional[UserEntity]:
        """
        Busca usuário por ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Optional[UserEntity]: Entidade do usuário ou None
        """
        stmt = select(UserModel).where(UserModel.id == user_id.value)
        model = self._db.execute(stmt).scalar_one_or_none()

        return model.to_entity() if model else None

    async def get_by_email(self, email: Email) -> Optional[UserEntity]:
        """
        Busca usuário por email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Optional[UserEntity]: Entidade do usuário ou None
        """
        stmt = select(UserModel).where(UserModel.email == email.value)
        model = self._db.execute(stmt).scalar_one_or_none()

        return model.to_entity() if model else None

    async def exists_by_email(self, email: Email) -> bool:
        """
        Verifica se email já existe.
        
        Args:
            email: Email a verificar
            
        Returns:
            bool: True se email existe
        """
        stmt = select(UserModel.id).where(UserModel.email == email.value)
        return self._db.execute(stmt).scalar_one_or_none() is not None

    async def get_credentials_by_email(
        self,
        email: Email,
    ) -> Optional[UserCredentials]:

        stmt = select(
            UserModel.id,
            UserModel.password,
            UserModel.is_active,
        ).where(UserModel.email == email.value)

        row = self._db.execute(stmt).first()

        if not row:
            return None

        return UserCredentials(
            user_id=UserId(row.id),
            password_hash=row.password,
            is_active=row.is_active,
        )

    async def update(self, user: UserEntity) -> UserEntity:
        """
        Atualiza dados do usuário.
        
        Args:
            user: Entidade com dados atualizados
            
        Returns:
            UserEntity: Entidade atualizada
        """
        
        stmt = select(UserModel).where(UserModel.id == user.id.value)
        result = self._db.execute(stmt)
        user_model = result.scalar_one_or_none()
        
        if not user_model:
            raise ValueError(f"Usuário {user.id} não encontrado")
        
        # Atualiza campos
        user_model.nome = user.nome.value
        user_model.email = user.email.value
        user_model.is_active = user.is_active
        
        self._db.commit()
        self._db.refresh(user_model)
        
        return user_model.to_entity()
    
    async def delete(self, user_id: UserId) -> bool:
        """
        Remove usuário do banco.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            bool: True se removido com sucesso
        """
        
        stmt = select(UserModel).where(UserModel.id == user_id.value)
        result = self._db.execute(stmt)
        user_model = result.scalar_one_or_none()
        
        if not user_model:
            return False
        
        self._db.delete(user_model)
        self._db.commit()
        
        return True

    async def update_password(self, user_id: UserId, password: Password) -> None:
        stmt = select(UserModel).where(UserModel.id == user_id.value)
        user_model = self._db.execute(stmt).scalar_one_or_none()

        if not user_model:
            raise ValueError("Usuário não encontrado")

        user_model.password = password.value
        self._db.commit()
