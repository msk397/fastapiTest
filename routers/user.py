import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

import Util
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
    oldPass:str = None
    confirmPass:str = None

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
    nP = request_data.newPass
    oP = request_data.oldPass
    cP = request_data.confirmPass
    data = crudCommon.get_userPass(db,login)
    ooP = Util.MD5(oP)
    if ooP != data[0]:
        return {"mess": "旧密码错误，请重新输入"}
    if oP == nP:
        return {"mess": "新密码与旧密码一致，请重新输入"}
    if nP != cP:
        return {"mess": "新密码与确认密码不一致，请重新输入"}
    nP =Util.MD5(nP)
    crudCommon.change_user_pass(db, login, nP)
    return {"mess": "修改成功"}

@router.get("/custnum")
async def custnum(db:Session = Depends(get_db)):
    data = crudCommon.getCustNum(db)
    return data

@router.get("/todaymoney")
async def todaymoney(db:Session = Depends(get_db)):
    time = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d')
    data0 = crudCommon.getmoneyfail(db,time)
    data1 = crudCommon.getmoneysucc(db,time)
    sum = data0+data1
    succ = '%.2f' %(data0/sum*100)+'%'
    sum = '%.2f' % sum
    str = '%.2f' %data1+'/'+sum
    return {'succ':succ,'fail':str}

@router.get("/fix")
async def fix(db:Session = Depends(get_db)):
    data0 = crudCommon.getfixsucc(db)
    data1 = crudCommon.getfixfail(db)
    sum = data0 + data1
    succ = '%.2f' % (data0 / sum * 100) + '%'
    sum = '%.0f' % sum
    str = '%.0f' % data0 + '/' + sum
    return {'succ':succ,'fail':str}

@router.get("/money")
async def money(db:Session = Depends(get_db)):
    data = crudCommon.getmoney(db)
    message = []
    for i in data:
        mid = i[1].__dict__
        mid.pop('_sa_instance_state')
        mid.pop('charge_time')
        mid.pop('charge_status')
        mid['name'] = i[0]
        message.append(mid)
    return message

@router.get("/todayfix")
async def todayfix(db:Session = Depends(get_db)):
    data = crudCommon.gettodayfix(db)
    message = []
    for i in data:
        mid = i[1].__dict__
        mid.pop('_sa_instance_state')
        mid.pop('admin_id')
        mid.pop('fix_status')
        mid.pop('fix_endtime')
        print(mid)
        mid['name'] = i[0]
        mid['addr'] = Util.addr(i[2])
        message.append(mid)
    return message

