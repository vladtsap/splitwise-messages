import logging

from aiogram.types import Message, Update
from aiogram.utils import executor

from config import dp, bot
from db import get_transaction, get_db, update_transaction
from exceptions import TransactionNotFound

NEW_LINE = '\n'


@dp.message_handler(is_reply=True)
async def reply_handler(message: Message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )

    with get_db() as db:
        transaction = get_transaction(
            db=db,
            message_id=message.reply_to_message.message_id,
            chat_id=message.reply_to_message.chat.id,
        )

        if message.text == 'null':
            transaction.custom_description = None
        else:
            transaction.custom_description = message.text

        update_transaction(
            db=db,
            transaction=transaction,
        )

    await bot.edit_message_text(
        text=transaction.message_view,
        chat_id=transaction.chat_id,
        message_id=transaction.message_id,
    )


@dp.message_handler()
async def keep_chat_empty(message: Message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )


@dp.errors_handler(exception=TransactionNotFound)
async def handle_transaction_not_found(update: Update, _):
    message = update.message
    reply_message = message.reply_to_message

    logging.error(
        f'transaction not found. '
        f'[TRANSACTION_TEXT:{reply_message.text.replace(NEW_LINE, " ")}]'
        f'[TRANSACTION_MESSAGE:{reply_message.message_id}]'
        f'[TRANSACTION_CHAT:{reply_message.chat.id}]'
        f'[USERNAME:{message.from_user.username}]'
        f'[USER:{message.from_user.full_name}]'
        f'[USER_ID:{message.from_user.id}]'
        f'[MESSAGE_TEXT:{message.text}]'
        f'[MESSAGE_ID:{message.message_id}]'
        f'[MESSAGE_CHAT:{message.chat.id}]'
    )
    return True


executor.start_polling(dp)
