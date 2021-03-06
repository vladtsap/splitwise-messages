from typing import List

from fastapi import APIRouter, Response

from bot.keyboards import pin_inline
from config import TELEGRAM_USER_ID, bot
from db.schemas import SplitwiseItem

router = APIRouter(
    prefix='/splitwise',
)


@router.post('')
async def process_transaction(items: List[SplitwiseItem]):
    for item in items:
        if not item.payment:
            await bot.send_message(
                chat_id=TELEGRAM_USER_ID,
                text=item.message_view,
                disable_notification=True,
                reply_markup=pin_inline,
            )

    return Response()


@router.get('')
async def ping():
    return Response()
