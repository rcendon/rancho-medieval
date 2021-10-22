from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash
from wtforms.validators import Email 

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from appdelivery import app, db, bcrypt

from .forms import RegistrationForm, LoginFormulario, CadastroProdutos

from .models import User, Produtos

##################### Rota Home ####################################################

#Rota Home
@app.route('/')

def home(): 
    return render_template('index.html')

####################################################################################

##################### Rota Usuario ####################################################

#Rota Usuario

@app.route('/usuario')
def usuario(): 
    if 'cpf' not in session: ###Controle de Acesso###
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('login'))
    return render_template('/admin/usuario.html')

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
    if 'cpf' not in session: ###Controle de Acesso###
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('login'))

    form = RegistrationForm(request.form) #Retorna valores do forms.py
    if request.method == "POST" and form.validate():
        hash_password = bcrypt.generate_password_hash(form.senha.data)

        user = User(nome=form.nome.data,email=form.email.data,telefone=form.telefone.data,rg=form.rg.data,cpf=form.cpf.data, 
        endereco=form.endereco.data, senha=hash_password)

        db.session.add(user)
        db.session.commit() #Salva os dados no banco 

        #Menssagem flash
        flash(f'{form.nome.data}, obrigado pelo registro, realize o login', 'success')        
        return redirect(url_for('login'))
        
    return render_template('/admin/registrar.html', form=form)

##################################################################################################


################## Rota Login Formulario ########################################################

#LoginFormulario

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'cpf' in session: ###Controle de Acesso###         
        return redirect(url_for('usuario'))

    form=LoginFormulario(request.form) #Retorna valores do forms.py
    if request.method == "POST" and form.validate():
        user= User.query.filter_by(cpf=form.cpf.data).first()
        
        if user and bcrypt.check_password_hash(user.senha, form.senha.data):
            session['cpf'] = form.cpf.data
            flash(f'Bem Vindo CPF: {form.cpf.data}','success')
            return redirect(request.args.get('next')or url_for('usuario'))
        else:   
            flash(f'CPF ou senha incorretos', 'danger')  
    return render_template('/admin/login.html', form=form)


###############################################################################################

##################### Rota Adicionar Produto ####################################################

@app.route('/addcardapio', methods=['GET', 'POST'])
def produtos():
    if 'cpf' not in session: ###Controle de Acesso###
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('login'))

    form=CadastroProdutos(request.form) #Retorna valores do forms.py
    if request.method == "POST": #SE POST
        
        requestprodutos = Produtos(nome=form.nome.data,quantidade_estoque=form.quantidade_estoque.data,valor=form.valor.data)
        
        db.session.add(requestprodutos) #Recebe os dados restornados do POST         
        db.session.commit() #Salva os dados no banco 
        #Menssagem flash
        flash(f'Produto cadastrado com sucesso ', 'success')  
        return redirect(url_for('usuario')) #Se o metodo POST for OK retornar para o INDEX

    return render_template('/admin/addcardapio.html',form=form) #ELSE mostra pagina ADD



@app.route("/logout")
def logout():
    session.pop('cpf')
    return redirect(url_for('login'))