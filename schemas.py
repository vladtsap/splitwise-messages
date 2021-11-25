from datetime import datetime
from typing import Optional, List

from fastapi_camelcase import CamelModel
from pydantic import BaseModel
from pytz import timezone

from config import SPLITWISE_USER_ID


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

    @property
    def message_view(self) -> str:
        owed = 0.
        for user in self.users:
            if user.user_id == SPLITWISE_USER_ID:
                owed = user.owed_share
                break

        result = (
            f'🤑 <b>{owed:,.2f} → {self.description}</b>\n'
            f'💸 {self.cost:,.2f} {self.currency}\n'
            f'🕑 {self.date.astimezone(timezone("Europe/Kiev")).strftime("%d.%m %H:%M")}\n'
            f'#сплітвайс'
        )
        return result


class TransactionBase(CamelModel):
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

    @property
    def message_view(self) -> str:
        result = '🤑 ' if self.amount < 0 else '🍀 '
        result += f'<b>{self.amount / 100}'
        result += ' → ' if self.amount < 0 else ' ← '
        result += f'{self.description}</b>\n'

        if self.cashback_amount:
            result += f'💫 кешбек: {self.cashback_amount / 100}\n'

        if self.commission_rate:
            result += f'🧨 комісія: {self.commission_rate / 100}\n'

        result += f'🏦 залишок: {self.balance / 100}\n'

        date = datetime.fromtimestamp(self.time)
        result += f'🕑 {date.astimezone(timezone("Europe/Kiev")).strftime("%d.%m %H:%M")}\n'

        if self.comment:
            result += f'✏️ {self.comment}\n'

        if self.custom_description:
            result += f'🏷 {self.custom_description}\n'

        return result


class WebhookTransaction(TransactionBase):
    id: str


class WebhookData(CamelModel):
    account: str
    statement_item: WebhookTransaction


class Webhook(BaseModel):
    type: str
    data: WebhookData


class Transaction(TransactionBase):
    bank_id: str
    message_id: int
    chat_id: int

    class Config:
        orm_mode = True

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
            description=webhook_transaction.description.replace('\n', ' '),
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
