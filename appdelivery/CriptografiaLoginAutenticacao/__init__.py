from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

#Construir APP - app recebe o objeto Flask (Instância do objeto Flask)
app = Flask(__name__)
app.config['SECRET KEY'] = 'minhaSenha'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:121312@localhost:5432/pessoas'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app) #db recebe o app Flask para automatização.
db_cardapio = SQLAlchemy(app) #db_cardapio recebe o app Flask para automatização.

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

import models
@login_manager.user_loader
def load_user(user_id):
    return models.Pessoas.query.get(int(user_id))

#blueprint para rotas auth
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint para rotas não-auth
from profile import main as main_blueprint
app.register_blueprint(main_blueprint)

########################################################################################################