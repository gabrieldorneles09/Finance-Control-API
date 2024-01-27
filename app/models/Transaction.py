from typing import Union
from pydantic import BaseModel
from uuid import UUID
import os
import json


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


    def convert_obj_to_json(self) -> dict:

        json_string = {
            "transaction_id": str(self.transaction_id),
            "transaction_receiver_id": self.transaction_receiver_id,
            "payment_form": self.payment_form,
            "entry_type": self.entry_type,
            "category": self.category,
            "description": self.description,
            "value": self.value,
            "charge_date": self.charge_date,
            "payment_date": self.payment_date,
            "recurrent": str(self.recurrent),
            "recurrence_type": self.recurrence_type,
            "insert_date": self.insert_date
        }

        return json_string
    
    def save_transaction(self) -> dict:
        transaction_dict = self.convert_obj_to_json()

        json_file = f"{os.getenv('DATA_PATH')}transactions.json"

        # Check if json file exists
        if os.path.exists(json_file):
            with open(json_file) as f:
                transactions_data = json.load(f)
            transactions = transactions_data["transactions"]
            transactions.append(transaction_dict)
            transactions_data["transactions"] = transactions

            with open(json_file, "w") as f:
                json.dump(transactions_data, f, indent=4, ensure_ascii=False)
        else:
            transaction_json = {
                "transactions": [transaction_dict]
            }
            with open(json_file, "w") as f:
                json.dump(transaction_json, f, indent=4, ensure_ascii=False)

        return transaction_dict
    
async def get_transaction_by_id(transaction_id: str) -> dict:
    json_file = f"{os.getenv('DATA_PATH')}transactions.json"

    with open(json_file) as f:
        transactions_data = json.load(f)
        transactions = transactions_data["transactions"]

    for transaction in transactions:
        if transaction["transaction_id"] == transaction_id:
            return transaction

    return None

async def get_all_transactions() -> list:
    json_file = f"{os.getenv('DATA_PATH')}transactions.json"

    with open(json_file) as f:
        transactions_data = json.load(f)
        transactions = transactions_data["transactions"]

    return transactions

async def get_transactions_by_receiver_id(receiver_id: str) -> list:
    json_file = f"{os.getenv('DATA_PATH')}transactions.json"
    transactions_by_receiver_id = []
    with open(json_file) as f:
        transactions_data = json.load(f)
        transactions = transactions_data["transactions"]

    for transaction in transactions:
        if transaction["transaction_receiver_id"] == receiver_id:
            transactions_by_receiver_id.append(transaction)

    return transactions_by_receiver_id