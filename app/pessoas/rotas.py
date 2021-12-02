from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash
from wtforms.validators import Email 

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from app import app, db, bcrypt

from .forms import FormularioDadosPessoaisPrincipais, FormularioEndereco, LoginFormularioCli

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
    teste = FormularioEndereco()
    form = FormularioDadosPessoaisPrincipais(request.form) #Retorna valores do forms.py
    if request.method == "POST" and form.validate():
        hash_password = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')

        user = Pessoas(
            nome = form.nome.data,
            email = form.email.data,
            rg = int(form.rg.data),
            cpf = int(form.cpf.data),
            # registro_diverso= form.registro_diverso.data,
            # pais_do_registro_diverso = form.pais_do_registro_diverso.data,
            senha = hash_password,
            tipo = 'C') # precisa alterar, junto com o frontend, para cadastrar os dados corretamente, além de adicionar nova variavel para cadastro do endereço que será outro formulario

        db.session.add(user)
        db.session.commit() #Salva os dados no banco 

        #Menssagem flash
        flash(f'{form.nome.data}, obrigado pelo registro, realize o login', 'success')        
        return redirect(url_for('logincliente'))
        
    return render_template('clientes/registrocliente.html', form=form, teste=teste)

######################################################################################

################## Rota Login Formulario #############################################

@app.route('/logincliente', methods=['GET', 'POST'])
def logincliente():
    if 'email' in session:         
        return redirect(url_for('minhaconta'))

    form=LoginFormularioCli(request.form) #Retorna valores do forms.py
    if request.method == "POST" and form.validate():
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
    return redirect(url_for('logincliente'))

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