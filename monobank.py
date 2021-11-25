from fastapi import APIRouter, Response, Depends
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


@router.post('')
async def new_transaction(webhook: schemas.Webhook, db: Session = Depends(get_db)):
    message = await bot.send_message(
        chat_id=TELEGRAM_USER_ID,
        text='transaction',
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
