from tkinter.constants import RAISED

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from projetosenac.models import Usuario


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Fazer Login')

class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField("Usuário", validators=[DataRequired(), Length(min=3, max=30)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 32)])
    confirmacao_senha = PasswordField("Confirme a senha", validators=[DataRequired(), EqualTo('senha')])
    botao_confirmacao = SubmitField('Confirmar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email já cadastrado. Faça Login para continuar")

class FormFoto(FlaskForm):
    foto = FileField ('Foto', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Confirmar')