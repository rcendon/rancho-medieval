from flask import Flask, Response, request #Response = Classe de Retorno da API / request = Comunicação com o body (post)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
import json

####################################################################################  

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8442@localhost:5432/pessoas'
db = SQLAlchemy(app) #db recebe o app Flask para automatização.
migrate = Migrate(app, db)

################################ Modelo Pessoas ######################################

class Cardapio(db.Model):
   __tablename__ = 'cardapio' 
    
   id = db.Column('cardapio_id', db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(50), nullable=False, unique=True)
   quantidade_estoque_produto = db.Column(db.VARCHAR(10), nullable=False)
   permite_estocagem = db.Column(db.Boolean)
   valor = db.Column(DOUBLE_PRECISION)
  
   def to_json(self):
      return{"cardapio_id": self.id, "nome": self.nome, "quantidade_estoque_produto": self.quantidade_estoque_produto, 
      "permite_estocagem":self.permite_estocagem, "valor": self.valor} 

####################################################################################
   
#Query All
@app.route("/cardapios", methods = ["GET"])
def seleciona_cardapios():
   cardapio = Cardapio.query.all()
   cardapio = [produto.to_json() for produto in cardapio]
   
   return gera_response(200, "cardapio", cardapio)

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
      body = {}
      body[nome_conteudo] = conteudo

      if mensagem:
         body ["mensagem"] = mensagem
      return Response(json.dumps(body), status=status, mimetype="application/json")  

####################################################################################
  
 #Query One
@app.route("/cardapio/<id>", methods=["GET"])
def seleciona_cardapio(id):
   cardapio = Cardapio.query.filter_by(id=id).first()
   cardapio = cardapio.to_json()
   return gera_response(200, "cardapio",cardapio )

####################################################################################

#Create
@app.route("/cardapio", methods=["POST"])
def cria_cardapio():
   body = request.get_json()
   try:
      cardapio = Cardapio(nome=body["nome"], quantidade_estoque_produto=body["quantidade_estoque_produto"], permite_estocagem=body["permite_estocagem"],
      valor=body["valor"])
      db.session.add(cardapio)
      db.session.commit()
      return gera_response(201, "cardapio", cardapio.to_json(), "Criado com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "cardapio", {}, "Erro ao cadastrar")

####################################################################################      
   
#Update
@app.route("/cardapio/<id>", methods=["PUT"])
def atualiza_cardapio(id):
   # usuario a ser modificado
   cardapio = Cardapio.query.filter_by(id=id).first()
   #Modificações
   body = request.get_json()
   
   try:
      
      cardapio.nome = body["nome"]
      cardapio.quantidade_estoque_produto = body["quantidade_estoque_produto"]
      cardapio.permite_estocagem = body["permite_estocagem"]
      cardapio.valor = body ["valor"]


      db.session.add(cardapio)
      db.session.commit()
      return gera_response(200, "cardapio", cardapio.to_json(), "Atualização realizada com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "cardapio", {}, "Erro ao atualizar")

####################################################################################      

#delete
@app.route("/cardapio/<id>", methods=["DELETE"])
def delete_cardapio(id):
   cardapio = Cardapio.query.filter_by(id=id).first()

   try:
      db.session.delete(cardapio)
      db.session.commit()
      return gera_response(200, "cardapio", cardapio.to_json(), "Excluído com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "cardapio", {}, "Erro ao excluir")

####################################################################################      

app.run(debug=True)
