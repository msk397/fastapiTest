import datetime
import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sql_app.crud import crudCommon, crudUser
from sql_app.database import SessionLocal

router = APIRouter(
    prefix="/userPoster",
)
#poster_log":"","poster_id":"345","admin_id":"123","poster_time":"15:47",
# "poster_title":"消防检查","admin_name":"阿斯顿","poster_date":"2021-04-21","status":"已发布"}
class Poster(BaseModel):
    poster_log: str = None
    poster_id: str = None
    admin_id: str = None
    poster_time: str = None
    poster_title: str = None
    admin_name: str = None
    poster_date: str = None
    status: str = None
    poster_enddate: str = None
    poster_endtime: str = None

class AddPoster(BaseModel):
    poster_log: str = None
    poster_title: str = None
    admin_name: str = None
    poster_date: str = None
    poster_time: str = None
    poster_enddate: str = None
    poster_endtime: str = None

class DelPoster(BaseModel):
    poster_id: str = None
def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/queryPoster")
async def query_poster(db: Session = Depends(get_db)):
    data = crudCommon.get_poster(db)
    message = []
    for i in data:
        mid = i[0].__dict__
        mid.pop('_sa_instance_state')
        mid['admin_name']=i[1]
        mid.pop('admin_id')
        time  = datetime.datetime.now().replace(microsecond=0) - mid['poster_time']
        time =time.days * 86400 + time.seconds
        if time >= 0:
            endtime = datetime.datetime.now().replace(microsecond=0) - mid['poster_endtime']
            endtime = endtime.days * 86400 + endtime.seconds
            if endtime>=0:
                mid['status']="已过期"
            else:
                mid['status'] = "已发布"
        else:
            mid['status'] = "未发布"
        mid['poster_date'] = mid['poster_time'].strftime('%Y-%m-%d')
        mid['poster_time'] = mid['poster_time'].strftime('%H:%M')
        mid['poster_enddate'] = mid['poster_endtime'].strftime('%Y-%m-%d')
        mid['poster_endtime'] = mid['poster_endtime'].strftime('%H:%M')
        mid['time'] = mid['poster_date']+" "+mid['poster_time']
        mid['endtime'] = mid['poster_enddate'] + " " + mid['poster_endtime']
        message.append(mid)
    return message

@router.post("/changePoster")
async def change_poster(request_data: Poster,db: Session = Depends(get_db)):
    poster_log=request_data.poster_log
    poster_id=request_data.poster_id
    poster_time=request_data.poster_time
    poster_title=request_data.poster_title
    poster_date = request_data.poster_date
    poster_time = poster_date +' '+poster_time+':00'
    poster_time= datetime.datetime.strptime(poster_time, '%Y-%m-%d %H:%M:%S')
    poster_enddate = request_data.poster_enddate
    poster_endtime = request_data.poster_endtime
    poster_endtime = poster_enddate + ' ' + poster_endtime + ':00'
    poster_endtime = datetime.datetime.strptime(poster_endtime, '%Y-%m-%d %H:%M:%S')
    time = poster_endtime-poster_time
    time = time.days * 86400 + time.seconds
    if time>0:
        crudUser.change_Poster(db, poster_id, poster_log, poster_title, poster_time, poster_endtime)
        return {"mess": "修改成功"}
    else:
        return {"mess": "截止时间需大于发布时间"}



@router.post("/AddPoster")
async def Add_poster(request_data: AddPoster,db: Session = Depends(get_db)):
    poster_log=request_data.poster_log
    admin_name = request_data.admin_name
    poster_title=request_data.poster_title
    poster_date = request_data.poster_date
    poster_time = request_data.poster_time
    poster_time = poster_date + ' ' + poster_time + ':00'
    poster_time = datetime.datetime.strptime(poster_time, '%Y-%m-%d %H:%M:%S')
    poster_enddate = request_data.poster_enddate
    poster_endtime = request_data.poster_endtime
    poster_endtime = poster_enddate + ' ' + poster_endtime + ':00'
    poster_endtime = datetime.datetime.strptime(poster_endtime, '%Y-%m-%d %H:%M:%S')
    poster_id = str(uuid.uuid4())
    admin_id = crudCommon.get_adminid(db, admin_name)
    time = poster_endtime-poster_time
    time = time.days * 86400 + time.seconds
    if time>0:
        crudUser.add_Poster(db, poster_id, poster_log,poster_title,poster_time,admin_id[0],poster_endtime)
        return {"mess": "添加成功"}
    else:
        return {"mess": "截止时间需大于发布时间"}

@router.post("/DelPoster")
async def Del_Poster(request_data: DelPoster,db: Session = Depends(get_db)):
    crudUser.del_posterone(db, request_data.poster_id)
