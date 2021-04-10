from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from sql_app.crud import crudCommon
from sql_app.database import SessionLocal

router = APIRouter(
    prefix="/user",
)

class QueryUser(BaseModel):
    name: str = None

class User(BaseModel):
    login: str = None
    real: str = None
    addr: str = None
    phone: str = None

class ChangePass(BaseModel):
    login: str = None
    newPass: str = None

def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/queryusermess")
async def queryusermess(request_data: QueryUser,db: Session = Depends(get_db)):
    account = request_data.name
    message = {"real": None, "addr": None, "phone": None, "passwd": None}
    data = crudCommon.get_admin(db, account).__dict__
    data.pop('_sa_instance_state')
    message["real"]=data["admin_realname"]
    message["addr"] = data["admin_addr"]
    message["phone"] = data["admin_phone"]
    message["passwd"] = data["admin_password"]
    return message

@router.post("/saveusermess")
async def save_user_mess(request_data: User,db: Session = Depends(get_db)):
    login = request_data.login
    real = request_data.real
    phone = request_data.phone
    addr = request_data.addr
    message = {"mess": "修改成功"}
    crudCommon.save_admin(db, login, real, addr, phone)
    return message

@router.post("/changeuserpass")
async def change_user_pass(request_data: ChangePass,db: Session = Depends(get_db)):
    login = request_data.login
    newPass = request_data.newPass
    crudCommon.change_user_pass(db, login, newPass)
    return {"mess": "修改成功"}
