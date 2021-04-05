# coding: utf-8
from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'admin'

    admin_id = Column(String(40), primary_key=True)
    admin_loginname = Column(String(20), nullable=False)
    admin_realname = Column(String(50), nullable=False)
    admin_password = Column(String(40), nullable=False)
    admin_phone = Column(String(20), nullable=False)
    admin_addr = Column(String(100))


class Charge(Base):
    __tablename__ = 'charge'

    charge_id = Column(String(40), primary_key=True)
    cust_id = Column(String(40), nullable=False)
    charge_status = Column(String(10), nullable=False, comment='????')
    charge_time = Column(DateTime)
    charge_cost = Column(Float(10, True), nullable=False)
    charge_ddl = Column(DateTime, nullable=False, comment='??????')
    charge_memo = Column(String(30), nullable=False, comment='????')


class Cust(Base):
    __tablename__ = 'cust'

    cust_id = Column(String(40), primary_key=True)
    cust_loginname = Column(String(40), nullable=False)
    cust_password = Column(String(50), nullable=False)
    cust_name = Column(String(50), nullable=False)
    cust_addr = Column(String(50), nullable=False)
    cust_phone = Column(String(20), nullable=False)


class Fix(Base):
    __tablename__ = 'fix'

    fix_id = Column(String(50), primary_key=True)
    fix_log = Column(String(500), nullable=False)
    fix_status = Column(String(10), nullable=False)
    fix_time = Column(DateTime, nullable=False, comment='?????')
    cust_id = Column(String(40), nullable=False)


class Poster(Base):
    __tablename__ = 'poster'

    poster_id = Column(String(255), primary_key=True)
    poster_log = Column(String(500), nullable=False)
    poster_time = Column(DateTime, nullable=False)
    poster_people = Column(String(255), nullable=False, comment='????')


class Test(Base):
    __tablename__ = 'test'

    test = Column(String(255), primary_key=True)
