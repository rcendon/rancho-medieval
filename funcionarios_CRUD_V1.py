from flask import Flask, Response, request
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

######################### Modelo Funcionários ######################################


class Funcionarios(db.Model):
   __tablename__ = 'funcionarios'
    
   id = db.Column('funcionario_id', db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.String(100), nullable=False)
   login = db.Column(db.VARCHAR(10), nullable=False)  
   rg = db.Column(db.String(10), nullable=False, unique=True)
   cpf = db.Column(db.String(12), nullable=False, unique=True)
   email= db.Column(db.VARCHAR(100), nullable=False, unique=True)
   endereco = db.Column(db.VARCHAR(100))
   senha = db.Column(db.VARCHAR(50), nullable=False)
   funcao = db.Column(db.VARCHAR(50), nullable=False)

   def to_json(self):
       return{"funcionario_id": self.id, "nome": self.nome, "login": self.login, "rg": self.rg, "cpf": self.cpf,
       "email": self.email, "endereco": self.endereco, "senha": self.senha, "funcao":self.funcao}

####################################################################################

#Query All
@app.route("/funcionarios", methods = ["GET"])
def seleciona_funcionarios():
   funcionarios_objetos = Funcionarios.query.all()
   funcionarios_json = [funcionario.to_json() for funcionario in funcionarios_objetos]
  
   return gera_response(200, "funcionarios", funcionarios_json)

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
      body = {}
      body[nome_conteudo] = conteudo

      if mensagem:
         body ["mensagem"] = mensagem
      return Response(json.dumps(body), status=status, mimetype="application/json")

####################################################################################

#Query One
@app.route("/funcionario/<id>", methods=["GET"])
def seleciona_funcionario(id):
   funcionario = Funcionarios.query.filter_by(id=id).first()
   funcionario_json = funcionario.to_json()
   return gera_response(200, "funcionario", funcionario_json)

####################################################################################

#Create
@app.route("/funcionario", methods=["POST"])
def cria_funcionario():
   body = request.get_json()
   try:
      funcionario = Funcionarios(nome=body["nome"], login=body["login"], rg=body['rg'], cpf=body['cpf'],
      email=body["email"], endereco=body['endereco'], senha=body['senha'], funcao=body['funcao'])
      db.session.add(funcionario)
      db.session.commit()
      return gera_response(201, "funcionario", funcionario.to_json(), "Criado com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "cliente", {}, "Erro ao cadastrar")

####################################################################################

#Update
@app.route("/funcionario/<id>", methods=["PUT"])
def atualiza(id):
   # usuario a ser modificado
   funcionario = Funcionarios.query.filter_by(id=id).first()
   #Modificações
   body = request.get_json()
   
   try:
      
      funcionario.nome = body["nome"]
      funcionario.login = body["login"]
      funcionario.rg = body["rg"]
      funcionario.cpf = body["cpf"]
      funcionario.email = body["email"]
      funcionario.endereco = body["endereco"]
      funcionario.senha = body["senha"]
      funcionario.funcao = body["funcao"]

      db.session.add(funcionario)
      db.session.commit()
      return gera_response(200, "funcionario", funcionario.to_json(), "Atualização realizada com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "funcionario", {}, "Erro ao atualizar")

####################################################################################

#delete
@app.route("/funcionario/<id>", methods=["DELETE"])
def delete(id):
   funcionario = Funcionarios.query.filter_by(id=id).first()

   try:
      db.session.delete(funcionario)
      db.session.commit()
      return gera_response(200, "funcionario", funcionario.to_json(), "Cliente excluido com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "funcionario", {}, "Erro ao excluir")

####################################################################################

app.run(debug=True)