import re
from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash
from flask.wrappers import Response
from werkzeug.utils import secure_filename
#from wtforms.validators import Email 

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from app import app, db, bcrypt

from .forms import RegistrationForm, LoginFormulario, CadastroProdutos

from ..produtos.models import Produtos

from ..pessoas.models import Pessoas

##################### Rota Home ####################################################

#Rota Home
@app.route('/')

def home(): 
    return render_template('index.html')

######################################################################################

##################### Rota Usuario ####################################################

#Rota Usuario
@app.route('/usuario')
def usuario(): 
    if 'cpf' not in session: ###Controle de Acesso###
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('login'))
    return render_template('admin/usuario.html')

####################################################################################

################## Rota Registrar ##################################################   

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - In the View

#RegistrationForm

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if 'cpf' not in session: ###Controle de Acesso###
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('login'))

    form = RegistrationForm(request.form) #Retorna valores do forms.py
    if request.method == "POST" and form.validate():
        hash_password = bcrypt.generate_password_hash(form.senha.data).encode('utf-8')

        user = Pessoas(
            nome = form.nome.data,
            email = form.email.data,
            rg = int(form.rg.data),
            cpf = int(form.cpf.data),
            # registro_diverso= form.registro_diverso.data,
            # pais_do_registro_diverso = form.pais_do_registro_diverso.data,
            senha = hash_password,
            tipo = 'F') # precisa alterar, junto com o frontend, para cadastrar os dados corretamente, além de adicionar nova variavel para cadastro do endereço que será outro formulario

        db.session.add(user)
        db.session.commit() #Salva os dados no banco 

        #Menssagem flash
        flash(f'{form.nome.data}, obrigado pelo registro, realize o login', 'success')        
        return redirect(url_for('login'))
        
    return render_template('admin/registrar.html', form=form)

##################################################################################################


################## Rota Login Formulario ########################################################

#LoginFormulario

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'cpf' in session: ###Controle de Acesso###         
        return redirect(url_for('usuario'))

    form=LoginFormulario(request.form) #Retorna valores do forms.py
    if request.method == "POST" and form.validate():
        user = Pessoas.query.filter_by(cpf=form.cpf.data).first()
        
        if user and bcrypt.check_password_hash(user.senha, form.senha.data):
        # if user and user.senha == form.senha.data:
            session['cpf'] = form.cpf.data
            flash(f'Bem Vindo CPF: {form.cpf.data}','success')
            return redirect(request.args.get('next') or url_for('usuario'))
        else:
            flash(f'CPF ou senha incorretos', 'danger')
    return render_template('admin/login.html', form=form)


###############################################################################################

##################### Rota Adicionar Produto ####################################################

@app.route('/addcardapio', methods=['GET', 'POST'])
def produtos():
    if 'cpf' not in session: ###Controle de Acesso###
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('login'))

    form=CadastroProdutos(request.form) #Retorna valores do forms.py
    if request.method == "POST": #SE POST  

        ### iMG ##########################################
        pic = request.files['pic']
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        ##################################################

        requestprodutos = Produtos(nome=form.nome.data,quantidade_estoque=form.quantidade_estoque.data,valor=form.valor.data,descricao=form.descricao.data,imagem=pic.read(),mimetype=mimetype)
        
        db.session.add(requestprodutos) #Recebe os dados restornados do POST      descricao   
        db.session.commit() #Salva os dados no banco 
        #Menssagem flash
        flash(f'Produto cadastrado com sucesso ', 'success')  
        return redirect(url_for('usuario')) #Se o metodo POST for OK retornar para o INDEX

    return render_template('admin/addcardapio.html',form=form) #ELSE mostra pagina ADD

##################### Rota Logout ####################################################

@app.route("/logout")
def logout():
    session.pop('cpf')
    return redirect(url_for('login'))

##################### Rota Exibir Imagem ####################################################

@app.route("/<int:id>") 
def get_img(id):
    img = Produtos.query.filter_by(id=id).first()
    return Response(img.imagem, mimetype=img.mimetype)