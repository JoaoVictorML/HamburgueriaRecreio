from models.Geral import Session
from models.User import User
from sqlalchemy import func

class UserRepository:
    @classmethod
    def authenticate(cls, email, password):
        session = Session()
        try:
            email_limpo = email.strip().lower()
            user = session.query(User).filter(func.lower(User.login) == email_limpo).first()
            
            if not user:
                print(f"DEBUG: E-mail não encontrado no banco: '{email_limpo}'")
                return None
            
            senha_banco = str(user.password).strip()
            senha_digitada = str(password).strip()
            
            if senha_banco == senha_digitada:
                print("DEBUG: Senha correta!")
                return user
            else:
                print(f"DEBUG: Senha incorreta! Banco: '{senha_banco}' | Digitada: '{senha_digitada}'")
                return None
        finally:
            session.close()