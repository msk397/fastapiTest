from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from sql_app import crud
from sql_app.database import SessionLocal

router = APIRouter(
    prefix="/user",
)

class QueryUser(BaseModel):
    name: str = None

def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/queryusermess")
async def queryusermess(request_data: QueryUser,db: Session = Depends(get_db)):
    print(request_data)
    account = request_data.name
    message = {"real": None, "addr": None, "phone": None, "passwd":None}
    data = crud.get_admin(db, account).__dict__
    data.pop('_sa_instance_state')
    message["real"]=data["admin_realname"]
    message["addr"] = data["admin_addr"]
    message["phone"] = data["admin_phone"]
    message["passwd"] = data["admin_password"]
    return message

@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
