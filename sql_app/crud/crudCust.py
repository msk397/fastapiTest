from sqlalchemy.orm import Session
from sql_app import models

def get_custName(db:Session):
    return db.query(models.Cust.cust_name).all()