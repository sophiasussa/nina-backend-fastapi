import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.modules.auth.domain.value_objects.password_vo import Password
from app.modules.auth.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.shared.domain.value_objects.id_vo import UserId
from app.shared.infrastructure.database.base_orm import Base


def test_sqlalchemy_user_repository_persists_and_updates_auth_data():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            repository = UserRepositoryImpl(session)
            user = UserEntity(
                id=UserId.new(),
                nome=Name("Ana Maria"),
                email=Email("ANA@example.com"),
                password=Password("stored-hash-value-" + "x" * 40),
            )

            created = asyncio.run(repository.create(user))
            by_email = asyncio.run(repository.get_by_email(Email("ana@example.com")))
            credentials = asyncio.run(
                repository.get_credentials_by_email(Email("ana@example.com"))
            )

            assert created.id == user.id
            assert by_email.nome.value == "Ana Maria"
            assert credentials.user_id == user.id
            assert credentials.password_hash == user.password.value
            assert credentials.is_active is True
            assert asyncio.run(repository.exists_by_email(Email("ana@example.com")))

            changed_password = Password("updated-hash-value-" + "y" * 40)
            asyncio.run(repository.update_password(user.id, changed_password))
            assert (
                asyncio.run(repository.get_by_id(user.id)).password.value
                == changed_password.value
            )

            renamed = by_email.change_name(Name("Maria Silva"))
            updated = asyncio.run(repository.update(renamed))
            assert updated.nome.value == "Maria Silva"
            assert updated.password.value == changed_password.value

            assert asyncio.run(repository.delete(user.id)) is True
            assert asyncio.run(repository.get_by_id(user.id)) is None
            assert asyncio.run(repository.delete(user.id)) is False
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()
