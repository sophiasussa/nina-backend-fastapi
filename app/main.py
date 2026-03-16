from fastapi import FastAPI
from app.modules.auth.presentation.routes.auth_routes import router as example_router

app = FastAPI(
    title="Example API",
    version="0.1.0",
)

app.include_router(example_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
