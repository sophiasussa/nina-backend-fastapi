from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from domain.value_objects.user_id_vo import UserId
from domain.value_objects.name_vo import Name
from domain.value_objects.email_vo import Email
from domain.value_objects.password_vo import Password


@dataclass(frozen=True)
class UserEntity:
    """
    Entidade de domínio que representa um usuário do sistema.

    No contexto de DDD, esta classe é uma **Entidade** e atua como
    **Aggregate Root** do agregado de Usuário.

    Princípios aplicados:
    ---------------------
    - Imutabilidade: qualquer mudança gera uma nova instância
    - Consistência garantida por Value Objects
    - Nenhuma dependência de infraestrutura
    - Nenhuma lógica técnica (hash, banco, HTTP, etc)

    Invariantes do domínio:
    ----------------------
    - Usuário sempre possui ID, nome, email e senha válidos
    - Usuário desativado não pode alterar dados sensíveis
    """

    id: UserId
    nome: Name
    email: Email
    password: Password
    is_active: bool = True
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = None

    # ------------------------------------------------------------------
    # Comportamentos do domínio
    # ------------------------------------------------------------------

    def activate(self) -> "UserEntity":
        """
        Ativa o usuário.

        Retorna uma nova instância com o usuário ativo.
        """
        if self.is_active:
            return self

        return self._copy(
            is_active=True,
            updated_at=datetime.now(timezone.utc),
        )

    def deactivate(self) -> "UserEntity":
        """
        Desativa o usuário.

        Regra de negócio:
        - Um usuário já desativado não sofre alterações adicionais
        """
        if not self.is_active:
            return self

        return self._copy(
            is_active=False,
            updated_at=datetime.now(timezone.utc),
        )

    def change_name(self, new_name: Name) -> "UserEntity":
        """
        Altera o nome do usuário.

        Regra de negócio:
        - Usuários desativados não podem alterar o nome
        """
        self._ensure_active()

        return self._copy(
            nome=new_name,
            updated_at=datetime.now(timezone.utc),
        )

    def change_password(self, new_password: Password) -> "UserEntity":
        """
        Altera a senha do usuário.

        Regra de negócio:
        - Usuários desativados não podem alterar a senha
        """
        self._ensure_active()

        return self._copy(
            password=new_password,
            updated_at=datetime.now(timezone.utc),
        )

    def can_login(self) -> bool:
        """
        Indica se o usuário pode realizar login.
        """
        return self.is_active

    # ------------------------------------------------------------------
    # Métodos auxiliares internos (privados)
    # ------------------------------------------------------------------

    def _ensure_active(self) -> None:
        """
        Garante que o usuário esteja ativo antes de executar ações sensíveis.
        """
        if not self.is_active:
            raise ValueError("Usuário desativado não pode executar esta ação")

    def _copy(self, **changes) -> "UserEntity":
        """
        Cria uma nova instância da entidade aplicando alterações pontuais.

        Este método:
        - Evita duplicação de código
        - Mantém imutabilidade
        - Centraliza criação de novas instâncias
        """
        return UserEntity(
            id=changes.get("id", self.id),
            nome=changes.get("nome", self.nome),
            email=changes.get("email", self.email),
            password=changes.get("password", self.password),
            is_active=changes.get("is_active", self.is_active),
            created_at=self.created_at,
            updated_at=changes.get("updated_at", self.updated_at),
        )
