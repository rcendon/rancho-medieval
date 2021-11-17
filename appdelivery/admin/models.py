from appdelivery import db

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

################################ FIM Modelo Pessoas ##################################################

################################ Modelo Cadastro Produtos ########################################################

class Produtos(db.Model):
   __tablename__ = 'cardapio' 
    
   id_produto = db.Column(db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(40))
   quantidade_estoque_produto = db.Column(db.Integer)
   valor = db.Column(db.Integer)
   descricao = db.Column(db.VARCHAR(40))   
   # imagem = db.Column(db.Text)
   # mimetype = db.Column(db.Text)
   
############################### Fim Modelo Cardápio #####################################################
