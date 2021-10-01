
#Não ensquecer de instalar os requerimentos:   
#pip install flask
#pip install flask_sqlalchemy
#pip install flask_migrate
#pip install psycopg2
#
#https://github.com/rcendon/rancho-medieval
#
#No Git Bash: https://git-scm.com/downloads

#git config --global user.email 
#git config --global github.token
#git clone https://github.com/rcendon/rancho-medieval.git .
#
#
################################   Servidor Flask    ###############################################

#Importar o flask e do objeto Flask importar o render_template eo redirect 
#from re import template
from flask import Flask, render_template, redirect, request, url_for 
from flask_sqlalchemy import SQLAlchemy

#Construir APP - app recebe o objeto Flask (Instância do objeto Flask)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
db = SQLAlchemy(app) #db recebe o app Flask para automatização.

class Pessoas(db.Model):
   __tablename__ = 'pessoas' 
    
   id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(50))
   login = db.Column(db.VARCHAR(10))  
   rg = db.Column(db.String(10), unique=True)
   cpf = db.Column(db.String(12), unique=True)
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

#Rota para renderizar a pagina
@app.route('/')
#Função da Rota
def index():
    pessoas = Pessoas.query.all()
    return render_template('index.html', pessoas=pessoas)

#Para aumentar a segurança o app.run() só roda se ele estiver no arquivo principal 
#if __name__ == '__main__': 
    #db.create_all()
app.run(debug=True) #Roda o aplicativo 
    # Obs: debug=True Modo desenvolvedor para atualizar os templates automaticamente.

##################################################################################################

