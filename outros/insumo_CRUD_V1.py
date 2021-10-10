from flask import Flask, render_template, Response, request #Response = Classe de Retorno da API / request = Comunicação com o body (post)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

####################################################################################  

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8442@localhost:5432/pessoas'
db = SQLAlchemy(app) #db recebe o app Flask para automatização.
migrate = Migrate(app, db)

################################ Modelo Pessoas ######################################

class Insumos(db.Model):
   __tablename__ = 'insumos' 
    
   id = db.Column('insumo_id', db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(50), nullable=False, unique=True)
   quantidade_estoque_insumo = db.Column(db.VARCHAR(10), nullable=False)  
  
   def to_json(self):
      return{"insumo_id": self.id, "nome": self.nome, "quantidade_estoque_insumo": self.quantidade_estoque_insumo} 

####################################################################################
   
#Query All
@app.route("/insumos", methods = ["GET"])
def seleciona_insumos():
   insumos = Insumos.query.all()
   insumos = [insumo.to_json() for insumo in insumos]
  
   return gera_response(200, "insumos", insumos)

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
      body = {}
      body[nome_conteudo] = conteudo

      if mensagem:
         body ["mensagem"] = mensagem
      return Response(json.dumps(body), status=status, mimetype="application/json")  

####################################################################################
  
 #Query One
@app.route("/insumo/<id>", methods=["GET"])
def seleciona_insumo(id):
   insumo = Insumos.query.filter_by(id=id).first()
   insumo = insumo.to_json()
   return gera_response(200, "insumo",insumo )
   
####################################################################################

#Create
@app.route("/insumo", methods=["POST"])
def cria_insumo():
   body = request.get_json()
   try:
      insumo = Insumos(nome=body["nome"], quantidade_estoque_insumo=body["quantidade_estoque_insumo"])
      db.session.add(insumo)
      db.session.commit()
      return gera_response(201, "insumo", insumo.to_json(), "Criado com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "insumo", {}, "Erro ao cadastrar")

####################################################################################      
   
#Update
@app.route("/insumo/<id>", methods=["PUT"])
def atualiza_insumo(id):
   # usuario a ser modificado
   insumo = Insumos.query.filter_by(id=id).first()
   #Modificações
   body = request.get_json()
   
   try:
      
      insumo.nome = body["nome"]
      insumo.quantidade_estoque_insumo = body["quantidade_estoque_insumo"]


      db.session.add(insumo)
      db.session.commit()
      return gera_response(200, "insumo", insumo.to_json(), "Atualização realizada com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "insumo", {}, "Erro ao atualizar")

####################################################################################      

#delete
@app.route("/insumo/<id>", methods=["DELETE"])
def delete_insumo(id):
   insumo = Insumos.query.filter_by(id=id).first()

   try:
      db.session.delete(insumo)
      db.session.commit()
      return gera_response(200, "insumo", insumo.to_json(), "Excluído com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "insumo", {}, "Erro ao excluir")

####################################################################################      

app.run(debug=True)