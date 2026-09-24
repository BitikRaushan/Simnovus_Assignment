import pytest
from fastapi.testclient import TestClient

from app.database import Base
from app.main import app
from app.database import engine

@pytest.fixture()
def client():
    # Tests use the configured database. For the assignment's normal run,
    # this is PostgreSQL. Clean the table between tests.
    Base.metadata.create_all(bind=engine)

    from app.database import SessionLocal
    db = SessionLocal()
    db.execute(__import__("sqlalchemy").text("DELETE FROM devices"))
    db.commit()
    db.close()

    with TestClient(app) as test_client:
        yield test_client
