"""
Constantes globais da aplicação.
"""

# HTTP Status Messages
HTTP_200_OK = "Success"
HTTP_201_CREATED = "Created"
HTTP_400_BAD_REQUEST = "Bad Request"
HTTP_401_UNAUTHORIZED = "Unauthorized"
HTTP_403_FORBIDDEN = "Forbidden"
HTTP_404_NOT_FOUND = "Not Found"
HTTP_409_CONFLICT = "Conflict"
HTTP_500_INTERNAL_ERROR = "Internal Server Error"

# Token Types
TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

# User Status
USER_ACTIVE = True
USER_INACTIVE = False

# Regex Patterns
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PASSWORD_MIN_LENGTH = 6
