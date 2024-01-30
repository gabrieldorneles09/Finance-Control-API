from typing import Union
from pydantic import BaseModel
from uuid import UUID, uuid4
from fastapi import Path
import os
import json
from datetime import date
from dateutil.relativedelta import relativedelta


class Transaction(BaseModel):
    transaction_id: Union[UUID, None] = None
    transaction_receiver_id: Union[str, None] = None
    payment_form: str
    entry_type: str
    category: str
    description: str
    value: float
    charge_date: date
    payment_date: date
    recurrent: bool
    recurrence_type: Union[str, None] = None
    total_installments: Union[int, None] = None
    installment_id: Union[UUID, None] = None
    installment: Union[int, None] = None
    installment_value: Union[float, None] = None
    insert_date: Union[str, None] = None
   
    async def save_transaction(self, transaction_dict: Union[dict, list[dict]]) -> dict:
        json_file = f"{os.getenv('DATA_PATH')}transactions.json"
        # Check if json file exists
        if os.path.exists(json_file):
            with open(json_file) as f:
                transactions_data = json.load(f)
            transactions = transactions_data["transactions"]
            if isinstance(transaction_dict, dict):
                transactions.append(transaction_dict)
            else:
                transactions.extend(transaction_dict)

            transactions_data["transactions"] = transactions

            with open(json_file, "w") as f:
                json.dump(transactions_data, f, indent=4, ensure_ascii=False)
        else:
            transaction_json = {
                "transactions": [transaction_dict] if isinstance(transaction_dict, dict) else transaction_dict
            }
            with open(json_file, "w") as f:
                json.dump(transaction_json, f, indent=4, ensure_ascii=False)

        return transaction_dict
    
    async def create_installments_transactions(self) -> list[dict]:
        self.installment_value = round(self.value / self.total_installments, 2)
        installments_transactions = []

        for i in range(0, self.total_installments):
            installment_transaction = self.model_copy(update={
                "installment_id": uuid4(),
                "payment_date": self.payment_date + relativedelta(months=i),
                "installment": i + 1,
            })
            installments_transactions.append(await convert_transaction_to_json(installment_transaction))
        return installments_transactions
    
async def convert_transaction_to_json(transaction: Transaction) -> dict:

    json_string = {
        "transaction_id": str(transaction.transaction_id),
        "transaction_receiver_id": transaction.transaction_receiver_id,
        "payment_form": transaction.payment_form,
        "entry_type": transaction.entry_type,
        "category": transaction.category,
        "description": transaction.description,
        "value": transaction.value,
        "charge_date": str(transaction.charge_date),
        "payment_date": str(transaction.payment_date),
        "recurrent": transaction.recurrent,
        "recurrence_type": transaction.recurrence_type,
        "total_installments": transaction.total_installments,
        "installment_id": str(transaction.installment_id) if transaction.installment_id else transaction.installment_id,
        "installment": transaction.installment,
        "installment_value": transaction.installment_value,
        "insert_date": transaction.insert_date
    }

    return json_string

async def get_transaction_by_id(transaction_id: str) -> dict:
    json_file = f"{os.getenv('DATA_PATH')}transactions.json"

    with open(json_file) as f:
        transactions_data = json.load(f)
        transactions = transactions_data["transactions"]

    transactions_found = []
    for transaction in transactions:
        if transaction["transaction_id"] == transaction_id:
            transactions_found.append(transaction)

    return transactions_found if transactions_found else None

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