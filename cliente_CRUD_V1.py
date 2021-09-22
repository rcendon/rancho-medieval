from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:121312@localhost:5432/pessoas'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Pessoas(db.Model):
   __tablename__ = 'pessoas'
    
   id = db.Column('pessoa_id', db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(50), nullable=False, unique=True)
   login = db.Column(db.VARCHAR(10), nullable=False)  
   rg = db.Column(db.String(10), nullable=True)
   cpf = db.Column(db.String(12), nullable=True)
   tipo = db.Column(db.CHAR)
   endereco = db.Column(db.Integer)
   senha = db.Column(db.VARCHAR(54), nullable=False)

   def to_json(self):
      return{"pessoa_id": self.id, "nome": self.nome, "login": self.login, "rg": self.rg, "cpf":self.cpf, "tipo": self.tipo,
      "endereco": self.endereco, "senha": self.senha}
   
   
#Query All
@app.route("/pessoas", methods = ["GET"])
def seleciona_pessoas():
   pessoas = Pessoas.query.all()
   pessoas = [pessoa.to_json() for pessoa in pessoas]
  
   return gera_response(200, "pessoas", pessoas)

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
      body = {}
      body[nome_conteudo] = conteudo

      if mensagem:
         body ["mensagem"] = mensagem
      return Response(json.dumps(body), status=status, mimetype="application/json")  
 
 #Query One
@app.route("/pessoa/<id>", methods=["GET"])
def seleciona_pessoa(id):
   pessoa_carro = Pessoas.query.filter_by(id=id).first()
   pessoa_carro = pessoa_carro.to_json()
   return gera_response(200, "pessoa", pessoa_carro)

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
      pessoa.endereco = body["endereco"]
      pessoa.senha = body["senha"]

      db.session.add(pessoa)
      db.session.commit()
      return gera_response(200, "pessoa", pessoa.to_json(), "Atualização realizada com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "pessoa", {}, "Erro ao atualizar")

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

app.run(debug=True)
