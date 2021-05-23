from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import Util
from sql_app.crud import crudCommon
from sql_app.database import SessionLocal
router = APIRouter(
    prefix="/common",
)

def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Item(BaseModel):
    choose: str=None
    account: str = None
    passwd: str = None

@router.post("/signin")
async def signin(request_data: Item,db: Session = Depends(get_db)):
    choose = request_data.choose
    account = request_data.account
    passwd = Util.MD5(request_data.passwd)
    message={"flag":False,"mess":None,"name":None}
    if choose == 'admin':
        data = crudCommon.get_admin(db, account)
        flag = 0
    elif choose =='fixer':
        data = crudCommon.get_fixer(db, account)
        flag = 2
    else:
        data = crudCommon.get_cust(db,account)
        flag = 1
    if not bool(data):
        message["flag"]="error"
        message["mess"]="用户不存在"
    else:
        data = data.__dict__
        data.pop('_sa_instance_state')
        if flag==0:
            if data["admin_password"] == passwd:
                message["flag"] = "success"
                message["mess"] = "admin"
                message["name"] = data["admin_realname"]
            else:
                message["flag"] = "error"
                message["mess"] = "密码错误"
        elif flag==1:
            if data["cust_password"] == passwd:
                message["flag"] = "success"
                message["mess"] = "cust"
                message["name"] = data["cust_name"]
            else:
                message["flag"] = "error"
                message["mess"] = "密码错误"
        elif flag==2:
            if data["passwd"] == passwd:
                message["flag"] = "success"
                message["mess"] = "fixer"
                message["name"] = data["name"]
            else:
                message["flag"] = "error"
                message["mess"] = "密码错误"
    return message



