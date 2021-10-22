from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from __init__ import db
from __init__ import db_cardapio


################################ Modelo Pessoas ##########################################################
#########################################################################################################

class Pessoas(UserMixin, db.Model): #Modelo Pessoas
   __tablename__ = 'pessoas' 
    
   id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(50), nullable=False)
   email = db.Column(db.VARCHAR(1000), unique=True, nullable=False)  
   rg = db.Column(db.String(10), nullable=False)
   cpf = db.Column(db.String(12), nullable=False)
   tipo = db.Column(db.CHAR(1), nullable=False)
   #endereco = db.Column(db.Integer)
   senha = db.Column(db.VARCHAR(164), nullable=False)

   def __init__(self, nome, email, rg, cpf, tipo, senha):
       self.nome = nome
       self.email = email
       self.rg = rg
       self.cpf = cpf
       self.tipo = tipo
       #self.endereco = endereco
       self.senha = senha

############################### Fim Modelo Pessoas #####################################################
########################################################################################################

############################### Modelo Cardápio ########################################################
#########################################################################################################

class Cardapio(db_cardapio.Model):
   __tablename__ = 'cardapio' 
    
   id_produto = db_cardapio.Column(db_cardapio.Integer, autoincrement=True, primary_key=True)
   nome = db_cardapio.Column(db_cardapio.VARCHAR(50))
   quantidade_estoque_produto = db_cardapio.Column(db.Integer)
   permite_estocagem = db_cardapio.Column(db_cardapio.CHAR(1))
   valor = db_cardapio.Column(DOUBLE_PRECISION)
   
   def __init__(self, nome, quantidade_estoque_produto, permite_estocagem, valor):
       self.nome = nome
       self.quantidade_estoque_produto = quantidade_estoque_produto
       self.permite_estocagem = permite_estocagem
       self.valor = valor

############################### Fim Modelo Cardápio #####################################################
########################################################################################################