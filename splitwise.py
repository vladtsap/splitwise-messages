from datetime import datetime
from typing import Optional, List

from fastapi import Response, APIRouter
from pydantic import BaseModel
from pytz import timezone

from bot import bot
from config import SPLITWISE_USER_ID, TELEGRAM_USER_ID

router = APIRouter(
    prefix='/splitwise',
)


class User(BaseModel):
    user_id: int
    paid_share: float
    owed_share: float
    net_balance: float


class Item(BaseModel):
    id: int
    cost: float
    date: datetime
    created_at: datetime
    users: List[User]
    payment: bool
    currency: str
    group_id: Optional[int]
    description: str
    friendship_id: Optional[int]


def message_view(item: Item) -> str:
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
async def process_transaction(items: List[Item]):
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
