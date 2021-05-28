# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT
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
    admin_root = Column(TINYINT(4), nullable=False)


class Cust(Base):
    __tablename__ = 'cust'

    cust_id = Column(String(40), primary_key=True)
    cust_loginname = Column(String(40), nullable=False)
    cust_password = Column(String(50), nullable=False)
    cust_name = Column(String(50), nullable=False)
    cust_addr = Column(String(50), nullable=False)
    cust_phone = Column(String(20), nullable=False)


class Fixer(Base):
    __tablename__ = 'fixer'

    id = Column(String(255), primary_key=True)
    sort = Column(String(255), nullable=False)
    login = Column(String(255), nullable=False)
    passwd = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)


class Log(Base):
    __tablename__ = 'log'

    log_id = Column(String(50), primary_key=True)
    log_title = Column(String(50), nullable=False)
    log_log = Column(String(500), nullable=False)
    cust_id = Column(String(40), nullable=False, index=True)
    log_time = Column(DateTime, nullable=False)
    log_status = Column(TINYINT(4), nullable=False)


class Charge(Base):
    __tablename__ = 'charge'

    charge_id = Column(String(40), primary_key=True)
    cust_id = Column(ForeignKey('cust.cust_id', onupdate='CASCADE'), nullable=False, index=True)
    charge_status = Column(TINYINT(1), nullable=False, comment='????')
    charge_time = Column(Date)
    charge_cost = Column(Float(10, True), nullable=False)
    charge_ddl = Column(Date, nullable=False, comment='??????')
    charge_memo = Column(String(30), nullable=False, comment='????')

    cust = relationship('Cust')


class Fix(Base):
    __tablename__ = 'fix'

    fix_id = Column(String(50), primary_key=True)
    fix_sort = Column(String(255), nullable=False)
    fix_log = Column(String(500), nullable=False)
    fix_status = Column(TINYINT(1))
    fix_startime = Column(DateTime, nullable=False, comment='?????')
    cust_id = Column(ForeignKey('cust.cust_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    fix_endtime = Column(DateTime)
    admin_id = Column(ForeignKey('admin.admin_id', onupdate='CASCADE'), index=True)
    fixer_id = Column(ForeignKey('fixer.id', onupdate='CASCADE'), index=True)

    admin = relationship('Admin')
    cust = relationship('Cust')
    fixer = relationship('Fixer')


class Poster(Base):
    __tablename__ = 'poster'

    poster_id = Column(String(255), primary_key=True)
    poster_title = Column(String(255), nullable=False)
    poster_log = Column(String(5000), nullable=False)
    poster_time = Column(DateTime, nullable=False)
    admin_id = Column(ForeignKey('admin.admin_id', onupdate='CASCADE'), nullable=False, index=True, comment='????')
    poster_endtime = Column(DateTime, nullable=False)
    poster_status = Column(TINYINT(4))

    admin = relationship('Admin')


class Fixlog(Base):
    __tablename__ = 'fixlog'

    id = Column(ForeignKey('fix.fix_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    log = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    pic = Column(LONGTEXT)
    title = Column(String(255), nullable=False)
    pid = Column(String(255), primary_key=True)

    fix = relationship('Fix')
