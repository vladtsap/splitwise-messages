import logging
from typing import Match

from aiogram.types import Message, Update, CallbackQuery, ContentTypes
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageNotModified

from config import dp, bot, TELEGRAM_USER_ID
from db.core import get_transaction, get_db, update_transaction
from db.exceptions import TransactionNotFound
from db.schemas import ManualTransaction
from keyboards import pin_inline, unpin_inline

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

    if message.reply_to_message.reply_markup == pin_inline:
        reply_markup = pin_inline
    else:
        reply_markup = unpin_inline

    await bot.edit_message_text(
        text=transaction.message_view,
        chat_id=transaction.chat_id,
        message_id=transaction.message_id,
        reply_markup=reply_markup,
    )


@dp.message_handler(regexp=r'^((-|\+)\d+.?\d)( (.*))?')
async def manual_transaction(message: Message, regexp: Match[str]):
    transaction = ManualTransaction.from_user(
        amount=float(regexp[1]),
        description=regexp[4],
    )

    await bot.send_message(
        chat_id=TELEGRAM_USER_ID,
        text=transaction.message_view,
        disable_notification=True,
        reply_markup=pin_inline,
    )


@dp.message_handler()
async def keep_chat_empty(message: Message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )


@dp.callback_query_handler(text='pin')
async def pin_message(query: CallbackQuery):
    await bot.pin_chat_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        disable_notification=True,
    )

    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=unpin_inline,
    )

    await query.answer('📍')


@dp.callback_query_handler(text='unpin')
async def unpin_message(query: CallbackQuery):
    await bot.pin_chat_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        disable_notification=True,
    )

    await bot.unpin_chat_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
    )

    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=pin_inline,
    )

    await query.answer('📌')


@dp.message_handler(content_types=ContentTypes.PINNED_MESSAGE)
async def clear_service_pinned_message(message: Message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )


@dp.errors_handler(exception=MessageNotModified)
async def handle_message_not_modified(*_):
    return True


@dp.errors_handler(exception=TransactionNotFound)
async def handle_transaction_not_found(update: Update, _):
    message = update.message
    reply_message = message.reply_to_message

    logging.error(
        f'transaction not found. '
        f'[TRANSACTION_TEXT:{reply_message.text.replace(NEW_LINE, " ") if reply_message.text else None}]'
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
