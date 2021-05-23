import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import time
import Util
from routers import fixer
from sql_app.crud import crudCommon, crudUser
from sql_app.database import SessionLocal

router = APIRouter(
    prefix="/userFix",
)
def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/queryUserFix")
async def query_UserFix(db: Session = Depends(get_db)):
    data = crudUser.get_fix(db)
    message = []
    for i in data:
        mid = i[0].__dict__
        mid.pop('_sa_instance_state')
        mid['cust_name'] = i[1]
        mid['cust_addr'] = Util.addr(i[4])
        #未处理
        if mid['admin_id'] == 'null':
            mid['admin_name'] = ''
            mid['admin_login'] = ''
            mid['fixer_name'] = ''
        #已处理
        else:
            mid['admin_name'] = i[2]
            mid['admin_login'] = i[3]
            mid['fixer_name'] = i[5]
        if mid['fix_status'] == None:
            mid['fix_status'] = "未处理"
            mid['status'] = False
            mid['fix_endtime'] = ''
        elif mid['fix_status']==0:
            mid['fix_status'] = "已指派"
            mid['status'] = False
            mid['fix_endtime'] = ''
        elif mid['fix_status']==1:
            mid['fix_status'] = "已处理"
            mid['status'] = True
            mid['fix_endtime'] = str(mid['fix_endtime'])
        mid['fix_startime'] = str(mid['fix_startime'])
        mid.pop('cust_id')
        message.append(mid)
    return message


class DelFix(BaseModel):
    id: str = None

@router.post("/DelFix")
async def Del_fix(request_data: DelFix,db: Session = Depends(get_db)):
    crudUser.del_fixone(db, request_data.id)

class changeFix(BaseModel):
    status: bool
    fix_id:str=None
    fix_endtime:str=None
    fix_log:str=None
    fix_startime:str=None
    admin_login:str=None
    cust_name:str=None

@router.post("/changeFix")
async def change_fix(request_data: changeFix,db: Session = Depends(get_db)):
    id =request_data.fix_id
    end =request_data. fix_endtime
    start =request_data. fix_startime
    log =request_data. fix_log
    login = request_data.admin_login
    name = request_data.cust_name
    status =request_data.status
    if end =='':
        end = start
        login = 'null'
    admin_id = crudCommon.get_userid(db, login)
    crudUser.change_fix(db, id,end,start,log,admin_id[0])
    return {"mess": "修改成功"}

@router.post("/queryUserFixbyfixer")
async def query_UserFix(redata:fixer.Fixer,db: Session = Depends(get_db)):
    data = crudUser.get_fixbyfixer(db,redata.name)
    message = []
    for i in data:
        mid = i[0].__dict__
        mid.pop('_sa_instance_state')
        mid['cust_name'] = i[1]
        mid['cust_addr'] = Util.addr(i[4])
        #未处理
        if mid['admin_id'] == 'null':
            mid['admin_name'] = ''
            mid['admin_login'] = ''
            mid['fixer_name'] = ''
        #已处理
        else:
            mid['admin_name'] = i[2]
            mid['admin_login'] = i[3]
            mid['fixer_name'] = i[5]
        if mid['fix_status'] == None:
            mid['fix_status'] = "未处理"
            mid['status'] = False
            mid['fix_endtime'] = ''
        elif mid['fix_status']==0:
            mid['fix_status'] = "已指派"
            mid['status'] = False
            mid['fix_endtime'] = ''
        elif mid['fix_status']==1:
            mid['fix_status'] = "已处理"
            mid['status'] = True
            mid['fix_endtime'] = str(mid['fix_endtime'])
        mid['fix_startime'] = str(mid['fix_startime'])
        mid.pop('cust_id')
        message.append(mid)
    return message

class tl(BaseModel):
    id:str=None
    log:str=None
    name:str=None
    pic:str=None

@router.post("/addtimeline")
async def addtl(data:tl,db: Session = Depends(get_db)):
    pid=str(uuid.uuid4())
    title=data.name+'师傅上传了维修记录'
    timee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    crudUser.addfixtimeline(db,pid,data.id,title,data.log,data.pic,timee)

@router.post("/queryFixlog")
async def qfl(data: tl, db: Session = Depends(get_db)):
    data = crudUser.get_fixlog(db, data.id)
    message = []
    for i in data:
        mid = i.__dict__
        mid.pop('_sa_instance_state')
        mid['time'] = mid['time'].strftime('%Y-%m-%d %H:%M:%S')
        message.append(mid)
    return message

@router.post("/finalfix")
async def ff(data: tl, db: Session = Depends(get_db)):
    timee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    crudUser.finalfix(db,data.id,timee)
    pid = str(uuid.uuid4())
    title = '完成维修'
    log = ''
    crudUser.addfixtimeline(db, pid, data.id, title, log, None, timee)
    return "已提交"


