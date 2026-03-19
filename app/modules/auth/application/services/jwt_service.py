from abc import ABC, abstractmethod


class JwtService(ABC):

    @abstractmethod
    def create_access_token(self, subject: str) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, subject: str) -> str:
        pass
