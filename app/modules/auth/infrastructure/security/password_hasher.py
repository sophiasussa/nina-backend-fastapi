from passlib.context import CryptContext

from app.core.config import settings


class PasswordHasher:
    """
    Classe responsável por hash e verificação de senhas.
    
    Utiliza bcrypt através da biblioteca passlib.
    """
    
    def __init__(self):
        self._pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=settings.BCRYPT_ROUNDS,
        )
    
    def hash(self, password: str) -> str:
        """
        Gera hash da senha.
        
        Args:
            password: Senha em texto plano
            
        Returns:
            str: Hash da senha
        """
        return self._pwd_context.hash(password)
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se senha corresponde ao hash.
        
        Args:
            plain_password: Senha em texto plano
            hashed_password: Hash armazenado
            
        Returns:
            bool: True se senha é válida
        """
        return self._pwd_context.verify(plain_password, hashed_password)
    
    def needs_rehash(self, hashed_password: str) -> bool:
        """
        Verifica se hash precisa ser atualizado.
        
        Útil quando mudamos configurações de segurança.
        
        Args:
            hashed_password: Hash armazenado
            
        Returns:
            bool: True se precisa ser rehashed
        """
        return self._pwd_context.needs_update(hashed_password)
