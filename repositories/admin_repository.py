from decimal import Decimal, InvalidOperation
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from models.Geral import Session
from models.Admin import Admin


def _parse_salario(valor):
    try:
        return Decimal(str(valor or "0").replace(",", "."))
    except InvalidOperation:
        return None


class AdminRepository:

    @staticmethod
    def list_all():
        with Session() as db:
            return [a.to_dict() for a in db.query(Admin).order_by(Admin.nome).all()]

    @staticmethod
    def find_by_id(admin_id):
        with Session() as db:
            admin = db.get(Admin, admin_id)
            return admin.to_dict() if admin else None

    @staticmethod
    def create(data):
        """Retorna (True, dict) ou (False, mensagem_de_erro)."""
        nome = (data.get("nome") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        salario = _parse_salario(data.get("salario"))

        if not nome or not email or not password:
            return False, "Nome, e-mail e senha são obrigatórios."
        if len(password) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres."
        if salario is None or salario < 0:
            return False, "Salário inválido."

        with Session() as db:
            admin = Admin(
                nome=nome,
                email=email,
                password=generate_password_hash(password),
                cargo=(data.get("cargo") or "Administrador").strip(),
                salario=salario,
                telefone=(data.get("telefone") or "").strip(),
                ativo=bool(data.get("ativo", True)),
            )
            db.add(admin)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                return False, "Já existe um admin com esse e-mail."
            return True, admin.to_dict()

    @staticmethod
    def update(admin_id, data):
        nome = (data.get("nome") or "").strip()
        email = (data.get("email") or "").strip().lower()
        salario = _parse_salario(data.get("salario"))
        password = data.get("password") or ""

        if not nome or not email:
            return False, "Nome e e-mail são obrigatórios."
        if salario is None or salario < 0:
            return False, "Salário inválido."
        if password and len(password) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres."

        with Session() as db:
            admin = db.get(Admin, admin_id)
            if not admin:
                return False, "Admin não encontrado."

            admin.nome = nome
            admin.email = email
            admin.cargo = (data.get("cargo") or "Administrador").strip()
            admin.salario = salario
            admin.telefone = (data.get("telefone") or "").strip()
            admin.ativo = bool(data.get("ativo", False))
            if password:  # só troca a senha se algo foi digitado
                admin.password = generate_password_hash(password)

            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                return False, "Já existe um admin com esse e-mail."
            return True, admin.to_dict()

    @staticmethod
    def delete(admin_id):
        with Session() as db:
            admin = db.get(Admin, admin_id)
            if not admin:
                return False
            db.delete(admin)
            db.commit()
            return True

    @staticmethod
    def authenticate(email, password):
        """Devolve o dict do admin se e-mail/senha estiverem certos e ele estiver ativo."""
        email = (email or "").strip().lower()
        with Session() as db:
            admin = db.query(Admin).filter(func.lower(Admin.email) == email).first()
            if admin and admin.ativo and check_password_hash(admin.password, password or ""):
                return admin.to_dict()
        return None