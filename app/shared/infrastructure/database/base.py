from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True  # não vira tabela
    """
    Classe base para todos os models SQLAlchemy.
    
    Fornece campos comuns:
    - id: UUID único
    - created_at: timestamp de criação
    - updated_at: timestamp de última atualização
    """
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )
