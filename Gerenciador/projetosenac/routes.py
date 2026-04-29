import os
from flask_login import login_required, login_user, logout_user, current_user
from projetosenac import app, database, bcrypt
from flask import render_template, url_for, redirect, request
from projetosenac.forms import FormLogin, FormCriarConta, FormFoto
from projetosenac.models import Usuario, Foto


# ── CRIAR CONTA ──────────────────────────────────────────────
@app.route('/criar-conta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()

    if formcriarconta.validate_on_submit():
        # Criptografando a senha antes de salvar
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)

        # Criando o usuário e salvando no banco
        usuario = Usuario(
            username=formcriarconta.username.data,
            email=formcriarconta.email.data,
            senha=senha
        )
        database.session.add(usuario)
        database.session.commit()

        # Já deixa o usuário logado depois de criar a conta
        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('criarconta.html', form=formcriarconta)


# ── LOGIN / HOMEPAGE ──────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()

    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()

        # Verificando se o usuário existe e a senha está correta
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('homepage.html', form=formlogin)


# ── PERFIL ────────────────────────────────────────────────────
@app.route('/perfil/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):

    # Verificando se o usuário está vendo o perfil DELE ou de OUTRO usuário
    if id_usuario == current_user.id:
        # É o próprio usuário: mostra o formulário de foto
        usuario = current_user
        form_foto = FormFoto()

        if form_foto.validate_on_submit():
            # Pegando o arquivo enviado pelo formulário
            arquivo = form_foto.foto.data

            # Criando um nome único para o arquivo usando o id do usuário
            nome_arquivo = f"usuario_{usuario.id}.{arquivo.filename.rsplit('.', 1)[1]}"

            # Montando o caminho completo onde a foto vai ser salva
            caminho = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                nome_arquivo
            )

            # Salvando o arquivo no disco
            arquivo.save(caminho)

            # Salvando o nome da foto no banco de dados
            foto = Foto(imagem=nome_arquivo, id_usuario=usuario.id)
            database.session.add(foto)
            database.session.commit()

            return redirect(url_for('perfil', id_usuario=usuario.id))

        return render_template('perfil.html', usuario=usuario, form=form_foto)

    else:
        # Outro usuário: não mostra o formulário de foto
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)


# ── LOGOUT ────────────────────────────────────────────────────
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))
