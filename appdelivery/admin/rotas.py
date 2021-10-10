from flask import render_template, session, request, url_for 
from appdelivery import app, db #Importa a variaveis APP e DB do "__init__.py" = (loja).

##################################################################################

#Rota Home
@app.route('/')

def home():
    return render_template('index.html')

##################################################################################    

#Rota Registrar
@app.route('/registrar')

def registrar():
    return render_template('admin/registrar.html')
    