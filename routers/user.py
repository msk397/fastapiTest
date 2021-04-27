import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session

import Util
from sql_app.crud import crudCommon, crudUser
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
    sum = '%.0f' % sum
    str = '%.0f' %data1+'/'+sum
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
        mid['name'] = i[0]
        mid['addr'] = Util.addr(i[2])
        message.append(mid)
    return message

class moneyalert(BaseModel):
    charge_cost: str = None
    charge_ddl: str = None
    charge_id: str = None
    charge_memo:str = None
    cust_id:str = None
    name:str = None

@router.post("/moneyalert")
async def moneyalert(request_data: moneyalert,db: Session = Depends(get_db)):
    data = crudCommon.getlog(db,request_data.charge_id)
    if data ==None:
        id = request_data.charge_id
        title = "缴费通知"
        log = "您有一笔"+request_data.charge_cost+"元的"+request_data.charge_memo+"，请及时缴纳"
        cust_id = request_data.cust_id
        time =datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        status = 0
        crudCommon.addlog(db,id,title,log,cust_id,time,status)
        return {"mess":"已通知"}
    else:
        return {"mess":"已通知完毕，请勿重复通知"}

@router.get("/poster")
async def poster(db:Session = Depends(get_db)):
    data = crudCommon.get_poster(db)
    message = []
    for i in data:
        mid = i[0].__dict__
        time = datetime.datetime.now().replace(microsecond=0) - mid['poster_time']
        time = time.days * 86400 + time.seconds
        endtime = datetime.datetime.now().replace(microsecond=0) - mid['poster_endtime']
        endtime = endtime.days * 86400 + endtime.seconds
        if time >= 0 and endtime < 0:
            mid['time'] = mid['poster_time'].strftime('%Y-%m-%d %H:%M')
            mid['endtime'] = mid['poster_endtime'].strftime('%Y-%m-%d %H:%M')
            mid.pop('_sa_instance_state')
            mid['admin_name'] = i[1]
            mid.pop('admin_id')
            mid.pop('poster_time')
            mid.pop('poster_endtime')
            message.append(mid)
    return message

@router.get("/postercount")
async def poster(db:Session = Depends(get_db)):
    data = crudCommon.get_postercount(db)
    message = []
    message.append(data)
    return message

@router.get("/unposter")
async def poster(db:Session = Depends(get_db)):
    data = crudCommon.get_poster(db)
    message = []
    jj=0
    for i in data:
        mid = i[0].__dict__
        time = datetime.datetime.now().replace(microsecond=0) - mid['poster_time']
        time = time.days * 86400 + time.seconds
        endtime = datetime.datetime.now().replace(microsecond=0) - mid['poster_endtime']
        endtime = endtime.days * 86400 + endtime.seconds
        if time <= 0 and endtime < 0:
            mid['time'] = mid['poster_time'].strftime('%Y-%m-%d %H:%M')
            mid['endtime'] = mid['poster_endtime'].strftime('%Y-%m-%d %H:%M')
            mid.pop('_sa_instance_state')
            mid['admin_name'] = i[1]
            mid.pop('admin_id')
            mid.pop('poster_time')
            mid.pop('poster_endtime')
            jj+=1
            message.append(mid)
    return message

class post(BaseModel):
    id: str = None

@router.post("/post")
async def post(request_data: post,db: Session = Depends(get_db)):
    time = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    crudUser.change_Posterpost(db,request_data.id,time)
    return {"mess":"已发布，请刷新页面查看"}
