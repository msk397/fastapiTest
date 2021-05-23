# from fastapi import APIRouter, Depends, HTTPException
# from dependencies import get_token_header
#
# #路径 prefix：/items。
# #tags：（仅有一个 items 标签）。
# #额外的 responses。
# #dependencies：它们都需要我们创建的 X-Token 依赖项。
# #因此，我们可以将其添加到 APIRouter 中，而不是将其添加到每个路径操作中。
# #注意比较它与user的不同
# router = APIRouter(
#
#     prefix="/items",
#
#     #tags=["items"],
#
#    #  dependencies=[Depends(get_token_header)],
#    #
#    # responses={404: {"description": "Not found"}},
#
# )
#
#
#
# fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}
#
#
#
# @router.get("/")
#
# async def read_items():
#     return {"asd":"asd"}
#
# @router.get("/{item_id}")
#
# async def read_item(item_id: str):
#     if item_id not in fake_items_db:
#         raise HTTPException(status_code=404, detail="not found")
#     return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
#
#
# @router.put(
#     "/{item_id}",
#     tags=["custom"],
#     responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}
import random
import uuid
import time
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session

import Util
from routers.user import ChangePass
from sql_app.crud import crudCommon, crudCust, crudUser
from sql_app.database import SessionLocal

router = APIRouter(
    prefix="/cust",
)


def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class loginname(BaseModel):
    login: str  = None

@router.post("/money")
async def money(data:loginname,db:Session = Depends(get_db)):
    data = crudCust.getmoney(db,data.login)
    message = []
    for i in data:
        mid = i[1].__dict__
        mid.pop('_sa_instance_state')
        mid.pop('charge_time')
        mid.pop('charge_status')
        mid['name'] = i[0]
        mid['login'] = i[2]
        message.append(mid)
    return message

@router.post("/fix")
async def fix(data:loginname,db:Session = Depends(get_db)):
    data = crudCust.getfix(db,data.login)
    message = []
    for i in data:
        mid = i[0].__dict__
        mid.pop('_sa_instance_state')
        # 未处理
        if mid['admin_id'] == 'null':
            mid['admin_name'] = ''
            mid['admin_login'] = ''
            mid['fix_endtime'] = ''
        # 已处理
        else:
            mid['admin_name'] = i[1]
            mid['admin_login'] = i[2]
            mid['fix_endtime'] = str(mid['fix_endtime'])
        if mid['fix_status'] == None:
            mid['fix_status'] = "未处理"
            mid['status'] = False
            mid['fix_endtime'] = ''
        elif mid['fix_status'] == 0:
            mid['fix_status'] = "已指派"
            mid['status'] = False
            mid['fix_endtime'] = ''
        elif mid['fix_status'] == 1:
            mid['fix_status'] = "已处理"
            mid['status'] = True
            mid['fix_endtime'] = str(mid['fix_endtime'])
        mid['fix_startime'] = str(mid['fix_startime'])
        message.append(mid)
    return message

class Fix(BaseModel):
    login:str = None
    log:str = None
    time:str = None
    fix_sort:str = None
@router.post("/AddFix")
async def AddFix(data:Fix,db:Session = Depends(get_db)):
    cust_id = crudCommon.get_custid(db,data.login)
    cust_id = cust_id[0]
    admin_id="null"
    fixer_id='null'
    fix_id = str(uuid.uuid4())
    timeee = data.time
    status=None
    crudCust.addFix(db,cust_id,admin_id,fix_id,timeee,status,data.log,data.fix_sort,fixer_id)
    pid = str(uuid.uuid4())
    title = '业主提交了维修记录'
    log=''
    timee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    crudUser.addfixtimeline(db, pid,fix_id, title, log, None, timee)

class log(BaseModel):
    name:str = None

@router.post("/querylog")
async def querylog(request_data:log,db:Session = Depends(get_db)):
    data = crudCommon.get_custid(db,request_data.name)
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


@router.post("/changecustpass")
async def change_cust_pass(request_data: ChangePass,db: Session = Depends(get_db)):
    login = request_data.login
    nP = request_data.newPass
    oP = request_data.oldPass
    cP = request_data.confirmPass
    data = crudCommon.get_custPass(db,login)
    ooP = Util.MD5(oP)
    if ooP != data[0]:
        return {"mess": "旧密码错误，请重新输入"}
    if oP == nP:
        return {"mess": "新密码与旧密码一致，请重新输入"}
    if nP != cP:
        return {"mess": "新密码与确认密码不一致，请重新输入"}
    nP =Util.MD5(nP)
    crudCust.change_cust_pass(db, login, nP)
    return {"mess": "修改成功"}

class Logid(BaseModel):
    id: str = None
@router.post("/readmail")
async def readmail(request_data: Logid,db: Session = Depends(get_db)):
    crudCust.readmail(request_data.id,db)


class paymoney(BaseModel):
    charge_cost: str = None
    charge_ddl: str = None
    charge_id: str = None
    charge_memo:str = None
    cust_id:str = None
    name:str = None

@router.post("/paymoney")
async def paymoney(request_data: paymoney,db: Session = Depends(get_db)):
    id = request_data.charge_id
    flag = random.randint(0,1)
    if flag == 0:
        crudCust.paymoney(db,id)
        return "缴费成功"
    else:
        return "缴费失败"