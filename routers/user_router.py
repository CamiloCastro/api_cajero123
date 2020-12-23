from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException, Header

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text, func
from db.db_connection import get_db
from db.user_db import UserInDB
from db.transaction_db import TransactionInDB
from db.role_db import RoleInDB
from db.user_roles_db import UserRoleInDB

from models.user_models import UserIn, UserOut, UserInCreate, ModifyBalanceIn, validate_user
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

@router.post("/user/balance/modify/")
async def modify_balance(modify_balance_in: ModifyBalanceIn, db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):

    if authorization == None:
        raise HTTPException(status_code=403, detail="No está autorizado")

    lista_roles = db.query(UserRoleInDB).\
        filter(UserRoleInDB.username == authorization, UserRoleInDB.role_name == "BANCO").\
            all()
    
    if not lista_roles:
        raise HTTPException(status_code=403, detail="No está autorizado")
    
    user_in_db = db.query(UserInDB).get(modify_balance_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    user_in_db.balance = modify_balance_in.balance
    db.commit()
    db.refresh(user_in_db)

    return {"Message" : "Balance modificado correctamente"}

@router.post("/user/create/")
async def user_create(user_in_create: UserInCreate, db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if authorization == None:
        raise HTTPException(status_code=403, detail="No está autorizado")

    lista_roles = db.query(UserRoleInDB).\
        filter(UserRoleInDB.username == authorization, UserRoleInDB.role_name == "BANCO").\
            all()
    
    if not lista_roles:
        raise HTTPException(status_code=403, detail="No está autorizado")

    validate_user(user_in_create)

    user_in_db = UserInDB(username = user_in_create.username, password = user_in_create.password, balance = user_in_create.balance)
    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)

    user_role_in_db = UserRoleInDB(username=user_in_create.username, role_name="USUARIO")
    db.add(user_role_in_db)
    db.commit()
    db.refresh(user_role_in_db)

    return {"Message" : "Usuario creado exitosamente"}

@router.post("/user/auth/")
async def auth_user(user_in: UserIn, db: Session = Depends(get_db)):

    user_in_db = db.query(UserInDB).get(user_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if user_in_db.password != user_in.password:
        raise HTTPException(status_code=403, detail="Error de autenticacion")

    roles = db.query(UserRoleInDB).\
        filter(UserRoleInDB.username == user_in.username).\
            order_by(UserRoleInDB.role_name).all()

    return roles

@router.get("/user/roles/{username}")
async def get_roles(username: str, db: Session = Depends(get_db)):
    
    roles = db.query(UserRoleInDB).\
        filter(UserRoleInDB.username == username).\
            order_by(UserRoleInDB.role_name).all()

    return roles

@router.get("/user/balance/{username}", response_model=UserOut)
async def get_balance(username: str, db: Session = Depends(get_db)):

    user_in_db = db.query(UserInDB).get(username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    return user_in_db