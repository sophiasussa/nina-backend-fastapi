import asyncio

from app.modules.auth.infrastructure.repositories import google_token_verifier_impl
from app.modules.auth.infrastructure.repositories.google_token_verifier_impl import (
    GoogleTokenVerifierImpl,
)


def test_google_verifier_checks_configured_client_id(monkeypatch):
    captured = {}

    async def fake_run_in_threadpool(function, *args):
        captured["function"] = function
        captured["args"] = args
        return {
            "email": "ana@example.com",
            "email_verified": True,
            "name": "Ana Maria",
        }

    monkeypatch.setattr(google_token_verifier_impl, "run_in_threadpool", fake_run_in_threadpool)
    result = asyncio.run(GoogleTokenVerifierImpl().verify("google-id-token"))

    assert result[0].value == "ana@example.com"
    assert result[1].value == "Ana Maria"
    assert captured["args"][0] == "google-id-token"
    assert captured["args"][2] == google_token_verifier_impl.settings.GOOGLE_CLIENT_ID
