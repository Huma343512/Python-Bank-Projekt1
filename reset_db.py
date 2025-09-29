from db import SessionLocal
from sqlalchemy import text

def reset_database():
    session = SessionLocal()
    try:
        session.execute(text("""
            TRUNCATE TABLE 
                flagged_transactions,
                transactions,
                
                accounts,
                phones,
                addresses,
                customers
            RESTART IDENTITY CASCADE;
        """))
        session.commit()
        print(" Databasen är nollställd (tabeller kvar, data borta, id nollat).")
    except Exception as e:
        session.rollback()
        print(" Fel vid nollställning:", e)
    finally:
        session.close()

if __name__ == "__main__":
    reset_database()
