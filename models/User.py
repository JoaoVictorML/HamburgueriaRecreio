from sqlalchemy import Column, Integer, String
from models.Geral import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    login = Column(String(150), nullable=False, unique=True)
    cpf = Column(String(14), nullable=False)
    password = Column(String(150), nullable=False)

    def __init__(self):
        self.cpassword = None