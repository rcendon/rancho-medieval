from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash
from wtforms.validators import Email 

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from appdelivery import app, db, bcrypt

from .forms import RegistrationFormCli, LoginFormularioCli

from .models import UserCli

##################### Rota Usuario ####################################################

#Rota Usuario

@app.route('/minhaconta')
def minhaconta(): 
    if 'email' not in session:
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('logincliente'))
    return render_template('../templates/clientes/minhaconta.html')

####################################################################################

################## Rota Registrar ##################################################   

#self.nome = nome
#self.email = email
#self.telefone = telefone
#self.rg = rg
#self.cpf = cpf
#self.endereco = endereco
#self.senha = senha

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - In the View

#RegistrationForm

@app.route('/registrocliente', methods=['GET', 'POST'])
def registrocliente():
    form = RegistrationFormCli(request.form) #Retorna valores do forms.py
    if request.method == "POST" and form.validate():
        hash_password = bcrypt.generate_password_hash(form.senha.data)

        user = UserCli(nome=form.nome.data,email=form.email.data,telefone=form.telefone.data,rg=form.rg.data,cpf=form.cpf.data, 
        endereco=form.endereco.data, senha=hash_password)

        db.session.add(user)
        db.session.commit() #Salva os dados no banco 

        #Menssagem flash
        flash(f'{form.nome.data}, obrigado pelo registro, realize o login', 'success')        
        return redirect(url_for('logincliente'))
        
    return render_template('/clientes/registrocliente.html', form=form)

######################################################################################


################## Rota Login Formulario ############################################# 

#LoginFormulario

@app.route('/logincliente', methods=['GET', 'POST'])
def logincliente():
    if 'email' in session:         
        return redirect(url_for('minhaconta'))

    form=LoginFormularioCli(request.form) #Retorna valores do forms.py
    if request.method == "POST" and form.validate():
        user= UserCli.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.senha, form.senha.data):
            session['email'] = form.email.data
            flash(f'Bem Vindo {form.email.data}','success')
            return redirect(request.args.get('next')or url_for('minhaconta'))
        else:   
            flash(f'E-mail ou Senha incorretos', 'danger')  
    return render_template('/clientes/logincliente.html', form=form)


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
    return render_template("clientes/carrinho.html")