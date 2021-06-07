import logging
from datetime import datetime
from typing import Optional, List

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from envparse import env
from fastapi import FastAPI, Response
from pydantic import BaseModel
from pytz import timezone

logging.basicConfig(
    format=u'[%(asctime)s] %(levelname)-8s %(message)s',
    level=logging.INFO,
)

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = env.int("TELEGRAM_USER_ID")
SPLITWISE_USER_ID = env.int("SPLITWISE_USER_ID")

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML, validate_token=True)
dp = Dispatcher(bot, storage=MemoryStorage())

app = FastAPI()


class AccessMiddleware(BaseMiddleware):
    def __init__(self, allowed_user_id: int):
        self.allowed_user_id = allowed_user_id
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if message.from_user.id != self.allowed_user_id:
            raise CancelHandler()


dp.middleware.setup(AccessMiddleware(TELEGRAM_USER_ID))


class UserInfo(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]


class User(BaseModel):
    user: UserInfo
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
        f'🤑 <b>{owed}</b> — {item.description}\n' \
        f'💸 {item.cost} {item.currency}\n' \
        f'🕑 {item.date.astimezone(timezone("Europe/Kiev")).strftime("%d.%m %H:%M")}\n'

    return result


@app.post('/')
async def process_transaction(items: List[Item]):
    for item in items:
        if not item.payment:
            await bot.send_message(
                chat_id=TELEGRAM_USER_ID,
                text=message_view(item),
            )

    return Response()
