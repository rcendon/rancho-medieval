from app import db
from datetime import datetime

itens_do_pedido = db.Table(
    'itens_do_pedido',
    db.Column('id_pedido', db.Integer, db.ForeignKey('pedidos.id'), primary_key=True),
    db.Column('id_produto', db.Integer, db.ForeignKey('cardapio.id_produto'), primary_key=True)
)

################################ Modelo Cadastro Pedidos ########################################################

class Pedidos(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status_pagamento = db.Column(db.CHAR(1), nullable=False) # 1 - A ; # 2 - N ; # 3 - P
    status = db.Column(db.VARCHAR(40), nullable=False) # 1 - Aguardando confirmação do pagamento ; 2 - Em preparação ; 3 - Preparado ; 4 - A caminho ; 5 - Entregue
    data = db.Column(db.TIMESTAMP, nullable=False)
    produtos = db.relationship('Produtos', secondary=itens_do_pedido, backref='pedidos', lazy='select', uselist=True)

    def __init__(self, id_cliente, valor, status_pagamento, status, data):
        self.id_cliente = id_cliente
        self.valor = valor
        self. status_pagamento = status_pagamento
        self.status = status
        self.data = data

    @staticmethod
    def calcula_valor_total_do_carrinhho(carrinho):
        valor_total_do_carrinho = 0
        for item in carrinho:
            valor_total_do_carrinho += item['valor_total_do_item']
        return valor_total_do_carrinho

    @staticmethod
    def gera_carrinho(cookies, lista_produtos_com_estoque):
        carrinho = []
        for produto in lista_produtos_com_estoque:
            if produto.nome in cookies.keys():
                carrinho.append({
                    'nome': produto.nome,
                    'quantidade': int(cookies[produto.nome]),
                    'valor_unitario': produto.valor,
                    'valor_total_do_item': int(cookies[produto.nome]) * produto.valor,
                    'produto': produto
                })
        return sorted(carrinho, key=lambda item: item['nome'])

    @staticmethod
    def gera_pedido(dados_pedido:dict, carrinho:list):

        if len(carrinho) == 0:

            return False

        else:

            pedido = Pedidos(
                dados_pedido['cliente_id'],
                Pedidos.calcula_valor_total_do_carrinhho(carrinho),
                'P',
                'Aguardando confirmação do pagamento',
                '2021-11-28 18:00:00'  # datetime.now() -> para testar depois
            )

        for item_carrinho in carrinho:

            if item_carrinho['quantidade'] > item_carrinho['produto'].quantidade_estoque_produto:

                return False

            else:

                item_carrinho['produto'].quantidade_estoque_produto -= item_carrinho['quantidade']
                db.session.add(item_carrinho['produto'])

        db.session.add(pedido)
        db.session.commit()
        return pedido

    @staticmethod
    def altera_status_pagamento(dados_pedido:dict, status_novo):

        pedido = Pedidos.query.filter_by(id_cliente=dados_pedido['id_cliente'], data=dados_pedido['data']).first()

        if pedido == None:

            return False

        else:

            pedido.status_pagamento = status_novo
            db.session.add(pedido)
            db.session.commit()
            return True

    @staticmethod
    def lista_pedidos(cliente_id=None):

        if cliente_id == None:

            pedidos = Pedidos.query.all()

        else:

            pedidos = Pedidos.query.filter_by(id_cliente=cliente_id).all()

        return pedidos

############################### Fim Modelo Pedidos #####################################################

