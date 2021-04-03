import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from sql_app import crud
from sql_app.database import SessionLocal
router = APIRouter(
    prefix="/common",
)

def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Item(BaseModel):
    choose: str=None
    account: str = None
    passwd: str = None

@router.post("/signin")
async def signin(request_data: Item,db: Session = Depends(get_db)):
    choose = request_data.choose
    account = request_data.account
    passwd = request_data.passwd
    data = crud.get_admin(db,account).__dict__
    data.pop('_sa_instance_state')
    return json.dumps(data,separators=(',',':'))



