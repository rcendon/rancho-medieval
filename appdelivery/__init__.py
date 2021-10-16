#__init__.py da appdelivery.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#Construir APP - app recebe o objeto Flask (Instância do objeto Flask)
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancolocal.db'

app.config['SECRET_KEY']='1234' #Chave para criptografar senha
db = SQLAlchemy(app) #db recebe o app Flask para automatização.

bcrypt = Bcrypt(app)

from appdelivery.admin import rotas #Importa da pasta appdelivery/admin a arquivo rotas.py