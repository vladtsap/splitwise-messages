from fastapi import APIRouter, Response

import schemas
from config import TELEGRAM_USER_ID, bot
from db import save_transaction, get_db

router = APIRouter(
    prefix='/monobank',
)


@router.post('')
async def new_transaction(webhook: schemas.Webhook):
    webhook_transaction = webhook.data.statement_item

    message = await bot.send_message(
        chat_id=TELEGRAM_USER_ID,
        text=webhook_transaction.message_view,
        disable_notification=True,
    )

    transaction = schemas.Transaction.from_webhook(
        webhook_transaction=webhook.data.statement_item,
        message_id=message.message_id,
        chat_id=message.chat.id,
    )

    with get_db() as db:
        save_transaction(db=db, transaction=transaction)

    return Response()


@router.get('')
async def ping():
    return Response()
