from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash
from wtforms.validators import Email 

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from app import app, db, bcrypt

from .forms import FormularioDadosPessoais, LoginFormularioCli

from .models import Pessoas
from ..pedidos.models import Pedidos

##################### Rota Usuario ####################################################

#Rota Usuario

@app.route('/minhaconta')
def minhaconta():

    if 'email' not in session:
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('login'))

    cliente = Pessoas.query.filter_by(email=session['email']).first()

    return render_template('clientes/minhaconta.html', cliente=cliente)

####################################################################################

################## Rota Registrar ##################################################   

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - In the View

#RegistrationForm

@app.route('/registro', methods=['GET', 'POST'])
def registro():

    form = FormularioDadosPessoais() #Retorna valores do forms.py

    if request.method == "POST" and form.validate_on_submit():

        Pessoas.adiciona_pessoa(form)
        flash(f'{form.nome.data}, obrigado pelo registro, realize o login', 'success')
        return redirect(url_for('login'))

    return render_template('clientes/registrocliente.html', form=form)

######################################################################################

################## Rota Login Formulario #############################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:         
        return redirect(url_for('minhaconta'))

    form=LoginFormularioCli() #Retorna valores do forms.py
    if request.method == "POST" and form.validate_on_submit():
        user = Pessoas.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.senha, form.senha.data):
            session['email'] = form.email.data
            flash(f'Bem Vindo {form.email.data}','success')
            return redirect(request.args.get('next') or url_for('minhaconta'))
        else:
            flash(f'E-mail ou Senha incorretos', 'danger')  
    return render_template('clientes/logincliente.html', form=form)

######################################################################################

@app.route("/logoutcli")
def logoutcli():
    session.pop('email')
    return redirect(url_for('minhaconta'))

################## Rota Carrinho #############################################

@app.route("/historico_de_pedidos")
def historico_de_pedidos():

    historico_pedidos = Pedidos.lista_pedidos(Pessoas.query.filter_by(email=session['email']).first().id)

    return render_template("clientes/historico_de_pedidos.html", historico_pedidos=historico_pedidos)

