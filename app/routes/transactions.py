from fastapi import APIRouter, Depends
from ..dependencies import test_dependency
from ..models.Transaction import Transaction
from datetime import datetime
from uuid import uuid4
import os

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(test_dependency)],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_transaction(transaction: Transaction) -> dict:
    # Create a new transaction based on the transaction received
    transaction.transaction_id = uuid4()
    transaction.transaction_receiver_id = "XXX"
    transaction.charge_date = str(datetime.strptime(transaction.charge_date,"%Y-%m-%d"))
    transaction.payment_date = str(datetime.strptime(transaction.payment_date,"%Y-%m-%d"))
    transaction.insert_date = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    with open(f"{os.getenv("DATA_PATH")}transactions.txt", "a") as f:
            f.write(str(transaction.model_dump()) + "\n")

    return {"transaction": transaction}

@router.get("/")
async def get_transactions():
    with open(f"{os.getenv('DATA_PATH')}transactions.txt", "r") as f:
            transactions = [line.strip('\n') for line in f]

    return {"message": transactions}

@router.get("/{transaction_id}")
async def get_transactions(transaction_id: str):
    with open(f"{os.getenv('DATA_PATH')}transactions.txt", "r") as f:
        for line in f:
            if transaction_id in line:
                transaction = line.strip('\n')
                return {"message": transaction}

    return {"message": "Transaction not found"}
    