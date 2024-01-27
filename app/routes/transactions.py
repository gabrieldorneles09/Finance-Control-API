from fastapi import APIRouter, Depends
from ..dependencies import test_dependency
from ..models.Transaction import Transaction, get_transaction_by_id, get_transactions_by_receiver_id, get_all_transactions
from datetime import datetime
from uuid import uuid4
import os


transactions_file = os.getenv('DATA_PATH') + "transactions.json"

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(test_dependency)],
    responses={404: {"description": "Not found"}},
)

@router.post("/{receiver_id}")
async def create_transaction(transaction: Transaction, receiver_id: str) -> dict:
    # Create a new transaction based on the transaction received
    transaction.transaction_id = uuid4()
    transaction.transaction_receiver_id = receiver_id
    transaction.charge_date = str(datetime.strptime(transaction.charge_date,"%Y-%m-%d"))
    transaction.payment_date = str(datetime.strptime(transaction.payment_date,"%Y-%m-%d"))
    transaction.insert_date = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    transaction_dict = transaction.save_transaction()

    return transaction_dict

@router.get("/")
async def get_transactions():
    transactions = await get_all_transactions()

    if not transactions:
        return {"message": "No transactions found"}

    return {"transactions": transactions}

@router.get("/receiver/{receiver_id}")
async def get_transactions(receiver_id: str):
    transaction = await get_transactions_by_receiver_id(receiver_id)

    if not transaction:
        return {"message": "No transactions found"}
    
    return {"message": transaction}

@router.get("/{transaction_id}")
async def get_transactions(transaction_id: str):
    transaction = await get_transaction_by_id(transaction_id)

    if not transaction:
        return {"message": "No transactions found"}

    return {"message": transaction}
