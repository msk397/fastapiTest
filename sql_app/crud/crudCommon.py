from sqlalchemy.orm import Session
from sql_app import models

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

def save_cust(db, login, real, phone):
    db.query(models.Cust).filter(models.Cust.cust_loginname == login).update({
        'cust_name': real,
        'cust_phone': phone,
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

def get_postercount(db):
    return db.query(models.Poster).all()


def getCustNum(db):
    return db.query(models.Cust).count()


def getmoneyfail(db, time):
    # return db.query(func.sum(models.Charge.charge_cost)).filter(models.Charge.charge_time==time)\
    #     .filter(models.Charge.charge_status==0).scalar()
    return db.query(models.Charge).filter(models.Charge.charge_status == 0).count()


def getmoneysucc(db, time):
    return db.query(models.Charge).filter(models.Charge.charge_status == 1).count()
    # return db.query(func.sum(models.Charge.charge_cost)).filter(models.Charge.charge_time == time) \
    #     .filter(models.Charge.charge_status == 1).scalar()


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


def getlog(db, id):
    return db.query(models.Log.log_id).filter(models.Log.log_id==id).first()


def addlog(db, id, title, log, cust_id, time, status):
    charge = models.Log(log_id = id,log_title = title,
                        log_log = log,cust_id = cust_id,
                        log_time = time,log_status=status
                        )
    db.add(charge)
    db.commit()


def get_custaddr(db, addr):
    return db.query(models.Cust.cust_loginname).filter(models.Cust.cust_addr == addr).first()


def get_custname(db, name):
    return db.query(models.Cust.cust_loginname).filter(models.Cust.cust_name == name).first()


def get_custaddrid(db, addr, id):
    return db.query(models.Cust.cust_loginname)\
        .filter(models.Cust.cust_addr == addr)\
        .filter(models.Cust.cust_id != id).first()


def get_custnameid(db, name, id):
    return db.query(models.Cust.cust_loginname).filter(models.Cust.cust_name == name).filter(models.Cust.cust_id != id).first()


def get_custPass(db, login):
    return db.query(models.Cust.cust_password).filter(models.Cust.cust_loginname == login).first()


def get_adminlogin(db, login):
    return db.query(models.Admin.admin_loginname).filter(models.Admin.admin_loginname == login).first()


def get_Fixerlogin(db, login):
    return db.query(models.Fixer.login).filter(models.Fixer.login == login).first()


def get_fixer(db, account):
    return db.query(models.Fixer).filter(models.Fixer.login == account).first()


def save_fixer(db, login, name, phone):
    db.query(models.Fixer).filter(models.Fixer.login == login).update({
        'name': name,
        'phone': phone,
    })
    db.commit()
