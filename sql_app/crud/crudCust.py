from sqlalchemy.orm import Session
from sql_app import models

def get_custName(db:Session):
    return db.query(models.Cust.cust_name).all()


def getmoney(db,login):
    return db.query(models.Cust.cust_name,models.Charge,models.Cust.cust_loginname)\
        .join( models.Cust, models.Charge.cust_id==models.Cust.cust_id )\
        .filter(models.Charge.charge_status == 0)\
        .filter(models.Cust.cust_loginname==login)\
        .order_by(models.Charge.charge_ddl).all()


def getfix(db, login):
    return db.query(models.Fix,models.Admin.admin_realname,models.Admin.admin_loginname) \
        .join(models.Cust, models.Fix.cust_id == models.Cust.cust_id) \
        .join(models.Admin, models.Fix.admin_id == models.Admin.admin_id) \
        .filter(models.Cust.cust_loginname == login) \
        .order_by(models.Fix.fix_startime).all()



def addFix(db, cus_id, admi_id, id, time, status,log):
    cust = models.Fix(fix_id=id,
                      cust_id = cus_id,
                      admin_id = admi_id,
                      fix_startime = time,
                      fix_status = status,
                      fix_log = log,
                      )
    db.add(cust)
    db.commit()


def getlog(db, data):
    return db.query(models.Log).filter(models.Log.cust_id == data).order_by(models.Log.log_time.desc()).all()


def getlogfail(db, data):
    return db.query(models.Log).filter(models.Log.cust_id == data).filter(models.Log.log_status==0).count()

def getlogsucc(db, data):
    return db.query(models.Log).filter(models.Log.cust_id == data).filter(models.Log.log_status==1).count()


def readmail(id, db):
    db.query(models.Log).filter(models.Log.log_id == id).update({
        'log_status': 1,
    })
    db.commit()


def change_cust_pass(db, login, nP):
    db.query(models.Cust).filter(models.Cust.cust_loginname == login).update({
        'cust_password': nP,
    })
    db.commit()


def paymoney(db, id):
    db.query(models.Charge).filter(models.Charge.charge_id == id).update({
        'charge_status': 1,
    })
    db.commit()