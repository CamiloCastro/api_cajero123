from pydantic import BaseModel
import re
from fastapi import HTTPException

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    balance: int

    class Config:
        orm_mode = True

class UserInCreate(BaseModel):
    username: str
    password: str
    repeat_password: str
    balance: int

class ModifyBalanceIn(BaseModel):
    username: str
    balance: int

def validate_user(user_in: UserInCreate):

    if user_in.password != user_in.repeat_password:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    if user_in.balance < 0:
        raise HTTPException(status_code=400, detail="El balance debe ser positivo")

    if not user_in.username:
        raise HTTPException(status_code=400, detail="El username no debe estar vacío")

    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}"

    pat = re.compile(reg)

    mat = re.search(pat, user_in.password)

    if not mat:
        raise HTTPException(status_code=400, detail="La contraseña debe tener un número, una minúscula y una mayúscula")


