from sqlalchemy.orm import Session
from . import models

def get_gene(db: Session, gene_id: int):
    return db.query(models.Gene).filter(models.Gene.id == gene_id).first()


def get_gene_by_name(db: Session, gene_name: str):
    return db.query(models.Gene).filter(models.Gene.gene == gene_name).first()


def get_genes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Gene).offset(skip).limit(limit).all()



def delete_gene(db: Session, gene_id: int):
    db.query(models.Gene).filter(models.Gene.id == gene_id).delete()
    db.commit()
    return {'Result': '删除成功'}