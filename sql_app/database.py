 # database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 使用mysqlclient的情况
SQLALCHEMY_DATABASE_URL = "mysql://root:MC@sh-cynosdbmysql-grp-.sql.tencentcdb.com:250/property?charset=utf8"
#sqlacodegen --outfile=models.py mysql://root:M@sh-cynosdbmysql-grp.sql.tencentcdb.com:20/property
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
