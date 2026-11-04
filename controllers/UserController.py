from models.Geral import Session
from models.User import User

def cadastrar_usuario(fullname, email, cpf_input, password, confirm_password):
    session = Session()
    try:
        usuario_existente = session.query(User).filter(User.login == email).first()
        if usuario_existente:
            return False, "Este e-mail já está cadastrado!"

        user = User()
        user.nome = fullname      
        user.login = email        
        user.cpf = cpf_input 
        user.password = password
        user.cpassword = confirm_password 

        if user.password != user.cpassword:
            return False, "A senha e a confirmação de senha devem ser iguais."
        
        session.add(user)
        session.commit()
        return True, "Usuário cadastrado com sucesso!"
        
    except Exception as e:
        session.rollback()
        print("❌ ERRO REAL DO MYSQL:", str(e))
        return False, "Erro ao cadastrar usuário no banco de dados."
    finally:
        session.close()