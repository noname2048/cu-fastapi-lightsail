import pytest


@pytest.fixture(scope="session", autouse=True)
def create_model():
    from app.config import settings

    if settings.backend_env == "ci":
        from app.database import Base, engine

        Base.metadata.create_all(bind=engine)
