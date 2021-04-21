from sqlalchemy.orm import Session
from sql_app import models
def get_charge(db:Session):
    return db.query(models.Charge,models.Cust.cust_name)\
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


def change_Poster(db, poster_id, poster_log, poster_title, poster_time):
    db.query(models.Poster).filter(models.Poster.poster_id == poster_id).update({
        'poster_log': poster_log,
        'poster_title': poster_title,
        'poster_time':  poster_time,
    })
    db.commit()


def add_Poster(db, id, log, title, time,ad_id):
    poster = models.Poster(poster_id=id, poster_log = log,
                           poster_title = title,poster_time = time,
                           admin_id = ad_id)
    db.add(poster)
    db.commit()