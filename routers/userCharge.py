from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sql_app.crud import crudUser
from sql_app.database import SessionLocal

router = APIRouter(
    prefix="/userCharge",
)

class Charge(BaseModel):
    charge_cost: str = None
    charge_ddl: str = None
    charge_id: str = None
    charge_memo: str = None
    charge_status: str = None
    charge_time: str = None
    cust_id: str = None
    cust_name:str = None
    status: bool

def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/queryUserCharge")
async def quer_user_charge(db: Session = Depends(get_db)):
    data = crudUser.get_charge(db)
    message = []
    for i in data:
        mid = i[0].__dict__
        mid.pop('_sa_instance_state')
        mid['cust_name']=i[1]
        if mid['charge_status']==0:
            mid['charge_status']="未缴费"
            mid['status']=False
        else:
            mid['charge_status'] = "已缴费"
            mid['status'] = True
        mid['charge_ddl'] = str(mid['charge_ddl'])
        mid['charge_time'] = str(mid['charge_time'])
        message.append(mid)
    return message

@router.get("/queryCustName")
async def quer_Cust_Name(db: Session = Depends(get_db)):
    data = crudUser.get_Cust(db)
    message=[]
    for i in data:
        i = i.__dict__
        i.pop('_sa_instance_state')
        print(i)
        message.append(i['cust_name'])
    print(message)
    return message



@router.post("/changeCharge")
async def change_charge(request_data: Charge,db: Session = Depends(get_db)):
    charge_cost =request_data.charge_cost
    charge_ddl =request_data. charge_ddl
    charge_id =request_data. charge_id
    charge_memo =request_data. charge_memo
    charge_status =request_data. charge_status
    charge_time =request_data. charge_time
    cust_id =request_data.cust_id
    cust_name =request_data.cust_name
    status =request_data.status
    if status:
        charge_status = 1
    else:
        charge_status = 0
    crudUser.change_Charge(db, charge_id,charge_memo,charge_ddl,charge_cost,charge_status)
    return {"mess": "修改成功"}