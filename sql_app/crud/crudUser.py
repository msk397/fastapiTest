from sqlalchemy.orm import Session
from sql_app import models
def get_charge(db:Session):
    return db.query(models.Charge,models.Cust.cust_name,models.Cust.cust_addr)\
        .join( models.Cust, models.Charge.cust_id==models.Cust.cust_id ).all()

def get_Cust(db:Session):
    return db.query(models.Cust)\
       .all()


def change_Charge(db, charge_id, charge_memo, charge_ddl, charge_cost, charge_status):
    db.query(models.Charge).filter(models.Charge.charge_id == charge_id).update({
        'charge_memo':charge_memo,
        'charge_ddl':charge_ddl,
        'charge_cost':charge_cost,
        'charge_status':charge_status
    })
    db.commit()


def add_Charge(db, id, memo, dl, cost, status, time, cu_id):
    charge = models.Charge(charge_id = id,charge_memo = memo,
                           charge_ddl=dl,charge_status=status,charge_cost = cost,
                           charge_time=time,cust_id = cu_id)
    db.add(charge)
    db.commit()

def del_chargeone(db: Session, id: str):
    db.query(models.Charge).filter(models.Charge.charge_id== id).delete()
    db.commit()


def change_Poster(db, poster_id, poster_log, poster_title, poster_time,endtime):
    db.query(models.Poster).filter(models.Poster.poster_id == poster_id).update({
        'poster_log': poster_log,
        'poster_title': poster_title,
        'poster_time':  poster_time,
        'poster_endtime':endtime,
    })
    db.commit()


def add_Poster(db, id, log, title, time,ad_id,endtime,status):
    poster = models.Poster(poster_id=id, poster_log = log,
                           poster_title = title,poster_time = time,
                           admin_id = ad_id,poster_endtime = endtime,
                           poster_status = status)
    db.add(poster)
    db.commit()


def del_posterone(db, id):
    db.query(models.Poster).filter(models.Poster.poster_id == id).delete()
    db.commit()

def get_fix(db:Session):
    return db.query(models.Fix,models.Cust.cust_name,models.Admin.admin_realname,models.Admin.admin_loginname,models.Cust.cust_addr)\
        .join( models.Cust, models.Fix.cust_id==models.Cust.cust_id ) \
        .join(models.Admin, models.Fix.admin_id == models.Admin.admin_id) \
        .all()


def del_fixone(db, id):
    db.query(models.Fix).filter(models.Fix.fix_id == id).delete()
    db.commit()


def change_fix(db, id, end, start, log, admin_id, fix_status):
    db.query(models.Fix).filter(models.Fix.fix_id == id).update({
        'fix_log':log,
        'fix_status':fix_status,
        'fix_startime':start,
        'fix_endtime':end,
        'admin_id':admin_id,
    })
    db.commit()

def get_custmess(db):
    return db.query(models.Cust).all()


def resetCustPass(db, id, md5Pass):
    db.query(models.Cust).filter(models.Cust.cust_id == id).update({
        'cust_password':md5Pass,
    })
    db.commit()


def change_Cust(db, id, addr, name, phone):
    db.query(models.Cust).filter(models.Cust.cust_id == id).update({
        'cust_addr':addr,
        'cust_name':name,
        'cust_phone':phone,
    })
    db.commit()


def add_Cust(db, id, addr, name, phone, loginname, param):
    cust = models.Cust(cust_id=id, cust_loginname=loginname,
                       cust_addr=addr,cust_name=name,
                       cust_phone=phone,cust_password=param)
    db.add(cust)
    db.commit()


def del_Custone(db, id):
    db.query(models.Cust).filter(models.Cust.cust_id == id).delete()
    db.commit()


def change_Posterpost(db, poster_id, time):
    db.query(models.Poster).filter(models.Poster.poster_id == poster_id).update({
        'poster_time': time,
    })
    db.commit()


def get_adminmess(db):
    return db.query(models.Admin)\
        .filter(models.Admin.admin_id!="null")\
        .filter(models.Admin.admin_id != "root")\
        .all()


def del_adminone(db, login):
    db.query(models.Admin).filter(models.Admin.admin_loginname == login).delete()
    db.commit()


def add_admin(db, id, addr,name, phone, loginname, param):
    cust = models.Admin(admin_id=id, admin_loginname=loginname,
                       admin_addr=addr, admin_realname=name,
                       admin_phone=phone, admin_password=param)
    db.add(cust)
    db.commit()


def change_Admin(db, addr, phone, login, name):
    db.query(models.Admin).filter(models.Admin.admin_loginname == login).update({
        'admin_addr': addr,
        'admin_realname': name,
        'admin_phone': phone,
    })
    db.commit()


def resetAdminPass(db, id, md5Pass):
    db.query(models.Admin).filter(models.Admin.admin_id == id).update({
        'admin_password': md5Pass,
    })
    db.commit()


def del_CustConfirm(db, id):
    a = db.query(models.Fix) \
        .filter(models.Fix.fix_status == 0)\
        .filter(models.Fix.cust_id == id)\
        .count()
    b = db.query(models.Charge) \
        .filter(models.Charge.charge_status == 0)\
        .filter(models.Charge.cust_id == id)\
        .count()
    return a+b


def change_Postersign(db, id):
    db.query(models.Poster).filter(models.Poster.poster_id == id).update({
        'poster_status': 1,
    })
    db.commit()