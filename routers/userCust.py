import uuid
from fastapi import APIRouter, Depends,UploadFile,File
import xlrd
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
    id = request_data.id[0:8]
    name = request_data.name
    passwd =id+Util.FirstPinyin(name)
    md5Pass = Util.MD5(passwd)
    crudUser.resetCustPass(db,request_data.id,md5Pass)
    return "已将密码重置为："+passwd


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
    getdata = crudCommon.get_custnameid(db, data.cust_name,data.cust_id)
    if getdata != None:
        return "姓名重复，请重新设置"
    getdata = crudCommon.get_custaddrid(db, addr,data.cust_id)
    if getdata != None:
        return "该地址已有业主，请重新设置"
    crudUser.change_Cust(db, data.cust_id, addr,data.cust_name,data.cust_phone)
    return "修改成功"


class AddCust(BaseModel):
    cust_floor: str = None
    cust_unit: str = None
    cust_door: str = None
    cust_name: str = None
    cust_phone: str = None
    cust_loginname: str = None


@router.post("/AddCust")
async def AddCust(data:AddCust,db:Session = Depends(get_db)):
    addr = data.cust_floor + '-' + data.cust_unit + '-' + data.cust_door
    getdata = crudCommon.get_custlogin(db, data.cust_loginname)
    mess=""
    if getdata != None:
        return "用户名重复请重新设置"
    getdata = crudCommon.get_custaddr(db, addr)
    if getdata !=None:
        return "该地址已有业主，请重新设置"
    getdata = crudCommon.get_custname(db, data.cust_name)
    if getdata != None:
        mess = "有业主重名，已将该业主命名为"+data.cust_name+addr+","
        data.cust_name = data.cust_name+addr
    id = str(uuid.uuid4())
    passwd = Util.setPass(id,data.cust_name)
    crudUser.add_Cust(db, id,addr,data.cust_name,data.cust_phone,data.cust_loginname,passwd[1])
    return mess+"密码为："+passwd[0]


class Delcust(BaseModel):
    id:str = None


@router.post("/DelCust")
async def Del_cust(request_data: Delcust,db: Session = Depends(get_db)):
    data = crudUser.del_CustConfirm(db, request_data.id)
    if data ==0:
        crudUser.del_Custone(db, request_data.id)
        return "删除成功"
    return "该用户在缴费或维修项目有未完成的事项，请处理完毕再删除"


@router.post("/addmore")
async def addmore(file: UploadFile = File(...),db: Session = Depends(get_db)):
    mess=[]
    f = await file.read()
    data = xlrd.open_workbook(file_contents=f)
    names = data.sheet_names()  # 返回表格中所有工作表的名字
    for sheet_name in names:
        status = data.sheet_loaded(sheet_name)  # 检查sheet1是否导入完毕
        if status is True:
            table = data.sheet_by_name(sheet_name)
            keys = ['login','name','floor','unit','door','phone']
            if keys:
                rowNum = table.nrows  # 获取该sheet中的有效行数
                colNum = table.ncols  # 获取该sheet中的有效列数
                if rowNum == 0 or colNum == 0:
                    continue
                else:
                    for i in range(1, rowNum):  # 从第二行（数据行）开始取数据
                        sheet_data = {}  # 定义一个字典用来存放对应数据
                        for j in range(colNum):  # j对应列值
                            sheet_data[keys[j]] = table.row_values(i)[j]  # 把第i行第j列的值取出赋给第j列的键值，构成字典
                        messs={}
                        sheet_data['floor']= '%.0lf'% sheet_data['floor']
                        sheet_data['door'] = '%.0lf' % sheet_data['door']
                        sheet_data['phone'] = '%.0lf' % sheet_data['phone']
                        addr = sheet_data['floor'] + '-' + sheet_data['unit'] + '-' + sheet_data['door']
                        getdata = crudCommon.get_custlogin(db, sheet_data['login'])
                        if getdata != None:
                            messs['mess']=(sheet_data['name']+"的用户名重复请重新设置\n")
                            mess.append(messs)
                            continue
                        getdata = crudCommon.get_custaddr(db, addr)
                        if getdata != None:
                            messs['mess']=(sheet_data['name']+"的地址已有业主，请重新设置\n")
                            mess.append(messs)
                            continue
                        getdata = crudCommon.get_custname(db,sheet_data['name'])
                        if getdata != None:
                            messs['mess']=(sheet_data['name']+"业主重名，已将该业主命名为" + sheet_data['name'] + addr + ",")
                            mess.append(messs)
                            sheet_data['name'] = sheet_data['name'] + addr
                        id = str(uuid.uuid4())
                        passwd = Util.setPass(id, sheet_data['name'])
                        crudUser.add_Cust(db, id, addr, sheet_data['name'], sheet_data['phone'], sheet_data['login'], passwd[1])
                        messs['mess']= (sheet_data['name']+"密码为：" + passwd[0])
                        mess.append(messs)
                        mess+='\n'
    return mess