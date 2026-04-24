from flask_login import login_required, login_user, logout_user, current_user
from projetosenac import app, database, bcrypt
from flask import render_template, url_for, redirect
from projetosenac.forms import FormLogin, FormCriarConta
from projetosenac.models import Usuario, Foto

# - criar conta -----------------------------------------------
@app.route('/criar-conta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()

    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, email=formcriarconta.email.data, senha=senha)

        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('criarconta.html', form=formcriarconta)

# - Login -----------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('homepage.html', form=formlogin)

# - PERFIL -----------------------------------------------
@app.route('/perfil/<id_usuario>')
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # o usuário está vendo o perfil dele
        return render_template('perfil.html', usuario=current_user)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario)

# - Sair -----------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))



