from abc import ABC, abstractmethod
from datetime import datetime


class SessionRepository(ABC):

    @abstractmethod
    def blacklist_access_token(self, token: str, expires_at: datetime) -> None:
        pass

    @abstractmethod
    def is_access_token_blacklisted(self, token: str) -> bool:
        pass

    @abstractmethod
    def store_refresh_token(self, jti: str, user_id: str, ttl_seconds: int) -> None:
        pass

    @abstractmethod
    def revoke_refresh_token(self, jti: str, user_id: str) -> None:
        pass

    @abstractmethod
    def is_refresh_token_valid(self, jti: str) -> bool:
        pass

    @abstractmethod
    def get_user_sessions(self, user_id: str):
        pass

    @abstractmethod
    def revoke_all_sessions(self, user_id: str) -> None:
        pass

    @abstractmethod
    def is_refresh_token_used(self, jti: str) -> bool:
        pass

    @abstractmethod
    def mark_refresh_token_used(self, jti: str, ttl_seconds: int) -> None:
        pass
