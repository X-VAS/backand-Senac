from projetosenac import app, database, login_manager
from datetime import datetime
from flask_login import UserMixin


# Função que o flask_login chama para buscar o usuário pelo id
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


# Tabela de usuários
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    # relacionamento com a tabela Foto
    fotos = database.relationship("Foto", backref="usuario", lazy=True)


# Tabela de fotos
class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")  # nome do arquivo salvo
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)
