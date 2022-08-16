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


def notion_button(page_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    'link to notion',
                    url=f'https://www.notion.so/{page_id}',
                )
            ]
        ]
    )
    return keyboard
