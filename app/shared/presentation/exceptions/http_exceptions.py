from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """Classe base para exceções HTTP customizadas."""
    
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=self.status_code,
            detail=detail or self.default_detail
        )


class BadRequestException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad Request"


class UnauthorizedException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Unauthorized"


class ForbiddenException(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Forbidden"


class NotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not Found"


class ConflictException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict"


class InternalServerException(BaseHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Internal Server Error"
