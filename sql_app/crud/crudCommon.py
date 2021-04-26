from sqlalchemy.orm import Session
from sql_app import models
from sqlalchemy import func

#user
def get_admin(db:Session, admin_loginname:str):
    return db.query(models.Admin).filter(models.Admin.admin_loginname == admin_loginname).first()

def save_admin(db:Session,login:str,real:str,addr:str,phone:str):
    db.query(models.Admin).filter(models.Admin.admin_loginname == login).update({
        'admin_realname': real,
        'admin_phone': phone,
        'admin_addr': addr,
    })
    db.commit()

def change_user_pass(db, login, newPass):
    db.query(models.Admin).filter(models.Admin.admin_loginname == login).update({
        'admin_password': newPass,
    })
    db.commit()

def get_adminid(db, admin_name):
    return db.query(models.Admin.admin_id).filter(models.Admin.admin_realname == admin_name).first()

def get_userid(db, login):
    return db.query(models.Admin.admin_id).filter(models.Admin.admin_loginname == login).first()

def get_userPass(db,login):
    return db.query(models.Admin.admin_password).filter(models.Admin.admin_loginname == login).first()

#cust
def get_cust(db:Session,cust_loginname:str):
    return db.query(models.Cust).filter(models.Cust.cust_loginname == cust_loginname).first()

def get_custid(db:Session,cust_name:str):
    return db.query(models.Cust.cust_id).filter(models.Cust.cust_name == cust_name).first()

def get_custlogin(db, login):
    return db.query(models.Cust.cust_loginname).filter(models.Cust.cust_loginname == login).first()

def get_poster(db):
    return db.query(models.Poster, models.Admin.admin_realname) \
        .join(models.Admin, models.Poster.admin_id == models.Admin.admin_id).all()


def getCustNum(db):
    return db.query(models.Cust).count()


def getmoneyfail(db, time):
    return db.query(func.sum(models.Charge.charge_cost)).filter(models.Charge.charge_time==time)\
        .filter(models.Charge.charge_status==0).scalar()


def getmoneysucc(db, time):
    return db.query(func.sum(models.Charge.charge_cost)).filter(models.Charge.charge_time == time) \
        .filter(models.Charge.charge_status == 1).scalar()


def getfixsucc(db):
    return db.query(models.Fix).filter(models.Fix.fix_status == 1).count()


def getfixfail(db):
    return db.query(models.Fix).filter(models.Fix.fix_status == 0).count()


def getmoney(db):
    return db.query(models.Cust.cust_name,models.Charge)\
        .join( models.Cust, models.Charge.cust_id==models.Cust.cust_id )\
        .filter(models.Charge.charge_status == 0)\
        .order_by(models.Charge.charge_ddl).all()


def gettodayfix(db):
    return db.query(models.Cust.cust_name, models.Fix,models.Cust.cust_addr) \
        .join(models.Cust, models.Fix.cust_id == models.Cust.cust_id) \
        .filter(models.Fix.fix_status == 0) \
        .order_by(models.Fix.fix_startime).all()