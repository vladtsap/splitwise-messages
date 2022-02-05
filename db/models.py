from sqlalchemy import Column, Integer, String

from config import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, nullable=True)
    bank_id = Column(String)
    message_id = Column(Integer, index=True)
    chat_id = Column(Integer, index=True)
    time = Column(Integer)
    description = Column(String)
    comment = Column(String, nullable=True)
    mcc = Column(Integer)
    original_mcc = Column(Integer)
    amount = Column(Integer)
    operation_amount = Column(Integer)
    currency_code = Column(Integer)
    commission_rate = Column(Integer)
    cashback_amount = Column(Integer)
    balance = Column(Integer)
    custom_description = Column(String, nullable=True)
