
#Não ensquecer de instalar os requerimentos:   
#pip install flask
#pip install flask_sqlalchemy
#pip install flask_migrate
#
#
#https://github.com/rcendon/rancho-medieval
#
#No Git Bash: https://git-scm.com/downloads
#
#git config --global user.name 
#git config --global user.email 
#git config --global github.token
#git clone https://github.com/rcendon/rancho-medieval.git .
#
#
################################   Servidor Flask    ###############################################

#Importar o flask e do objeto Flask importar o render_template eo redirect 
from flask import Flask, render_template, redirect 

#Construir APP - app recebe o objeto Flask (Instância do objeto Flask)
app = Flask(__name__)

#Rota para renderizar a pagina
@app.route('/')
#Função da Rota
def index():
    return render_template('index.html')

#Para aumentar a segurança o app.run() só roda se ele estiver no arquivo principal 
if __name__ == '__main__': 
    app.run(debug=True) #Roda o aplicativo 
    # Obs: debug=True Modo desenvolvedor para atualizar os templates automaticamente.

##################################################################################################

