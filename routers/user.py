
import datetime
import uuid
import requests
import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session

import Util
from sql_app.crud import crudCommon, crudUser, crudCust
from sql_app.database import SessionLocal

router = APIRouter(
    prefix="/user",
)

class QueryUser(BaseModel):
    name: str = None

class view(BaseModel):
    base: str = None

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

@router.post("/querycustmess")
async def querycustmess(request_data: QueryUser,db: Session = Depends(get_db)):
    account = request_data.name
    message = {"real": None, "addr": None, "phone": None,}
    data = crudCommon.get_cust(db, account).__dict__
    data.pop('_sa_instance_state')
    data.pop('cust_password')
    message["real"]=data["cust_name"]
    message["addr"] = data["cust_addr"]
    message["phone"] = data["cust_phone"]
    addrlist = data['cust_addr'].split('-', 2)
    message['cust_floor'] = addrlist[0]
    message['cust_unit'] = addrlist[1]
    message['cust_door'] = addrlist[2]
    message['addr'] = message['cust_floor'] + '号楼' + message['cust_unit'] + '单元' + message['cust_door']
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

@router.post("/savecustmess")
async def save_user_mess(request_data: User,db: Session = Depends(get_db)):
    login = request_data.login
    real = request_data.real
    phone = request_data.phone
    addr = request_data.addr
    message = {"mess": "修改成功"}
    crudCommon.save_cust(db, login, real, phone)
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
        title = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d')+" 缴费通知"
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
        if time >= 0 and endtime < 0 and mid['poster_status']!= None:
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
        if time <= 0 and endtime < 0 and mid['poster_status']!= None:
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
    crudUser.change_Posterpost(db, request_data.id, time)
    return {"mess":"已发布"}

class Post(BaseModel):
    id: str = None
@router.post("/postsign")
async def postSign(request_data: Post, db: Session = Depends(get_db)):
    crudUser.change_Postersign(db,request_data.id)
    return {"mess":"已签发"}

@router.get("/queryadmin")
async def query_admin(db: Session = Depends(get_db)):
    data = crudUser.get_adminmess(db)
    message = []
    for i in data:
        mid = i.__dict__
        mid.pop('_sa_instance_state')
        mid.pop('admin_password')
        if mid['admin_root']==0:
            mid['status']=False
        else:
            mid['status'] = True
        message.append(mid)
    return message

@router.post("/DelAdmin")
async def Del_admin(request_data: User,db: Session = Depends(get_db)):
    crudUser.del_adminone(db, request_data.login)
    return "删除员工成功"

class Admin(BaseModel):
    admin_id:str = None
    admin_realname:str = None
    admin_loginname: str= None
    admin_addr:str = None
    admin_phone:str = None
    admin_root:str = None
    status:bool

@router.post("/AddAdmin")
async def AddAdmin(data:Admin,db:Session = Depends(get_db)):
    getdata = crudCommon.get_adminlogin(db, data.admin_loginname)
    if getdata != None:
        return "用户名重复请重新设置"
    id = str(uuid.uuid4())
    passwd = Util.setPass(id,data.admin_realname)
    if data.status:
        data.admin_root = 1
    else:
        data.admin_root = 0
    crudUser.add_admin(db, id,data.admin_addr,data.admin_realname,data.admin_phone,data.admin_loginname,passwd[1],data.admin_root)
    return "密码为："+passwd[0]

@router.post("/changeAdminMess")
async def changeAdminMess(data:Admin,db: Session = Depends(get_db)):
    if data.status:
        data.admin_root = 1
    else:
        data.admin_root = 0
    crudUser.change_Admin(db, data.admin_addr,data.admin_phone,data.admin_loginname,data.admin_realname,data.admin_root)
    return "修改成功"

@router.post("/resetPass")
async def resetPass(request_data: Admin,db: Session = Depends(get_db)):
    id = request_data.admin_id[0:8]
    name = request_data.admin_realname
    passwd =id+Util.FirstPinyin(name)
    md5Pass = Util.MD5(passwd)
    crudUser.resetAdminPass(db,request_data.admin_id,md5Pass)
    return "已将密码重置为："+passwd

class log(BaseModel):
    admin_id: str = None
    log_log:str = None
    title:str = None
    name: str = None

@router.post("/addlog")
async def addlog(data:log,db:Session = Depends(get_db)):
    id = str(uuid.uuid4())
    title = data.title
    log =data.log_log
    cust_id = data.admin_id
    time = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    status = 0
    crudCommon.addlog(db, id, title, log, cust_id, time, status)
    return "已通知"


@router.post("/querylog")
async def querylog(request_data:log,db:Session = Depends(get_db)):
    data = crudCommon.get_userid(db,request_data.name)
    data = data[0]
    data0 = crudCust.getlogfail(db, data)
    data1 = crudCust.getlogsucc(db, data)
    data = crudCust.getlog(db,data)
    message=[]
    mess=[]
    for i in data:
        mid = i.__dict__
        mid.pop('_sa_instance_state')
        mid.pop('cust_id')
        mid['log_time'] = mid['log_time'].strftime('%Y-%m-%d %H:%M')
        message.append(mid)
    mess.append(message)
    mess.append(data0)
    mess.append(data1)
    return mess


@router.get("/unsign")
async def unsign(db:Session = Depends(get_db)):
    data = crudCommon.get_poster(db)
    message = []
    jj=0
    for i in data:
        mid = i[0].__dict__
        time = datetime.datetime.now().replace(microsecond=0) - mid['poster_time']
        time = time.days * 86400 + time.seconds
        endtime = datetime.datetime.now().replace(microsecond=0) - mid['poster_endtime']
        endtime = endtime.days * 86400 + endtime.seconds
        if endtime < 0 and mid['poster_status'] == None:
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

@router.post("/view")
async  def view(request_data:view):
    cc = request_data.base[0:50].find(',')+1
    mess = request_data.base[cc:]
    data = {'images':[mess]}
    headers = {"Content-type": "application/json"}
    url = "http://1.15.184.95:8866/predict/chinese_ocr_db_crnn_mobile"
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    # 打印预测结果
    if r.json()["results"][0]['data']:
        return {'mess':'识别成功','res':r.json()["results"][0]['data'][0]['text']}
    return {'mess':'识别失败','res':''}

@router.get("/queryfixsort")
async  def qfs(db:Session = Depends(get_db)):
    data = crudUser.getfixsort(db)
    message=[]
    for i in data:
        message.append({'x':i[0],'y':i[1]})
    return message

@router.get("/querymoneybymonth")
async  def qmm(db:Session = Depends(get_db)):
    data = crudUser.getmoneybymonth(db)
    message=[]
    for i in data:
        message.append({'x':i[0],'y':i[1]})
    return message
