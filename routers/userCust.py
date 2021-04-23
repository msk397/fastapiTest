import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import  Util
from sql_app.crud import crudCommon, crudUser
from sql_app.database import SessionLocal

router = APIRouter(
    prefix="/userCust",
)
def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/queryCust")
async def query_cust(db: Session = Depends(get_db)):
    data = crudUser.get_custmess(db)
    message = []
    for i in data:
        mid = i.__dict__
        mid.pop('_sa_instance_state')
        addrlist = mid['cust_addr'].split('-', 2)
        mid['cust_floor'] = addrlist[0]
        mid['cust_unit']=addrlist[1]
        mid['cust_door'] = addrlist[2]
        mid['cust_addr']= mid['cust_floor']+'号楼'+mid['cust_unit']+'单元'+mid['cust_door']
        message.append(mid)
    return message

class resetPass(BaseModel):
    id: str = None
    name: str = None

@router.post("/resetPass")
async def resetPass(request_data: resetPass,db: Session = Depends(get_db)):
    id = request_data.id[0:5]
    name = request_data.name
    passwd =id+Util.FirstPinyin(name)
    md5Pass = Util.MD5(passwd)
    crudUser.resetCustPass(db,request_data.id,md5Pass)
    return passwd


class CustMess(BaseModel):
    cust_floor:str = None
    cust_unit:str = None
    cust_door:str = None
    cust_addr:str = None
    cust_id:str = None
    cust_name:str = None
    cust_phone:str = None
    cust_loginname:str = None


@router.post("/changeCustMess")
async def changeCustMess(data:CustMess,db: Session = Depends(get_db)):
    addr = data.cust_floor+'-'+data.cust_unit+'-'+data.cust_door
    crudUser.change_Cust(db, data.cust_id, addr,data.cust_name,data.cust_phone)
    return {"mess": "修改成功"}


class AddCust(BaseModel):
    cust_floor: str = None
    cust_unit: str = None
    cust_door: str = None
    cust_name: str = None
    cust_phone: str = None
    cust_loginname: str = None


@router.post("/AddCust")
async def AddCust(data:AddCust,db:Session = Depends(get_db)):
    addr =  data.cust_floor+'-'+data.cust_unit+'-'+data.cust_door
    id = str(uuid.uuid3(uuid.NAMESPACE_DNS, data.cust_loginname))
    passwd = Util.setPass(id,data.cust_name)
    crudUser.add_Cust(db, id,addr,data.cust_name,data.cust_phone,data.cust_loginname,passwd[1])
    return passwd[0]


class Delcust(BaseModel):
    id:str = None


@router.post("/DelCust")
async def Del_cust(request_data: Delcust,db: Session = Depends(get_db)):
    crudUser.del_Custone(db, request_data.id)





