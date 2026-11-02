from models.Geral import Base, engine
from models.Admin import Admin
from repositories.admin_repository import AdminRepository

Base.metadata.create_all(engine)

ok, result = AdminRepository.create({
    "nome": "Administrador",
    "email": "administrator@gmail.com",
    "password": "admi123",
    "cargo": "Administrador",
    "salario": "0",
    "telefone": "",
    "ativo": True,
})
print("Criado!" if ok else f"Erro: {result}")