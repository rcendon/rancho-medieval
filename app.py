
#Não ensquecer de instalar os requerimentos:   
#pip install flask
#pip install flask_sqlalchemy
#pip install flask_migrate
#pip install psycopg2
#
#https://github.com/rcendon/rancho-medieval
#
#No Git Bash: https://git-scm.com/downloads
#
#git config --global user.name SEU_USUARIO
#git config --global user.email SEU_EMAIL
#git config --global github.token SEU_TOKEN
#git clone https://github.com/rcendon/rancho-medieval.git .
#
#
################################   Servidor Flask    ####################################################

#Importar o flask e do objeto Flask importar o render_template eo redirect 
#from re import template
from flask import Flask, render_template, redirect, request, url_for 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

#Construir APP - app recebe o objeto Flask (Instância do objeto Flask)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
db = SQLAlchemy(app) #db recebe o app Flask para automatização.
db_cardapio = SQLAlchemy(app) #db_cardapio recebe o app Flask para automatização.

################################ Modelo Pessoas ##########################################################
#########################################################################################################

class Pessoas(db.Model): #Modelo Pessoas
   __tablename__ = 'pessoas' 
    
   id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(50))
   login = db.Column(db.VARCHAR(10))  
   rg = db.Column(db.String(10))
   cpf = db.Column(db.String(12))
   tipo = db.Column(db.CHAR(1))
   #endereco = db.Column(db.Integer)
   senha = db.Column(db.VARCHAR(64))

   def __init__(self, nome, login, rg, cpf, tipo, senha):
       self.nome = nome
       self.login = login
       self.rg = rg
       self.cpf = cpf
       self.tipo = tipo
       #self.endereco = endereco
       self.senha = senha

########################################################################################################

#Create Pessoas
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST': #SE POST
        pessoa = Pessoas(
            request.form['nome'],
            request.form['login'], 
            request.form['rg'], 
            request.form['cpf'], 
            request.form['tipo'], 
            request.form['senha'], )
        db.session.add(pessoa) #Recebe os dados restornados do POST 
        db.session.commit() #Salva os dados no banco 
        return redirect(url_for('index')) #Se o metodo POST for OK retornar para o INDEX
    return render_template('add.html') #ELSE mostra pagina ADD

########################################################################################################

#Update Pessoas

########################################################################################################

#Delete Pessoas 

############################### Fim Modelo Pessoas #####################################################
########################################################################################################



################################ Modelo Cardápio ########################################################
#########################################################################################################

class Cardapio(db_cardapio.Model):
   __tablename__ = 'cardapio' 
    
   id_produto = db_cardapio.Column(db_cardapio.Integer, autoincrement=True, primary_key=True)
   nome = db_cardapio.Column(db_cardapio.VARCHAR(50), nullable=False, unique=True)
   quantidade_estoque_produto = db_cardapio.Column(db_cardapio.VARCHAR(10), nullable=False)
   permite_estocagem = db_cardapio.Column(db.Boolean)
   valor = db_cardapio.Column(DOUBLE_PRECISION)
   
   def __init__(self, nome, quantidade_estoque_produto, permite_estocagem, valor):
       self.nome = nome
       self.quantidade_estoque_produto = quantidade_estoque_produto
       self.permite_estocagem = permite_estocagem
       self.valor = valor

############################### Fim Modelo Cardápio #####################################################
########################################################################################################

#Rota para renderizar a pagina
@app.route('/')
#Função da Rota
def index():
    pessoas = Pessoas.query.all() #Select * from Pessoas
    cardapio = Cardapio.query.all() #Select * from Cardapio

    return render_template('index.html', pessoas=pessoas, cardapio=cardapio)

    

#Para aumentar a segurança o app.run() só roda se ele estiver no arquivo principal 
#if __name__ == '__main__': 
db.create_all()
db_cardapio.create_all()
app.run(debug=True) #Roda o aplicativo 
    # Obs: debug=True Modo desenvolvedor para atualizar os templates automaticamente.

########################################################################################################

