from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.concurrency import run_in_threadpool

from app.modules.auth.application.services.google_token_verifier import GoogleTokenVerifier
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name


class GoogleTokenVerifierImpl(GoogleTokenVerifier):

    async def verify(self, token: str) -> tuple[Email, Name]:
        try:
            id_info = await run_in_threadpool(
                id_token.verify_oauth2_token,
                token,
                requests.Request(),
                # deixa SEM client_id por enquanto
                None,
            )


            if not id_info.get("email_verified"):
                raise ValueError("Email do Google não verificado")

            email = Email(id_info["email"])
            name = Name(id_info.get("name", "Usuário Google"))

            return email, name

        except Exception as e:
            print("GOOGLE TOKEN ERROR:", e)
            raise ValueError("Token do Google inválido")
