from typing import List

from fastapi import APIRouter, Response
from pytz import timezone

from bot import bot
from config import SPLITWISE_USER_ID, TELEGRAM_USER_ID
from schemas import SplitwiseItem

router = APIRouter(
    prefix='/splitwise',
)


def message_view(item: SplitwiseItem) -> str:
    owed = 0.
    for user in item.users:
        if user.user_id == SPLITWISE_USER_ID:
            owed = user.owed_share
            break

    result = \
        f'🤑 <b>{owed:,.2f} → {item.description}</b>\n' \
        f'💸 {item.cost:,.2f} {item.currency}\n' \
        f'🕑 {item.date.astimezone(timezone("Europe/Kiev")).strftime("%d.%m %H:%M")}\n'

    return result


@router.post('')
async def process_transaction(items: List[SplitwiseItem]):
    for item in items:
        if not item.payment:
            await bot.send_message(
                chat_id=TELEGRAM_USER_ID,
                text=message_view(item),
                disable_notification=True,
            )

    return Response()


@router.get('')
async def ping():
    return Response()
