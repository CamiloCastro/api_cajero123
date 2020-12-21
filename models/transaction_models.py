from pydantic import BaseModel
from datetime import datetime, date
from fastapi import HTTPException

class TransactionIn(BaseModel):
    username: str
    value: int

class TransactionOut(BaseModel):
    id: int
    username: str
    date: datetime
    value: int
    actual_balance: int

    class Config:
        orm_mode = True

def validate_transaction(transaction_in: TransactionIn):
    if transaction_in.username == None or not transaction_in.username:
        raise HTTPException(status_code=400, detail="El nombre de usuario no debe estar vacio")

    if transaction_in.value < 0:
        raise HTTPException(status_code=400, detail="El valor de la transacción debe ser positivo")
