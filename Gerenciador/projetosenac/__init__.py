from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Criando o app Flask
app = Flask(__name__)

# Configurações do app
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Gerenciador.db'
app.config["SECRET_KEY"] = "144b35e7d055a510ab3890fb5be86294"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"  # pasta onde as fotos vão ser salvas

# Criando as extensões
db = SQLAlchemy(app)
database = db              # usando o mesmo objeto para não conflitar
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"  # rota que o usuário vai ser redirecionado se não estiver logado

# Importando as rotas e modelos (tem que ser no final para evitar import circular)
from projetosenac import routes
from projetosenac.models import Usuario, Foto
