#__init__.py da appdelivery.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Construir APP - app recebe o objeto Flask (Instância do objeto Flask)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
db = SQLAlchemy(app) #db recebe o app Flask para automatização.

from appdelivery.admin import rotas #Importa da pasta loja/admin a arquivo rotas.py