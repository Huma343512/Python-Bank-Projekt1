import pandas as pd
from db import SessionLocal
from models import Customer, Address, Phone, Account

# FIX: korrekt sätt att läsa in CSV och skapa session
df = pd.read_csv("data/clean/customers_clean.csv")
session = SessionLocal()

try:
    for _, row in df.iterrows():
        existing_customer = session.query(Customer).filter_by(personnummer=row["Personnummer"]).first()
        if existing_customer:
            print(f"❗ Personnummer {row['Personnummer']} finns redan, hoppar över.")
            continue

        customer = Customer(
            customer=row["Customer"],
            personnummer=row["Personnummer"]
        )
        session.add(customer)
        session.flush()

        address = Address(
            customer_id=customer.id,
            address=row["Address"],
            is_active=True
        )
        session.add(address)

        phone = Phone(
            customer_id=customer.id,
            phone=row["Phone"],
            is_active=True
        )
        session.add(phone)

        account = Account(
            customer_id=customer.id,
            account_number=row["BankAccount"],
            balance=0.0
        )
        session.add(account)

    session.commit()
    print("Kunddata importerades (eller hoppades över) korrekt.")
except Exception as e:
    print("Fel vid import:", e)
    session.rollback()
finally:
    session.close()

