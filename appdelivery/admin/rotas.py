from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash 

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from appdelivery import app, db, bcrypt

from .forms import RegistrationForm

from .models import User
##################################################################################

#Rota Home
@app.route('/')

def home(): 
    return render_template('index.html')

##################################################################################    

#self.nome = nome
#self.login = login
#self.rg = rg
#self.cpf = cpf
#self.tipo = tipo
###########self.endereco = endereco
#self.senha = senha

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - In the View

#Rota Registrar
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.senha.data)

        user = User(nome=form.nome.data, login=form.login.data, rg=form.rg.data,cpf=form.cpf.data, 
        tipo=form.tipo.data, senha=hash_password)

        db.add(user)
        
        flash('Obrigado pelo registro')
        
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form)

###################################################################################

