from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash
from wtforms.validators import Email 

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from app import app, db, bcrypt

from .forms import FormularioDadosPessoais, LoginFormularioCli

from .models import Pessoas

##################### Rota Usuario ####################################################

#Rota Usuario

@app.route('/minhaconta')
def minhaconta(): 
    if 'email' not in session:
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('logincliente'))
    return render_template('clientes/minhaconta.html')

####################################################################################

################## Rota Registrar ##################################################   

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - In the View

#RegistrationForm

@app.route('/registrocliente', methods=['GET', 'POST'])
def registrocliente():

    form = FormularioDadosPessoais() #Retorna valores do forms.py

    if request.method == "POST" and form.validate_on_submit():

        Pessoas.adiciona_pessoa(form)
        flash(f'{form.nome.data}, obrigado pelo registro, realize o login', 'success')
        return redirect(url_for('logincliente'))

    return render_template('clientes/registrocliente.html', form=form)

######################################################################################

################## Rota Login Formulario #############################################

@app.route('/logincliente', methods=['GET', 'POST'])
def logincliente():
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

# redirect(request.args.get('next') or
######################################################################################

@app.route("/logoutcli")
def logoutcli():
    session.pop('email')
    return redirect(url_for('minhaconta'))

################## Rota Carrinho #############################################

app.route("/carrinho")
def carrinho():
    if carrinho not in session:
        return render_template("index.html")
    return render_template("clientes/historico_de_pedidos.html")


# admin = Pessoas(
#     nome = 'Admin',
#     email = 'admin@email.com',
#     cpf = 1,
#     senha = str(bcrypt.generate_password_hash("12345")).encode('utf-8'),
#     tipo = 'A'
# )
#
# db.session.add(admin)
#
# db.session.commit()