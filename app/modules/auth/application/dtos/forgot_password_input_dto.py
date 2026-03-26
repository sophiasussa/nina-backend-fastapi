from app.modules.auth.domain.value_objects.email_vo import Email


class ForgotPasswordInputDTO:
    def __init__(self, email: str):
        self.email = Email(email)
