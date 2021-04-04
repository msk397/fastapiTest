from sqlalchemy.orm import Session
from . import models


def get_admin(db:Session,admin_loginname:str):
    return db.query(models.Admin).filter(models.Admin.admin_loginname == admin_loginname).first()

def get_cust(db:Session,cust_loginname:str):
    return db.query(models.Cust).filter(models.Cust.cust_loginname == cust_loginname).first()

def get_gene_by_name(db: Session, gene_name: str):
    return db.query(models.Gene).filter(models.Gene.gene == gene_name).first()


def get_genes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Gene).offset(skip).limit(limit).all()



def delete_gene(db: Session, gene_id: int):
    db.query(models.Gene).filter(models.Gene.id == gene_id).delete()
    db.commit()
    return {'Result': '删除成功'}