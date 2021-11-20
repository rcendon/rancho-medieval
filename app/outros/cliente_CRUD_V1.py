from flask import Flask, render_template, Response, request,  redirect  #Response = Classe de Retorno da API / request = Comunicação com o body (post)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

####################################################################################  

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://User:Password@Host:5432/Database'
db = SQLAlchemy(app) #db recebe o app Flask para automatização.
migrate = Migrate(app, db)

################################ Modelo Pessoas ######################################

class Pessoas(db.Model):
   __tablename__ = 'pessoas' 
    
   id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(50), nullable=False, unique=True)
   login = db.Column(db.VARCHAR(10), nullable=False)  
   rg = db.Column(db.String(10), nullable=True)
   cpf = db.Column(db.String(12), nullable=True)
   tipo = db.Column(db.CHAR)
   #endereco = db.Column(db.Integer)
   senha = db.Column(db.VARCHAR(54), nullable=False)

   def to_json(self):
      return{"pessoa_id": self.id, "nome": self.nome, "login": self.login, "rg": self.rg, "cpf":self.cpf, "tipo": self.tipo, "senha": self.senha}
   
####################################################################################
   
#Query All
@app.route("/pessoas", methods = ["GET"])
def seleciona_pessoas():
   pessoas = Pessoas.query.all() #Select * from
   pessoas = [pessoas.to_json() for pessoa in pessoas]
  
   return gera_response(200, "pessoas", pessoas)

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
      body = {}
      body[nome_conteudo] = conteudo

      if mensagem:
         body ["mensagem"] = mensagem
      return Response(json.dumps(body), status=status, mimetype="application/json")  

####################################################################################
  
 #Query One
@app.route("/pessoa/<id>", methods=["GET"])
def seleciona_pessoa(id):
   pessoa = Pessoas.query.filter_by(id=id).first()
   pessoa = pessoa.to_json()
   return gera_response(200, "pessoa", pessoa)

####################################################################################

#Create
@app.route("/pessoa", methods=["POST"])
def cria_pessoa():
   body = request.get_json()
   try:
      pessoa = Pessoas(nome=body["nome"], login=body["login"], rg=body['rg'], cpf=body["cpf"], tipo=body["tipo"],
       endereco=body['endereco'], senha=body['senha'])
      db.session.add(pessoa)
      db.session.commit()
      return gera_response(201, "pessoa", pessoa.to_json(), "Criado com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "pessoa", {}, "Erro ao cadastrar")

####################################################################################      
   
#Update
@app.route("/pessoa/<id>", methods=["PUT"])
def atualiza_pessoa(id):
   # usuario a ser modificado
   pessoa = Pessoas.query.filter_by(id=id).first()
   #Modificações
   body = request.get_json()
   
   try:
      
      pessoa.nome = body["nome"]
      pessoa.login = body["login"]
      pessoa.rg = body["rg"]
      pessoa.cpf = body["cpf"]
      pessoa.tipo = body["tipo"]
      #pessoa.endereco = body["endereco"]
      pessoa.senha = body["senha"]

      db.session.add(pessoa)
      db.session.commit()
      return gera_response(200, "pessoa", pessoa.to_json(), "Atualização realizada com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "pessoa", {}, "Erro ao atualizar")

####################################################################################      

#delete
@app.route("/pessoa/<id>", methods=["DELETE"])
def delete_pessoa(id):
   pessoa = Pessoas.query.filter_by(id=id).first()

   try:
      db.session.delete(pessoa)
      db.session.commit()
      return gera_response(200, "pessoa", pessoa.to_json(), "Excluído com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "pessoa", {}, "Erro ao excluir")

####################################################################################      

app.run(debug=True)
