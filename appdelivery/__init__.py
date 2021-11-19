#__init__.py da appdelivery.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import getenv
from dotenv import load_dotenv

#Construir APP - app recebe o objeto Flask (Instância do objeto Flask)
app = Flask(__name__)

load_dotenv() # carrega as variáveis de ambiente para o getenv localizá-las

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('database_URI').replace("postgres://", "postgresql://", 1) #'sqlite:///bancolocal.db' , deve ser colocado no arquivo .env

app.config['SECRET_KEY']= getenv('secret_key') # '1234' Chave para criptografar senha, deve ser colocada no arquivo .env

db = SQLAlchemy(app) #db recebe o app Flask para automatização.

bcrypt = Bcrypt(app)

from appdelivery.admin import rotas #Importa da pasta appdelivery/admin o arquivo rotas.py
from appdelivery.produtos import rotas #Importa da pasta appdelivery/produtos o arquivo rotas.py
from appdelivery.pessoas import rotas #Importa da pasta appdelivery/pessoas o arquivo rotas.py
from appdelivery.diversos import rotas #Importa da pasta appdelivery/diversos o arquivo rotas.py
from appdelivery.erros import rotas #Importa da pasta appdelivery/erros o arquivo rotas.py