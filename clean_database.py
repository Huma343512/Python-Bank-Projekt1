from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, Address, Phone, Account, Transaction, FlaggedTransaction  # Anpassa import enligt ditt projekt

engine = create_engine("postgresql://postgres:Root@host:5432/bankdb1")

Session = sessionmaker(bind=engine)
session = Session()

try:
    # Radera data i rätt ordning pga. FK-beroenden
    session.query(FlaggedTransaction).delete(synchronize_session=False)
    session.query(Transaction).delete(synchronize_session=False)
    session.query(Account).delete(synchronize_session=False)
    session.query(Phone).delete(synchronize_session=False)
    session.query(Address).delete(synchronize_session=False)
    session.query(Customer).delete(synchronize_session=False)

    session.commit()
    print("All data raderad utan att påverka tabellstrukturen.")
except Exception as e:
    session.rollback()
    print(f"Fel vid radering: {e}")
finally:
    session.close()

