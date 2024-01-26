from typing import Union
from pydantic import BaseModel
from uuid import UUID
import os


class Transaction(BaseModel):
    transaction_id: Union[UUID, None] = None
    transaction_receiver_id: Union[str, None] = None
    payment_form: str
    entry_type: str
    category: str
    description: str
    value: float
    charge_date: str
    payment_date: str
    recurrent: bool
    recurrence_type: Union[str, None] = None
    insert_date: Union[str, None] = None
