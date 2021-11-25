from datetime import datetime
from typing import Optional, List

from fastapi_camelcase import CamelModel
from pydantic import BaseModel


class SplitwiseUser(BaseModel):
    user_id: int
    paid_share: float
    owed_share: float
    net_balance: float


class SplitwiseItem(BaseModel):
    id: int
    cost: float
    date: datetime
    created_at: datetime
    users: List[SplitwiseUser]
    payment: bool
    currency: str
    group_id: Optional[int]
    description: str
    friendship_id: Optional[int]


class WebhookTransaction(CamelModel):
    id: str
    time: int
    description: str
    comment: Optional[str]
    mcc: int
    original_mcc: int
    amount: int
    operation_amount: int
    currency_code: int
    commission_rate: int
    cashback_amount: int
    balance: int


class WebhookData(CamelModel):
    account: str
    statement_item: WebhookTransaction


class Webhook(BaseModel):
    type: str
    data: WebhookData


class Transaction(BaseModel):
    bank_id: str
    message_id: int
    chat_id: int
    time: int
    description: str
    comment: Optional[str]
    mcc: int
    original_mcc: int
    amount: int
    operation_amount: int
    currency_code: int
    commission_rate: int
    cashback_amount: int
    balance: int
    custom_description: Optional[str]

    @classmethod
    def from_webhook(
            cls, webhook_transaction: WebhookTransaction,
            message_id: int, chat_id: int, custom_description: str = None,
    ):
        return cls(
            bank_id=webhook_transaction.id,
            message_id=message_id,
            chat_id=chat_id,
            time=webhook_transaction.time,
            description=webhook_transaction.description,
            comment=webhook_transaction.comment,
            mcc=webhook_transaction.mcc,
            original_mcc=webhook_transaction.original_mcc,
            amount=webhook_transaction.amount,
            operation_amount=webhook_transaction.operation_amount,
            currency_code=webhook_transaction.currency_code,
            commission_rate=webhook_transaction.commission_rate,
            cashback_amount=webhook_transaction.cashback_amount,
            balance=webhook_transaction.balance,
            custom_description=custom_description,
        )
