from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask import Markup
import models
from __init__ import app, db


auth = Blueprint('auth', __name__)

#################################################################
#Rota para renderizar login
@auth.route('/login')
def login():    
    return render_template('index.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    senha = request.form.get('senha')
    lembrar = True if request.form.get('lembrar') else False
    
    usuario = models.Pessoas.query.filter_by(email=email).first()
    

    if not usuario or not check_password_hash(usuario.senha, senha):
        message = Markup('<h5><font color="#FFFF00">Email ou senha incorretos. Por favor, confira seus dados de usuário e tente novamente ou cadastra-se</font></h5>')
        flash(message)
        return redirect(url_for('auth.login'))
    

    # Se os requisitos acima forem atendidos redireciona para área logada
    login_user(usuario, remember=lembrar)
    return redirect(url_for('main.profile'))

#############################################################
#rota para formulário de cadastro
@auth.route('/addcliente')
def add_cliente():
    return render_template('addcliente.html')

@auth.route('/addcliente', methods=['POST'])
def add_cliente_post():
    nome = request.form.get('nome')
    email = request.form.get('email')
    rg = request.form.get('rg')
    cpf = request.form.get('cpf')
    tipo = request.form.get('tipo')
    senha = request.form.get('senha')

    pessoa = models.Pessoas.query.filter_by(email=email).first()

    if pessoa:
        message = Markup('<h5><font color="#FFFF00">O endereço de e-mail já existe. Faça login</font></h5>')
        flash(message)
        return redirect(url_for('auth.login'))

    novo_usuario = models.Pessoas(nome=nome, email=email, rg=rg, cpf=cpf, tipo=tipo, senha=generate_password_hash(senha, method='sha256'))
    db.session.add(novo_usuario)
    db.session.commit()

    return render_template('index.html')
####################################################

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))