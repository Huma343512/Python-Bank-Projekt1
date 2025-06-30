import pandas as pd
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from models import Transaction, Account

# Läs in CSV-filen
df = pd.read_csv("data/clean/transactions_clean.csv")

# Rensa och förenkla kolumnnamn
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

session = SessionLocal()

try:
    for _, row in df.iterrows():
        # Kontrollera att avsändare och mottagare finns
        sender = session.query(Account).filter_by(account_number=row["sender_account"]).first()
        receiver = session.query(Account).filter_by(account_number=row["receiver_account"]).first()

        if not sender or not receiver:
            print(f"❗ Hoppar över: konto saknas för transaktion {row['transaction_id']}")
            continue

        # Kontrollera om transaktionen redan finns
        existing = session.query(Transaction).filter_by(id=row["transaction_id"]).first()
        if existing:
            print(f"❗ Transaktion {row['transaction_id']} finns redan, hoppar över.")
            continue

        transaction = Transaction(
            id=row["transaction_id"],
            amount=row["amount"],
            currency=row["currency"],
            notes=row.get("notes", None),
            sender_account_id=sender.id,
            receiver_account_id=receiver.id,
            sender_country=row.get("sender_country"),
            sender_municipality=row.get("sender_municipality"),
            receiver_country=row.get("receiver_country"),
            receiver_municipality=row.get("receiver_municipality"),
            transaction_type=row.get("transaction_type")
        )

        session.add(transaction)

    session.commit()
    print(" Transaktioner importerades korrekt.")

except IntegrityError as e:
    print(" Fel vid import (integritet), rullar tillbaka:", e)
    session.rollback()

except Exception as e:
    print(" Fel vid import, rullar tillbaka:", e)
    session.rollback()

finally:
    session.close()


