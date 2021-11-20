from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash
from sqlalchemy import inspect

from app import db, app
from .models import Produtos


##################### Rota Cardapio ####################################################

@app.route('/cardapio')
def cardapio():
    cardapio = Produtos.query.all() #Select * from 
    return render_template('produtos/cardapio.html',cardapio=cardapio)


##################### Rota Promoções ####################################################

@app.route('/promocoes')
def promocoes():
    return render_template('/produtos/promocoes.html')