from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from projetosenac.models import Usuario


# Formulário de login
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Fazer Login')


# Formulário de criar conta
class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField("Usuário", validators=[DataRequired(), Length(min=3, max=30)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 32)])
    confirmacao_senha = PasswordField("Confirme a senha", validators=[DataRequired(), EqualTo('senha')])
    botao_confirmacao = SubmitField('Criar conta')

    # Validação personalizada: checa se o email já está cadastrado
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email já cadastrado. Faça Login para continuar")


# Formulário para enviar foto de perfil
class FormFoto(FlaskForm):
    foto = FileField('Foto de perfil', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Somente imagens são permitidas!')
    ])
    botao_confirmacao = SubmitField('Atualizar foto')
