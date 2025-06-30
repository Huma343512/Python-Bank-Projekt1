import pandas as pd
import os
from datetime import datetime

def create_clean_dir():
    os.makedirs("data/clean", exist_ok=True)

def load_customers(path="data/sebank_customers_with_accounts.csv"):
    return pd.read_csv(path)

def clean_customers(customers_df):
    print(f"Totalt kunder innan validering: {len(customers_df)}")
    customers_df = customers_df.dropna(subset=["Customer", "BankAccount"])
    print(f"Efter dropna på Customer och BankAccount: {len(customers_df)}")

    phone_pattern = r"^\+?[\d\s\-]{7,15}$"
    customers_df = customers_df[customers_df["Phone"].str.contains(phone_pattern, na=False)]
    print(f"Efter telefonfilter: {len(customers_df)}")

    personnummer_pattern = r"^\d{6}[-+]?\d{4}$"
    customers_df = customers_df[customers_df["Personnummer"].str.contains(personnummer_pattern, na=False)]
    print(f"Efter personnummerfilter: {len(customers_df)}")

    customers_df = customers_df.drop_duplicates(subset="BankAccount")
    print(f"Efter drop_duplicates på BankAccount: {len(customers_df)}")

    return customers_df

def save_customers(customers_df, path="data/clean/customers_clean.csv"):
    customers_df.to_csv(path, index=False)
    print(f"Kunddata sparad i {path}\n")

def load_transactions(path="data/transactions.csv"):
    return pd.read_csv(path)

def clean_transactions(transactions_df):
    transactions_df["notes"] = transactions_df["notes"].fillna("ingen kommentar")
    transactions_df["timestamp"] = pd.to_datetime(transactions_df["timestamp"], errors='coerce')

    print(f"Totalt transaktioner innan validering: {len(transactions_df)}")
    transactions_df = transactions_df[transactions_df["amount"] >= 0.01]
    print(f"Efter filter på amount >= 0.01: {len(transactions_df)}")

    transactions_df = transactions_df[transactions_df["currency"].str.match(r"^[A-Z]{3}$", na=False)]
    print(f"Efter valutafilter: {len(transactions_df)}")

    transactions_df = transactions_df.dropna(subset=["notes"])
    print(f"Efter dropna på notes: {len(transactions_df)}")

    transactions_df = transactions_df.drop_duplicates(subset="transaction_id")
    print(f"Efter drop_duplicates på transaction_id: {len(transactions_df)}")

    return transactions_df

def save_transactions(transactions_df, path="data/clean/transactions_clean.csv"):
    transactions_df.to_csv(path, index=False)
    print(f"Transaktionsdata sparad i {path}\n")

def flag_suspected_transactions(transactions_df):
    flagged = []

    # 1. Samma konto som avsändare och mottagare
    samma_konto = transactions_df[transactions_df["sender_account"] == transactions_df["receiver_account"]]
    for _, row in samma_konto.iterrows():
        flagged.append({
            "transaction_id": row["transaction_id"],
            "reason": "Samma konto som avsändare och mottagare",
            "flagged_date": datetime.today().strftime("%Y-%m-%d"),
            "amount": row["amount"]
        })

    # 2. Högt belopp
    for _, row in transactions_df[transactions_df["amount"] > 100_000].iterrows():
        flagged.append({
            "transaction_id": row["transaction_id"],
            "reason": "Belopp över 100 000 SEK",
            "flagged_date": datetime.today().strftime("%Y-%m-%d"),
            "amount": row["amount"]
        })

    # 3. Negativt belopp (ska inte finnas kvar, men dubbelkolla)
    for _, row in transactions_df[transactions_df["amount"] < 0].iterrows():
        flagged.append({
            "transaction_id": row["transaction_id"],
            "reason": "Negativt belopp",
            "flagged_date": datetime.today().strftime("%Y-%m-%d"),
            "amount": row["amount"]
        })

    # 4. Flera transaktioner från samma konto inom 1 minut
    tx = transactions_df.sort_values(by=["sender_account", "timestamp"])
    for account, group in tx.groupby("sender_account"):
        timestamps = group["timestamp"].tolist()
        for i in range(len(timestamps) - 3):
            if (timestamps[i + 3] - timestamps[i]).total_seconds() <= 60:
                match = group.iloc[i:i+4]
                for _, row in match.iterrows():
                    flagged.append({
                        "transaction_id": row["transaction_id"],
                        "reason": "Flera transaktioner inom 1 minut",
                        "flagged_date": datetime.today().strftime("%Y-%m-%d"),
                        "amount": row["amount"]
                    })

    flagged_df = pd.DataFrame(flagged).drop_duplicates(subset=["transaction_id", "reason"])
    return flagged_df

def save_flagged(flagged_df, path="data/clean/flagged_transactions.csv"):
    flagged_df.to_csv(path, index=False)
    print(f"Flaggade transaktioner sparade i {path}\n")

def run_validation():
    create_clean_dir()

    customers_df = load_customers()
    customers_clean = clean_customers(customers_df)
    save_customers(customers_clean)

    transactions_df = load_transactions()
    transactions_clean = clean_transactions(transactions_df)
    save_transactions(transactions_clean)

    flagged_df = flag_suspected_transactions(transactions_clean)
    save_flagged(flagged_df)

    print("Klart! Validering och flaggning klar.")

if __name__ == "__main__":
    run_validation()

