from app import db
from ..produtos.models import Produtos

itens_do_pedido = db.Table(
    'itens_do_pedido',
    db.Column('id_pedido', db.Integer, db.ForeignKey('pedidos.id'), primary_key=True),
    db.Column('id_produto', db.Integer, db.ForeignKey('cardapio.id_produto'))
)

################################ Modelo Cadastro Pedidos ########################################################

class Pedidos(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    valor = db.Column(db.Float)
    status = db.Column(db.CHAR(1))

############################### Fim Modelo Pedidos #####################################################
