from sqlalchemy.orm import Session

import models
import schemas


def save_transaction(db: Session, transaction: schemas.Transaction):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
