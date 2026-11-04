from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from models.Geral import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)  # guarda o HASH, nunca a senha pura
    cargo = Column(String(100), nullable=False, default="Administrador")
    salario = Column(Numeric(10, 2), nullable=False, default=0)
    telefone = Column(String(20), nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cargo": self.cargo,
            "salario": float(self.salario or 0),
            "telefone": self.telefone,
            "ativo": self.ativo,
            "criado_em": self.criado_em,
        }