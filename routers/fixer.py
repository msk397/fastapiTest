import uuid
import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import Util
import routers.user
from sql_app.crud import crudCommon, crudUser, crudCust
from sql_app.database import SessionLocal
router = APIRouter(
    prefix="/fixer",
)
class Fixer(BaseModel):
    id: str = None
    name:str = None
    login:str = None
    phone:str = None
    sort:str = None
    sort_list: list = None
    passwd:str = None
def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/queryfixer")
async def query_fixer(db: Session = Depends(get_db)):
    data = crudUser.get_fixer(db)
    message = []
    for i in data:
        mid = i.__dict__
        mid.pop('_sa_instance_state')
        mid.pop('passwd')
        mid['sort_list']=mid['sort'].split(",")
        message.append(mid)
    return message


@router.post("/resetPass")
async def resetPass(request_data: Fixer,db: Session = Depends(get_db)):
    id = request_data.id[0:8]
    name = request_data.name
    passwd =id+Util.FirstPinyin(name)
    md5Pass = Util.MD5(passwd)
    crudUser.resetFixerPass(db,request_data.id,md5Pass)
    return "已将密码重置为："+passwd

@router.post("/Delfixer")
async def Del_fixer(request_data: Fixer,db: Session = Depends(get_db)):
    crudUser.del_Fixerone(db, request_data.login)
    return "已删除该工人师傅"

@router.post("/changeFixerMess")
async def changeFixerMess(data:Fixer,db: Session = Depends(get_db)):
    crudUser.change_Fixer(db, data.id,data.name,','.join(data.sort_list),data.phone)
    return "修改成功"

class log(BaseModel):
    id: str = None
    log_log:str = None
    title:str = None
    name: str = None
@router.post("/addlog")
async def addlog(data:log,db:Session = Depends(get_db)):
    id = str(uuid.uuid4())
    title = data.title
    log =data.log_log
    cust_id = data.id
    time = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    status = 0
    crudCommon.addlog(db, id, title, log, cust_id, time, status)
    return "已通知"

@router.post("/AddFixer")
async def AddFixer(data:Fixer,db:Session = Depends(get_db)):
    getdata = crudCommon.get_Fixerlogin(db, data.login)
    if getdata != None:
        return "用户名重复请重新设置"
    id = str(uuid.uuid4())
    passwd = Util.setPass(id,data.name)
    crudUser.add_fixer(db, id,data.name,data.phone,data.login,passwd[1],','.join(data.sort_list))
    return "密码为："+passwd[0]

@router.get("/queryfixersort")
async def query_fixersort(db: Session = Depends(get_db)):
    data = crudUser.get_fixer(db)
    elc=[]
    water=[]
    gas=[]
    net=[]
    message = []
    for i in data:
        mid = i.__dict__
        mid.pop('_sa_instance_state')
        mid.pop('passwd')
        if "电工" in mid['sort']:
            elc.append(mid['name'])
        if "水工" in mid['sort']:
            water.append(mid['name'])
        if "燃气工人" in mid['sort']:
            gas.append(mid['name'])
        if "网络工人" in mid['sort']:
            net.append(mid['name'])
    message.extend([gas,water,elc,net])
    return message

class postfix(BaseModel):
    admin_login:str = None
    cust_addr:str = None
    cust_name:str = None
    fix_id:str = None
    name :str = None

@router.post("/postfix")
async def postfix(data:postfix,db: Session = Depends(get_db)):
    id = str(uuid.uuid4())
    title = "待处理的维修记录"
    log = data.cust_addr+'的'+data.cust_name+'业主，需要您的帮助'
    cust_id = crudUser.get_fixerid(db,data.name)
    time = datetime.datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    status = 0
    crudCommon.addlog(db, id, title, log, cust_id[0], time, status)
    id = data.fix_id
    login = data.admin_login
    admin_id = crudCommon.get_userid(db, login)
    crudUser.postfix(db, id,  admin_id[0],cust_id[0])
    return {"mess": "指派成功"}

@router.post("/queryfixermess")
async def queryfixermess(request_data: Fixer,db: Session = Depends(get_db)):
    account = request_data.name
    message = {}
    data = crudCommon.get_fixer(db, account).__dict__
    data.pop('_sa_instance_state')
    message["name"]=data["name"]
    message["phone"] = data["phone"]
    message["passwd"] = data["passwd"]
    return message

@router.post("/savefixermess")
async def save_fixer_mess(request_data: Fixer,db: Session = Depends(get_db)):
    login = request_data.login
    name = request_data.name
    phone = request_data.phone
    crudCommon.save_fixer(db, login, name, phone)
    return {"mess": "修改成功"}

class log(BaseModel):
    admin_id: str = None
    log_log:str = None
    title:str = None
    name: str = None
@router.post("/querylog")
async def querylog(request_data:Fixer,db:Session = Depends(get_db)):
    data = crudUser.get_fixerid(db,request_data.name)
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

class ChangePass(BaseModel):
    login: str = None
    newPass: str = None
    oldPass:str = None
    confirmPass:str = None

@router.post("/changepass")
async def change_user_pass(request_data: ChangePass,db: Session = Depends(get_db)):
    login = request_data.login
    nP = request_data.newPass
    oP = request_data.oldPass
    cP = request_data.confirmPass
    data = crudCommon.get_fixerPass(db,login)
    ooP = Util.MD5(oP)
    if ooP != data[0]:
        return {"mess": "旧密码错误，请重新输入"}
    if oP == nP:
        return {"mess": "新密码与旧密码一致，请重新输入"}
    if nP != cP:
        return {"mess": "新密码与确认密码不一致，请重新输入"}
    nP =Util.MD5(nP)
    crudCommon.change_fixer_pass(db, login, nP)
    return {"mess": "修改成功"}