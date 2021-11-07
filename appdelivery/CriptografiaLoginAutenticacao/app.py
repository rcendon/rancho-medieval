
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
from flask import Flask, Blueprint, render_template, redirect, request, url_for
from models import Cardapio
from __init__ import app, db, db_cardapio
#Construir APP - app recebe o objeto Flask (Instância do objeto Flask)
########################################################################################################

#Rota para renderizar a pagina INDEX.HTML
@app.route('/') 
#Função da Rota
def index():
    cardapio = Cardapio.query.all() #Select * from Cardapio
    return render_template('index.html', cardapio=cardapio)

########################################################################################################

#Rota para renderizar a pagina ADD.HTML 
@app.route('/addcliente', methods=['GET', 'POST'])

# ###### Create Pessoas ######
# def add_pessoa():
#     pessoas = Pessoas.query.all() #Select * from Pessoas
#     if request.method == 'POST': #SE POST
#         pessoarequest = Pessoas(
#             request.form['nome'],
#             request.form['login'], 
#             request.form['rg'], 
#             request.form['cpf'], 
#             request.form['tipo'], 
#             request.form['senha'],)
#         db.session.add(pessoarequest) #Recebe os dados restornados do POST 
#         db.session.commit() #Salva os dados no banco 
#         return redirect(url_for('index')) #Se o metodo POST for OK retornar para o INDEX
#     return render_template('addcliente.html', pessoas=pessoas) #ELSE mostra pagina ADD

########################################################################################################

#Rota para renderizar a pagina ADDCARDAPIO.HTML 
@app.route('/addcardapio', methods=['GET', 'POST'])

###### Create Cardapio ######
def add_cardapio():
    #cardapio = Cardapio.query.all() #Select * from Cardapio
    if request.method == 'POST': #SE POST
        cardapioRequest = Cardapio(
            request.form['nome'],
            request.form['quantidade_estoque_produto'],
            request.form['permite_estocagem'],
            request.form['valor'],)        
        db.session.add(cardapioRequest) #Recebe os dados restornados do POST 
        db.session.commit() #Salva os dados no banco 
        return redirect(url_for('index')) #Se o metodo POST for OK retornar para o INDEX
    return render_template('addcardapio.html') #ELSE mostra pagina ADD

########################################################################################################

#Para aumentar a segurança o app.run() só roda se ele estiver no arquivo principal 
#if __name__ == '__main__': 
db.create_all()
#db_cardapio.create_all()
app.secret_key='minhaSenha'
app.run(debug=True) #Roda o aplicativo 
    # Obs: debug=True Modo desenvolvedor para atualizar os templates automaticamente.

########################################################################################################

