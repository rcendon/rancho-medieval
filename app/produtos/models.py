from app import db

receita = db.Table(
    "receitas",
    db.Column('id_produto', db.Integer, db.ForeignKey('cardapio.id_produto'), primary_key=True),
    db.Column('id_insumo', db.Integer, db.ForeignKey('insumos.id'))
)

################################ Modelo Cadastro Produtos ########################################################

class Produtos(db.Model):
   __tablename__ = 'cardapio' 
    
   id_produto = db.Column(db.Integer, autoincrement=True, primary_key=True)
   nome = db.Column(db.VARCHAR(40))
   quantidade_estoque_produto = db.Column(db.Integer, nullable=False)
   valor = db.Column(db.Float)
   descricao = db.Column(db.VARCHAR(40))   
   imagem = db.Column(db.Text)
   mimetype = db.Column(db.Text)
   receita = db.relationship('Insumos', backref='produto', secondary=receita, lazy='select', uselist=False)


############################### Fim Modelo Cardápio #####################################################

################################ Modelo Cadastro Pedidos ########################################################

class Insumos(db.Model):
    __tablename__ = 'insumos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    quantidade_estoque_insumo = db.Column(db.Integer, nullable=False)

############################### Fim Modelo Cardápio #####################################################
