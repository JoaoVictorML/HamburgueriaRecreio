from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import DataError, PendingRollbackError

engine = create_engine("mysql+pymysql://root:@localhost:3306/cadastro")
Session = sessionmaker(bind=engine)

Base = declarative_base()