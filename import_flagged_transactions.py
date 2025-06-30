import pandas as pd
from db import SessionLocal
from models import FlaggedTransaction, Transaction

csv_path = "data/clean/flagged_transactions.csv"

# Läs in CSV
df = pd.read_csv(csv_path)

session = SessionLocal()

try:
    count_imported = 0
    count_skipped = 0

    for _, row in df.iterrows():
        transaction_id = row["transaction_id"]

        # Kontrollera om transaktionen finns i databasen
        transaction = session.query(Transaction).filter_by(id=transaction_id).first()
        if not transaction:
            print(f"❗ Hoppar över: Transaktion ID {transaction_id} finns inte i databasen.")
            count_skipped += 1
            continue

        # Skapa och lägg till flagged transaction
        flagged = FlaggedTransaction(
            transaction_id=transaction_id,
            reason=row["reason"],
            flagged_date=pd.to_datetime(row["flagged_date"]).date(),
            amount=row["amount"]
        )
        session.add(flagged)
        count_imported += 1

    session.commit()
    print(f" Import klar: {count_imported} markerade transaktioner importerade, {count_skipped} hoppades över.")

except Exception as e:
    print(" Fel under import, rullar tillbaka. Fel:", e)
    session.rollback()
finally:
    session.close()




