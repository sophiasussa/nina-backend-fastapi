from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import uuid

from jose import JWTError, jwt

from app.core.config import settings
from app.core.constants import TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException

RESERVED_CLAIMS = {"sub", "exp", "iat", "type"}

class JWTHandler:
    """
    Classe responsável por criação e validação de tokens JWT.
    
    Tokens contêm:
    - sub: ID do usuário
    - type: tipo do token (access ou refresh)
    - exp: timestamp de expiração
    - iat: timestamp de criação
    """

    def __init__(self):
        self._secret_key = settings.SECRET_KEY
        self._algorithm = settings.ALGORITHM
        self._access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def _now(self) -> datetime:
        """Retorna datetime atual em UTC."""
        return datetime.now(timezone.utc)

    def create_access_token(
        self,
        user_id: str,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:

        """
        Cria token de acesso JWT.
        
        Args:
            user_id: ID do usuário
            additional_claims: Claims adicionais (opcional)
            
        Returns:
            str: Token JWT
        """
        expire = self._now() + timedelta(minutes=self._access_token_expire)
        
        claims = {
            "sub": user_id,
            "type": TOKEN_TYPE_ACCESS,
            "exp": expire,
            "iat": self._now(),
        }

        if additional_claims:
            # Evita sobrescrever claims reservados
            invalid = RESERVED_CLAIMS & additional_claims.keys()
            if invalid:
                raise ValueError(f"Claims reservados não podem ser sobrescritos: {invalid}")

            claims.update(additional_claims)

        return jwt.encode(claims, self._secret_key, algorithm=self._algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        expire = self._now() + timedelta(days=self._refresh_token_expire)

        payload = {
            "sub": user_id,
            "type": TOKEN_TYPE_REFRESH,
            "jti": str(uuid.uuid4()),
            "exp": expire,
            "iat": self._now(),
        }

        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(
        self,
        token: str,
        expected_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Decodifica e valida token JWT.

        Args:
            token: Token JWT
            expected_type: Tipo esperado do token (access ou refresh)

        Returns:
            Dict[str, Any]: Claims do token

        Raises:
            InvalidTokenException: Token inválido, expirado ou tipo incorreto
        """
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )
        except JWTError as e:
            raise InvalidTokenException(f"Token inválido: {str(e)}")

        token_type = payload.get("type")
        if expected_type and token_type != expected_type:
            raise InvalidTokenException(
                f"Tipo de token inválido. Esperado={expected_type}, recebido={token_type}"
            )

        return payload

    def get_user_id_from_token(self, token: str) -> str:
        """
        Extrai ID do usuário do token.
        
        Args:
            token: Token JWT
            
        Returns:
            str: ID do usuário
            
        Raises:
            InvalidTokenException: Token inválido
        """
        
        payload = self.decode_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise InvalidTokenException("Token não contém ID do usuário")

        return user_id
    
    def verify_token_type(self, token: str, expected_type: str) -> bool:
        """
        Verifica se token é do tipo esperado.
        
        Args:
            token: Token JWT
            expected_type: Tipo esperado (access ou refresh)
            
        Returns:
            bool: True se tipo corresponde
        """
        
        try:
            payload = self.decode_token(token)
            token_type = payload.get("type")
            return token_type == expected_type
        except InvalidTokenException:
            return False

    def get_token_expiration(self, token: str) -> datetime:
        """
        Retorna timestamp de expiração do token.
        
        Args:
            token: Token JWT
            
        Returns:
            datetime: Data/hora de expiração
            
        Raises:
            InvalidTokenException: Token inválido
        """
        payload = self.decode_token(token)
        exp = payload.get("exp")

        if not exp:
            raise InvalidTokenException("Token não contém expiração")

        if isinstance(exp, (int, float)):
            return datetime.fromtimestamp(exp, tz=timezone.utc)

        if isinstance(exp, datetime):
            return exp

        raise InvalidTokenException("Formato inválido de expiração no token")

    def is_token_expired(self, token: str) -> bool:
        """
        Verifica se token está expirado.
        
        Args:
            token: Token JWT
            
        Returns:
            bool: True se expirado
        """
        
        try:
            expiration = self.get_token_expiration(token)
            return self._now() > expiration
        except InvalidTokenException:
            return True
    
