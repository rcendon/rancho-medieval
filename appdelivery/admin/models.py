from appdelivery import db

#self.nome = nome
#self.email = email
#self.telefone = telefone
#self.rg = rg
#self.cpf = cpf
#self.endereco = endereco
#self.senha = senha

################################ Modelo Pessoas ##################################################

#https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

class User(db.Model):
    __tablename__ = 'usuariosinternos' 
        
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    email = db.Column(db.VARCHAR(30))
    telefone = db.Column(db.String(11))
    rg = db.Column(db.String(10))      
    cpf = db.Column(db.String(11))    
    endereco = db.Column(db.VARCHAR(50))
    senha = db.Column(db.VARCHAR(180))

    def __init__(self, nome, email, telefone, rg, cpf, endereco, senha):
       self.nome = nome
       self.email = email
       self.telefone = telefone
       self.rg = rg       
       self.cpf = cpf       
       self.endereco = endereco
       self.senha = senha

#db.create_all()

################################ FIM Modelo Pessoas ##################################################

################################ Modelo Cardápio ########################################################

class Produtos(db.Model):
   __tablename__ = 'cardapio' 
    
   id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(40))
   quantidade_estoque = db.Column(db.Integer)
   valor = db.Column(db.Integer)
   #Upload Imagem
   
   def __init__(self, nome, quantidade_estoque, valor):
       self.nome = nome
       self.quantidade_estoque = quantidade_estoque
       self.valor = valor

#db.create_all()
############################### Fim Modelo Cardápio #####################################################
