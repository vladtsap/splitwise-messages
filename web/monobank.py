import asyncio
import logging
from datetime import datetime

from fastapi import APIRouter, Response
from pytz import timezone
import requests

from db import schemas
from config import TELEGRAM_USER_ID, bot, NOTION_SECRET
from db.core import save_transaction, get_db
from bot.keyboards import notion_button

router = APIRouter(
    prefix='/monobank',
)

logger = logging.getLogger(__name__)


async def save_to_notion(transaction: schemas.Transaction):
    payload = {
        "parent": {
            "type": "database_id",
            "database_id": "085c5720-d8b4-4ee4-84e8-49650e77b269"  # TODO: hardcoded
        },
        "properties": {
            "Description": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": transaction.description
                        }
                    }
                ]
            },
            "ID": {
                "rich_text": [
                    {
                        "text": {
                            "content": transaction.bank_id
                        }
                    }
                ]
            },
            "Comment": {
                "rich_text": [
                    {
                        "text": {
                            "content": transaction.comment or ''
                        }
                    }
                ]
            },
            "Custom Description": {
                "rich_text": [
                    {
                        "text": {
                            "content": transaction.custom_description or ''
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": datetime.utcfromtimestamp(transaction.time).astimezone(timezone("Europe/Kiev")).isoformat()
                }
            },
            "Amount": {
                "number": transaction.amount / 100
            },
            "Operation Amount": {
                "number": transaction.operation_amount / 100
            },
            "Currency": {
                "number": transaction.currency_code
            },
            "MCC": {
                "number": transaction.mcc
            },
            "Original MCC": {
                "number": transaction.original_mcc
            },
            "Commission": {
                "number": transaction.commission_rate / 100
            },
            "Cashback": {
                "number": transaction.cashback_amount / 100
            },
            "Balance": {
                "number": transaction.balance / 100
            },
        }
    }

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTION_SECRET}"
    }

    response = requests.post(
        "https://api.notion.com/v1/pages",
        json=payload,
        headers=headers,
    )

    try:
        page_id = response.json()['id'].replace('-', '')
    except KeyError:
        logger.error(f'KEY ERROR. RESPONSE: {response.json()}')
    else:
        await bot.edit_message_reply_markup(
            chat_id=transaction.chat_id,
            message_id=transaction.message_id,
            reply_markup=notion_button(page_id),
        )


@router.post('')
async def new_transaction(webhook: schemas.Webhook):
    webhook_transaction = webhook.data.statement_item

    message = await bot.send_message(
        chat_id=TELEGRAM_USER_ID,
        text=webhook_transaction.message_view,
        disable_notification=True,
    )

    transaction = schemas.Transaction.from_webhook(
        webhook_transaction=webhook.data.statement_item,
        message_id=message.message_id,
        chat_id=message.chat.id,
    )

    asyncio.create_task(save_to_notion(transaction))

    with get_db() as db:
        save_transaction(db=db, transaction=transaction)

    return Response()


@router.get('')
async def ping():
    return Response()
