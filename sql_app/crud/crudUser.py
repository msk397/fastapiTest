from sqlalchemy.orm import Session
from sql_app import models
def get_charge(db:Session):
    return db.query(models.Charge,models.Cust.cust_name).join( models.Cust, models.Charge.cust_id==models.Cust.cust_id ).all()