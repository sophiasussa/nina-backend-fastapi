from app.modules.auth.application.services.jwt_service import JwtService
from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler


class JwtServiceImpl(JwtService):
    def __init__(self, jwt_handler: JWTHandler):
        self.jwt_handler = jwt_handler

    def create_access_token(self, subject: str) -> str:
        return self.jwt_handler.create_access_token(subject)

    def create_refresh_token(self, subject: str) -> str:
        return self.jwt_handler.create_refresh_token(subject)
