import pytest
import pandas as pd
import validation  # importera din valideringsmodul


@pytest.fixture
def customers_raw():
    # Läser in rådata för kunder
    return validation.load_customers("data/sebank_customers_with_accounts.csv")


@pytest.fixture
def transactions_raw():
    # Läser in rådata för transaktioner
    return validation.load_transactions("data/transactions.csv")


def test_clean_customers(customers_raw):
    cleaned = validation.clean_customers(customers_raw)


    assert isinstance(cleaned, pd.DataFrame)
    assert not cleaned["Customer"].isnull().any()
    assert not cleaned["BankAccount"].isnull().any()
    assert cleaned["Phone"].str.match(r"^\+?[\d\s\-]{7,15}$").all()
    assert cleaned["Personnummer"].str.match(r"^\d{6}[-+]?\d{4}$").all()
    assert cleaned["BankAccount"].is_unique


def test_clean_transactions(transactions_raw):
    cleaned = validation.clean_transactions(transactions_raw)

    assert isinstance(cleaned, pd.DataFrame)
    assert (cleaned["amount"] >= 0.01).all()
    assert cleaned["currency"].str.match(r"^[A-Z]{3}$").all()
    assert not cleaned["notes"].isnull().any()
    assert cleaned["transaction_id"].is_unique


def test_flag_suspected_transactions(transactions_raw):
    cleaned = validation.clean_transactions(transactions_raw)
    flagged = validation.flag_suspected_transactions(cleaned)

    assert isinstance(flagged, pd.DataFrame)
    # Flagged transactions måste ha kolumnerna 'transaction_id', 'reason', 'flagged_date', 'amount'
    for col in ["transaction_id", "reason", "flagged_date", "amount"]:
        assert col in flagged.columns
    # Optional: kontrollera att flaggade är subset av transaktioner
    assert set(flagged["transaction_id"]).issubset(set(cleaned["transaction_id"]))




