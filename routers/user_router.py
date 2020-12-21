from typing import List
from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text, func
from db.db_connection import get_db
from db.user_db import UserInDB
from db.transaction_db import TransactionInDB

from models.user_models import UserIn, UserOut
from models.transaction_models import TransactionIn, TransactionOut

router = APIRouter()

@router.get("/examples")
async def examples(db: Session = Depends(get_db)):

    '''
    user1 = UserInDB(username = "juan25", password = "hola", balance = 120000)
    user2 = UserInDB(username = "andres15", password = "password", balance = 80000)    
    db.add_all([user1, user2])
    db.commit()
    '''
    
    users = db.query(func.count(UserInDB.username))

    users_list = users.one_or_none()
    print(users_list[0])
    print("*******************")

    for u in users.all():
        print(u)


    return {"Message" : "Todo funciono bien"}
#    db.refresh(user1)

    #users = db.query(UserInDB).order_by(UserInDB.username)


@router.post("/user/auth/")
async def auth_user(user_in: UserIn, db: Session = Depends(get_db)):

    user_in_db = db.query(UserInDB).get(user_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if user_in_db.password != user_in.password:
        raise HTTPException(status_code=403, detail="Error de autenticacion")

    return {"Autenticado": True}

@router.get("/user/balance/{username}", response_model=UserOut)
async def get_balance(username: str, db: Session = Depends(get_db)):

    user_in_db = db.query(UserInDB).get(username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    return user_in_db