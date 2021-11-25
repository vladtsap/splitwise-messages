from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class SplitwiseUser(BaseModel):
    user_id: int
    paid_share: float
    owed_share: float
    net_balance: float


class SplitwiseItem(BaseModel):
    id: int
    cost: float
    date: datetime
    created_at: datetime
    users: List[SplitwiseUser]
    payment: bool
    currency: str
    group_id: Optional[int]
    description: str
    friendship_id: Optional[int]

