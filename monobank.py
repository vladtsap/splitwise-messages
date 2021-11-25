import datetime

from fastapi import APIRouter, Response, Depends
from pytz import timezone
from sqlalchemy.orm import Session

import schemas
from bot import bot
from config import TELEGRAM_USER_ID, SessionLocal
from db import save_transaction

router = APIRouter(
    prefix='/monobank',
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def message_view(transaction: schemas.WebhookTransaction) -> str:
    result = '🤑 ' if transaction.amount < 0 else '🍀 '
    result += f'<b>{transaction.amount / 100}'
    result += ' → ' if transaction.amount < 0 else ' ← '
    result += f'{transaction.description}</b>\n'

    if transaction.cashback_amount:
        result += f'💫 кешбек: {transaction.cashback_amount / 100}\n'

    if transaction.commission_rate:
        result += f'🧨 комісія: {transaction.commission_rate / 100}\n'

    result += f'🏦 залишок: {transaction.balance / 100}\n'

    date = datetime.datetime.fromtimestamp(transaction.time)
    result += f'🕑 {date.astimezone(timezone("Europe/Kiev")).strftime("%d.%m %H:%M")}\n'

    return result


@router.post('')
async def new_transaction(webhook: schemas.Webhook, db: Session = Depends(get_db)):
    webhook_transaction = webhook.data.statement_item

    message = await bot.send_message(
        chat_id=TELEGRAM_USER_ID,
        text=message_view(webhook_transaction),
        disable_notification=True,
    )

    transaction = schemas.Transaction.from_webhook(
        webhook_transaction=webhook.data.statement_item,
        message_id=message.message_id,
        chat_id=message.chat.id,
    )

    save_transaction(db=db, transaction=transaction)

    return Response()


@router.get('')
async def ping():
    return Response()
