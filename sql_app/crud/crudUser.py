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