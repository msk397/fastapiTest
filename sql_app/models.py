# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'admin'

    admin_id = Column(String(40), primary_key=True, nullable=False, index=True)
    admin_loginname = Column(String(20), primary_key=True, nullable=False)
    admin_realname = Column(String(50), nullable=False)
    admin_password = Column(String(40), nullable=False)
    admin_phone = Column(String(20), nullable=False)
    admin_addr = Column(String(100))


class Cust(Base):
    __tablename__ = 'cust'

    cust_id = Column(String(40), primary_key=True)
    cust_loginname = Column(String(40), nullable=False)
    cust_password = Column(String(50), nullable=False)
    cust_name = Column(String(50), nullable=False)
    cust_addr = Column(String(50), nullable=False)
    cust_phone = Column(String(20), nullable=False)


class Charge(Base):
    __tablename__ = 'charge'

    charge_id = Column(String(40), primary_key=True)
    cust_id = Column(ForeignKey('cust.cust_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    charge_status = Column(TINYINT(1), nullable=False, comment='????')
    charge_time = Column(Date)
    charge_cost = Column(Float(10, True), nullable=False)
    charge_ddl = Column(Date, nullable=False, comment='??????')
    charge_memo = Column(String(30), nullable=False, comment='????')

    cust = relationship('Cust')


class Fix(Base):
    __tablename__ = 'fix'

    fix_id = Column(String(50), primary_key=True)
    fix_log = Column(String(500), nullable=False)
    fix_status = Column(TINYINT(1), nullable=False)
    fix_startime = Column(DateTime, nullable=False, comment='?????')
    cust_id = Column(ForeignKey('cust.cust_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    fix_endtime = Column(DateTime)
    admin_id = Column(ForeignKey('admin.admin_id', onupdate='CASCADE'), index=True)
    admin = relationship('Admin')
    cust = relationship('Cust')


class Poster(Base):
    __tablename__ = 'poster'

    poster_id = Column(String(255), primary_key=True)
    poster_title = Column(String(255), nullable=False)
    poster_log = Column(String(5000), nullable=False)
    poster_time = Column(DateTime, nullable=False)
    admin_id = Column(ForeignKey('admin.admin_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='????')

    admin = relationship('Admin')
