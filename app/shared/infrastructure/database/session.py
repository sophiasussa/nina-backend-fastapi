from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings


# Cria engine do SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_size=10,        # Tamanho do pool de conexões
    max_overflow=20,     # Máximo de conexões extras
)

# Cria session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency do FastAPI para obter sessão do banco.
    
    Uso:
```python
    @router.get("/users")
    def get_users(db: Session = Depends(get_db)):
        ...
```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa o banco de dados.
    Cria todas as tabelas definidas nos models.
    """
    from app.shared.infrastructure.database.base import Base
    
    # Importar todos os models aqui para que sejam registrados
    from app.modules.auth.infrastructure.models.user_model import UserModel
    
    Base.metadata.create_all(bind=engine)
