from db import SessionLocal
from sqlalchemy import text

def test_database_connection():
    session = None
    try:
        session = SessionLocal()
        result = session.execute(text("SELECT 1"))  # FIX: använd text()
        assert result.scalar() == 1
    finally:
        if session:
            session.close()

