from models.Geral import Session
from models.Employeer import Employeer

def cadastrar_usuario(fullname, email, cpf_input, password, confirm_password):
    session = Session()
    try:
        usuario_existente = session.query(Employeer).filter(Employeer.login == email).first()
        if usuario_existente:
            return False, "Este e-mail já está cadastrado!"

        employeer = Employeer()
        employeer.nome = fullname      
        employeer.login = email        
        employeer.cpf = cpf_input 
        employeer.password = password
        employeer.cpassword = confirm_password 

        if employeer.password != employeer.cpassword:
            return False, "A senha e a confirmação de senha devem ser iguais."
        
        session.add(employeer)
        session.commit()
        return True, "Usuário cadastrado com sucesso!"
        
    except Exception as e:
        session.rollback()
        print("❌ ERRO REAL DO MYSQL:", str(e))
        return False, "Erro ao cadastrar usuário no banco de dados."
    finally:
        session.close()