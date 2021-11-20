from appdelivery import db


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

# db.create_all()

############################### Fim Modelo Cardápio #####################################################

################################ Modelo Cadastro Pedidos ########################################################

class Pedidos(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    quantidade_estoque_produto = db.Column(db.Integer)
    valor = db.Column(db.Integer)
    descricao = db.Column(db.VARCHAR(40))
    # imagem = db.Column(db.Text)
    # mimetype = db.Column(db.Text)

    # db.create_all()


############################### Fim Modelo Cardápio #####################################################
