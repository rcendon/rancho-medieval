#__init__.py da app.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import getenv
from dotenv import load_dotenv
from flask_migrate import Migrate



#Construir APP - app recebe o objeto Flask (Instância do objeto Flask)
app = Flask(__name__)

load_dotenv() # carrega as variáveis de ambiente para o getenv localizá-las

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('database_URI').replace("postgres://", "postgresql://", 1) #'sqlite:///bancolocal.db' , deve ser colocado no arquivo .env

app.config['SECRET_KEY']= getenv('secret_key') # '1234' Chave para criptografar senha, deve ser colocada no arquivo .env

db = SQLAlchemy(app) #db recebe o app Flask para automatização.

bcrypt = Bcrypt(app)

from app.admin import rotas #Importa da pasta app/admin o arquivo rotas.py
from app.produtos import rotas #Importa da pasta app/produtos o arquivo rotas.py
from app.pessoas import rotas #Importa da pasta app/pessoas o arquivo rotas.py
from app.diversos import rotas #Importa da pasta app/diversos o arquivo rotas.py
from app.erros import rotas #Importa da pasta app/erros o arquivo rotas.py

migrate = Migrate(app, db)

db.create_all()
