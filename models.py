from sqlalchemy import Column, String, Integer, Float, Date, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    customer = Column(String, nullable=False)  # Från CSV: Customer
    personnummer = Column(String, unique=True, nullable=False)

    addresses = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    phones = relationship("Phone", back_populates="customer", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="customer", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    address = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    customer = relationship("Customer", back_populates="addresses")


class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    phone = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    customer = relationship("Customer", back_populates="phones")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    account_number = Column(String, unique=True, nullable=False)  # Från CSV: BankAccount
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    balance = Column(Float, default=0.0)

    customer = relationship("Customer", back_populates="accounts")

    transactions_sent = relationship(
        "Transaction",
        back_populates="sender_account",
        foreign_keys="Transaction.sender_account_id"
    )
    transactions_received = relationship(
        "Transaction",
        back_populates="receiver_account",
        foreign_keys="Transaction.receiver_account_id"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True)  # Från CSV: transaction_id
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    notes = Column(String)

    sender_account_id = Column(Integer, ForeignKey("accounts.id"))
    receiver_account_id = Column(Integer, ForeignKey("accounts.id"))

    sender_account = relationship(
        "Account",
        back_populates="transactions_sent",
        foreign_keys=[sender_account_id]
    )
    receiver_account = relationship(
        "Account",
        back_populates="transactions_received",
        foreign_keys=[receiver_account_id]
    )

    sender_country = Column(String)
    sender_municipality = Column(String)
    receiver_country = Column(String)
    receiver_municipality = Column(String)
    transaction_type = Column(String)


class FlaggedTransaction(Base):
    __tablename__ = "flagged_transactions"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, ForeignKey("transactions.id"), nullable=False)
    reason = Column(String, nullable=False)
    flagged_date = Column(Date, default=func.current_date())
    amount = Column(Float)

    transaction = relationship("Transaction")



