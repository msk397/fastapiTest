from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def update_admin():
    return {"message": " post:Admin getting schwifty"}

@router.get("/")
async def update_admin():
    return {"message": "get:Admin getting schwifty"}
