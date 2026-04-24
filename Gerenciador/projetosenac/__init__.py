from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Gerenciador.db'
app.config["SECRET_KEY"] = "144b35e7d055a510ab3890fb5be86294"
app.config["UPLOUD_FOLDER"] = "static/fotos_posts"


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "Gerenciador"

from projetosenac import routes
from projetosenac.models import Usuario, Foto
