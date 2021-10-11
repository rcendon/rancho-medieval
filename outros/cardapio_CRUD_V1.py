from flask import Flask, Response, request  #Response = Classe de Retorno da API / request = Comunicação com o body (post)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import json

####################################################################################  
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hkuxpjcwuldatj:8a0d2ed471b0e35e8aa4b8d123186db7c263dc22c6a49e33fc86578ea91bd660@ec2-44-195-201-3.compute-1.amazonaws.com:5432/dc60qmfkulhdc5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8442@localhost:5432/ranchomedievaldevelop'
db = SQLAlchemy(app) #db recebe o app Flask para automatização.
migrate = Migrate(app, db)

################################ Modelo Pessoas ######################################
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def salvar_imagem(imagem):
   if allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem.save(caminho)

            return caminho
   else:
            raise Exception("Formato inválido")
   

def atualizar_imagem(caminho_antigo_imagem, nova_imagem):
   caminho = salvar_imagem(nova_imagem)
   excluir_imagem(caminho_antigo_imagem)

   return caminho

def excluir_imagem(caminho_antigo_imagem):

   if caminho_antigo_imagem != os.path.join(app.config['UPLOAD_FOLDER'], "default.jpg"):
      os.remove(caminho_antigo_imagem)

class Cardapio(db.Model):
   __tablename__ = 'cardapio' 
    
   id_produto = db.Column(db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(50))
   quantidade_estoque_produto = db.Column(db.Integer)
   permite_estocagem = db.Column(db.CHAR(1))
   valor = db.Column(DOUBLE_PRECISION)
   imagem = db.Column(db.VARCHAR(255))
   
   def __init__(self, nome, quantidade_estoque_produto, permite_estocagem, valor, imagem):
       self.nome = nome
       self.quantidade_estoque_produto = quantidade_estoque_produto
       self.permite_estocagem = permite_estocagem
       self.valor = valor
       self.imagem = imagem
  
   def to_json(self):
      return{"cardapio_id": self.id_produto, "nome": self.nome, "quantidade_estoque_produto": self.quantidade_estoque_produto, 
      "permite_estocagem":self.permite_estocagem, "valor": self.valor, "imagem": self.imagem} 

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
   body = request.form.to_dict()
   try:
      imagem = os.path.join(app.config['UPLOAD_FOLDER'], "default.jpg")
      if len(request.files) > 0:
         imagem = salvar_imagem(request.files['imagem'])

      cardapio = Cardapio(nome=body["nome"], 
                          quantidade_estoque_produto=int(body["quantidade_estoque_produto"]), 
                          permite_estocagem=body["permite_estocagem"],
                          valor=float(body["valor"]),
                          imagem = imagem
                          )
      
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
   cardapio = Cardapio.query.filter_by(id_produto=id).first()
   caminho_imagem_antiga = cardapio.imagem
   #Modificações
   body = request.form.to_dict()
   if len(request.files) > 0:
      imagem_nova = request.files['imagem']
   else:
      imagem_nova = "default.jpg"
   
   try:
      
      cardapio.nome = body["nome"]
      cardapio.quantidade_estoque_produto = int(body["quantidade_estoque_produto"])
      cardapio.permite_estocagem = body["permite_estocagem"]
      cardapio.valor = float(body["valor"])

      if imagem_nova == "default.jpg":
         excluir_imagem(caminho_imagem_antiga)
         cardapio.imagem = os.path.join(app.config['UPLOAD_FOLDER'], imagem_nova)
      else:
         if caminho_imagem_antiga != os.path.join(app.config['UPLOAD_FOLDER'], imagem_nova.filename):
            cardapio.imagem = atualizar_imagem(caminho_imagem_antiga, imagem_nova)


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
   cardapio = Cardapio.query.filter_by(id_produto=id).first()

   try:
      
      db.session.delete(cardapio)
      excluir_imagem(cardapio.imagem)
      db.session.commit()
      return gera_response(200, "cardapio", cardapio.to_json(), "Excluído com sucesso")

   except Exception as e:
      print(e)
      return gera_response(400, "cardapio", {}, "Erro ao excluir")
####################################################################################      

app.run(debug=True)
