class AuthException(Exception):
    """
    Exceção base do domínio de autenticação.

    No contexto de DDD, esta classe representa a raiz de todas
    as exceções relacionadas ao domínio de autenticação.

    Características:
    -----------------
    - Herda de Exception
    - Não depende de frameworks (FastAPI, HTTP, etc)
    - Deve ser usada apenas dentro do domínio e aplicação

    Objetivo:
    ---------
    - Permitir que a camada de aplicação trate erros de autenticação
      de forma consistente
    - Evitar o uso de exceções genéricas (Exception, ValueError)
      para regras de negócio
    """
    pass


class InvalidCredentialsException(AuthException):
    """
    Exceção lançada quando as credenciais informadas são inválidas.

    Cenários comuns:
    ----------------
    - Email não encontrado
    - Senha incorreta
    - Combinação email/senha inválida

    Observações:
    ------------
    - Não revela qual campo está errado (boa prática de segurança)
    - Usada principalmente no caso de uso de login
    """

    def __init__(self):
        super().__init__("Email ou senha incorretos")


class UserAlreadyExistsException(AuthException):
    """
    Exceção lançada ao tentar registrar um usuário que já existe.

    Regra de negócio:
    -----------------
    - Não pode existir mais de um usuário com o mesmo email

    Geralmente lançada quando:
    --------------------------
    - O email já está cadastrado no sistema
    """

    def __init__(self, email: str):
        super().__init__(f"Usuário com email '{email}' já existe")


class UserNotFoundException(AuthException):
    """
    Exceção lançada quando um usuário não é encontrado.

    Pode ocorrer em operações como:
    -------------------------------
    - Login
    - Busca de perfil
    - Atualização de dados
    - Remoção de usuário

    O identificador pode ser:
    -------------------------
    - ID do usuário
    - Email
    - Qualquer identificador único do domínio
    """

    def __init__(self, identifier: str):
        super().__init__(f"Usuário '{identifier}' não encontrado")


class InactiveUserException(AuthException):
    """
    Exceção lançada quando um usuário inativo tenta realizar
    uma ação que exige conta ativa.

    Exemplo de regra de negócio:
    ----------------------------
    - Usuários inativos não podem fazer login
    - Usuários inativos não podem alterar dados
    """

    def __init__(self):
        super().__init__("Usuário inativo")


class InvalidTokenException(AuthException):
    """
    Exceção lançada quando um token de autenticação é inválido.

    Pode representar:
    -----------------
    - Token malformado
    - Token expirado
    - Token assinado incorretamente
    - Token revogado

    Usada normalmente em:
    ---------------------
    - Middleware de autenticação
    - Casos de uso que dependem de token válido
    """

    def __init__(self):
        super().__init__("Token inválido ou expirado")
