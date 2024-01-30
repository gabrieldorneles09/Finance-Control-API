from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import test_dependency
from ..models.Transaction import Transaction, get_transaction_by_id, get_transactions_by_receiver_id, get_all_transactions, convert_transaction_to_json
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
    transaction.insert_date = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    if transaction.value < 0:
        raise HTTPException(status_code=400, detail="Value cannot be negative")

    if transaction.total_installments > 1:
        installments_transactions = await transaction.create_installments_transactions()
        await transaction.save_transaction(installments_transactions)

        return {"transactions": installments_transactions}

    transaction_dict = await convert_transaction_to_json(transaction)
    await transaction.save_transaction(transaction_dict)

    return {"transactions": transaction_dict}

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
    
    return {"transactions": transaction}

@router.get("/{transaction_id}")
async def get_transactions(transaction_id: str):
    transaction = await get_transaction_by_id(transaction_id)

    if not transaction:
        return {"message": "No transactions found"}

    return {"transactions": transaction}
