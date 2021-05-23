#from fastapi import Depends, FastAPI
from fastapi import FastAPI
#from .dependencies import get_query_token, get_token_header
from routers import cust, common, user, userCharge,userPoster,userFix,userCust,fixer
from internal import admin
from fastapi.middleware.cors import CORSMiddleware
#app = FastAPI(dependencies=[Depends(get_query_token)])

app = FastAPI()
app.include_router(user.router)
app.include_router(fixer.router)
app.include_router(userCharge.router)
app.include_router(userPoster.router)
app.include_router(userFix.router)
app.include_router(userCust.router)
app.include_router(cust.router)
app.include_router(common.router)
app.include_router(
    admin.router,
    prefix="/admin",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}