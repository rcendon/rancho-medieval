from flask import render_template, session, request, redirect, url_for, flash
from flask.helpers import flash

from appdelivery import db, app


##################### Rota Cardapio ####################################################

@app.route('/cardapio')

def cardapio(): 
    return render_template('/produtos/cardapio.html')


##################### Rota Promoções ####################################################

@app.route('/promocoes')

def promocoes(): 
    return render_template('/produtos/promocoes.html')