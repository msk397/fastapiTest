#from fastapi import Depends, FastAPI
from fastapi import FastAPI
#from .dependencies import get_query_token, get_token_header
from routers import cust, user
import uvicorn
from internal import admin
#app = FastAPI(dependencies=[Depends(get_query_token)])

app = FastAPI()
app.include_router(user.router)
app.include_router(cust.router)
app.include_router(
    admin.router,
    prefix="/admin",
    #tags=["admin"],
    #dependencies=[Depends(get_token_header)],
   # responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)