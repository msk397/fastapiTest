 # database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 使用mysqlclient的情况
SQLALCHEMY_DATABASE_URL = "mysql://root:MChx199937@sh-cynosdbmysql-grp-rymc0t26.sql.tencentcdb.com:25970/property?charset=utf8"
#sqlacodegen --outfile=models.py mysql://root:MChx199937@sh-cynosdbmysql-grp-rymc0t26.sql.tencentcdb.com:25970/property
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
