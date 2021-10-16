from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash
from wtforms.validators import Email 

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from appdelivery import app, db, bcrypt

from .forms import RegistrationForm, LoginFormulario

from .models import User

##################### Rota Home ####################################################

#Rota Home
@app.route('/')

def home(): 
    return render_template('index.html')

####################################################################################

##################### Rota Admin ####################################################

#Rota Usuario

@app.route('/usuario')
def usuario(): 
    if 'email' not in session:
        flash(f'Faça o login primeiro', 'danger')    
        return redirect(url_for('login'))
    return render_template('usuario.html')

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

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        hash_password = bcrypt.generate_password_hash(form.senha.data)

        user = User(nome=form.nome.data,email=form.email.data,telefone=form.telefone.data,rg=form.rg.data,cpf=form.cpf.data, 
        endereco=form.endereco.data, senha=hash_password)

        db.session.add(user)
        db.session.commit() #Salva os dados no banco 

        #Menssagem flash
        flash(f'{form.nome.data}, obrigado pelo registro, realize o login', 'success')        
        return redirect(url_for('login'))
        
    return render_template('registrar.html', form=form)

######################################################################################


################## Rota Login Formulario ############################################# 

#LoginFormulario

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginFormulario(request.form)
    if request.method == "POST" and form.validate():
        user= User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.senha, form.senha.data):
            session['email'] = form.email.data
            flash(f'Bem Vindo {form.email.data}','success')
            return redirect(request.args.get('next')or url_for('usuario'))
        else:   
            flash(f'E-mail ou Senha incorretos', 'danger')  
    return render_template('login.html', form=form)


######################################################################################

