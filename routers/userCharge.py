from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sql_app.crud import crudUser
from sql_app.database import SessionLocal

router = APIRouter(
    prefix="/userCharge",
)


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
    j=0
    message = []
    for i in data:
        mid = i[0].__dict__
        mid.pop('_sa_instance_state')
        mid['cust_name']=i[1]
        j+=1
        message.append(mid)
    return message
