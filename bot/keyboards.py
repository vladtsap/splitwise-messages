from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

pin_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('pin 📍', callback_data='pin')
        ]
    ]
)

unpin_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('unpin 📌', callback_data='unpin')
        ]
    ]
)
