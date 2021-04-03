from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
router = APIRouter(
    prefix="/common",
)

class Item(BaseModel):
    choose: str=None
    account: str = None
    passwd: str = None

@router.post("/signin")
async def signin(request_data: Item):
    a = request_data.choose
    b = request_data.account
    c = request_data.passwd
    print(a,b,c)
    result = {'a': a, 'b': b, 'c': c}
    return result

