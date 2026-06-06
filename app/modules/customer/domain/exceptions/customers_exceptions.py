class CustomerDomainError(Exception):
    """Erro base para o domínio de clientes."""
    pass


class CustomerNotFoundError(CustomerDomainError):
    """Levantado quando o cliente não é encontrado."""

    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Cliente não encontrado: '{identifier}'.")


class CustomerAlreadyExistsError(CustomerDomainError):
    """Levantado quando há tentativa de criar cliente com e-mail já existente."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Já existe um cliente cadastrado com o e-mail '{email}'.")


class CustomerDocumentAlreadyExistsError(CustomerDomainError):
    """Levantado quando há tentativa de cadastrar CPF já registrado."""

    def __init__(self, document: str):
        self.document = document
        super().__init__(f"Já existe um cliente cadastrado com o CPF '{document}'.")


class CustomerInactiveError(CustomerDomainError):
    """Levantado quando uma operação é tentada em cliente inativo."""

    def __init__(self, customer_id: str):
        self.customer_id = customer_id
        super().__init__(
            f"O cliente '{customer_id}' está inativo e não pode realizar esta operação."
        )


class CustomerValidationError(CustomerDomainError):
    """Levantado quando dados do cliente não passam na validação de domínio."""

    def __init__(self, field: str, reason: str):
        self.field = field
        self.reason = reason
        super().__init__(f"Dado inválido no campo '{field}': {reason}")
