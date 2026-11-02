from flask import Flask
# 1. Importar Base e engine PRIMEIRO
from models.Geral import Base, engine

# 2. Importar TODOS os modelos ANTES de criar as tabelas
from models.User import User
from models.Admin import Admin  
from models.credito import Emprestimo

# 3. Registar as rotas
from routes.views import views_bp
from routes.api import api_bp
from routes.admin import admin_bp 

# 4. Criar as tabelas NO BANCO (Agora o SQLAlchemy conhece User e Emprestimo)
Base.metadata.create_all(engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta_ifce'

# 5. Registrar Blueprints
app.register_blueprint(views_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)  