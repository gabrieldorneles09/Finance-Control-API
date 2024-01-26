from fastapi import FastAPI, Depends
from .dependencies import test_dependency
from .routes import transactions
import dotenv
import os

dotenv.load_dotenv()

app = FastAPI(dependencies=[Depends(test_dependency)])

app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"Hello": os.getenv("TESTE")}
