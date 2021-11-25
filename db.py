from contextlib import contextmanager

from sqlalchemy.orm import Session

import models
import schemas
from config import SessionLocal
from exceptions import TransactionNotFound


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_transaction(db: Session, message_id: int, chat_id: int) -> models.Transaction:
    db_transaction = db.query(
        models.Transaction
    ).filter(
        models.Transaction.message_id == message_id,
        models.Transaction.chat_id == chat_id,
    ).first()

    if not db_transaction:
        raise TransactionNotFound()

    return db_transaction


def get_transaction(db: Session, message_id: int, chat_id: int) -> schemas.Transaction:
    db_transaction = get_db_transaction(db, message_id, chat_id)

    return schemas.Transaction.from_orm(db_transaction)


def update_transaction(db: Session, transaction: schemas.Transaction):
    db_transaction = get_db_transaction(
        db=db,
        message_id=transaction.message_id,
        chat_id=transaction.chat_id,
    )

    db_transaction.custom_description = transaction.custom_description
    db.commit()


def save_transaction(db: Session, transaction: schemas.Transaction):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
