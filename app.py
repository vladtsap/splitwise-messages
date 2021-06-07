from datetime import datetime
from typing import Optional, List

from aiogram import Bot, types
from envparse import env
from fastapi import FastAPI, Response
from pydantic import BaseModel
from pytz import timezone

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = env.int("TELEGRAM_USER_ID")
SPLITWISE_USER_ID = env.int("SPLITWISE_USER_ID")

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML, validate_token=True)
app = FastAPI()


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


@app.get('/')
def test_request():
    return Response()


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


@app.post('/')
async def process_transaction(items: List[Item]):
    for item in items:
        if not item.payment:
            await bot.send_message(
                chat_id=TELEGRAM_USER_ID,
                text=message_view(item),
                disable_notification=True,
            )

    return Response()
