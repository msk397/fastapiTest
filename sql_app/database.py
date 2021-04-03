 # database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# 使用mysqlclient的情况
SQLALCHEMY_DATABASE_URL = "mysql://root:MChx199937@sh-cynosdbmysql-grp-rymc0t26.sql.tencentcdb.com:25970/property?charset=utf8"
# 使用pymysql
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/数据库名?charset=utf8"
from sqlalchemy.orm import sessionmaker

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()