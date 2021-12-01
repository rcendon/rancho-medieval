from app import db
from ..produtos.models import Produtos
from ..pessoas.models import Pessoas
from ..pedidos.forms import valida_dados_pagamento, valida_dados_cartao
from flask import session, request
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
    status_pagamento = db.Column(db.CHAR(1), nullable=False) # 1 - A ; # 2 - N
    status = db.Column(db.VARCHAR(15)) # 1 - Aguardando confirmação do pagamento ; 2 - Em preparação ; 3 - Preparado ; 4 - A caminho ; 5 - Entregue
    data = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, id_cliente, valor, status_pagamento, status, data):
        self.id_cliente = id_cliente
        self.valor = valor
        self. status_pagamento = status_pagamento
        self.status = status
        self.data = data

    # def insere_pedido(self, carrinho:dict):
    #     for item in carrinho:
    #         if carrinho.keys() in Produtos.query.all():

    @staticmethod
    def calcula_valor_total_do_carrinhho(carrinho):
        valor_total_do_carrinho = 0
        for item in carrinho:
            valor_total_do_carrinho += item['valor_total_do_item']
        return valor_total_do_carrinho

    @staticmethod
    def gera_carrinho(cookies):
        carrinho = []
        for produto in Produtos.query.all():
            if produto.nome in cookies.keys():
                carrinho.append({
                    'nome': produto.nome,
                    'quantidade': cookies[produto.nome],
                    'valor_unitario': produto.valor,
                    'valor_total_do_item': int(cookies[produto.nome]) * produto.valor
                })
        return sorted(carrinho, key=lambda item: item['nome'])

    # def lista_pedidos(self):

    # @staticmethod
    # def insere_pedido():
    #
    #     carrinho = Pedidos.gera_carrinho(request.cookies)
    #     pedido = Pedidos.gera_pedido(carrinho)
    #
    #     cliente = Pessoas(
    #
    #
    #     )
    #
    #     for item in carrinho
    #
    #     novo_pedido = Pedidos(
    #         pedido['id_cliente'],
    #         pedido['valor'],
    #         pedido['status_pagamento'],
    #         pedido['status'],
    #         pedido['data']
    #     )
    #
    #
    #
    #     db.session.add(novo_pedido)
    #     db.session.commit()

    @staticmethod
    def gera_pedido(carrinho:dict):
        pedido = {
            'id_cliente': Pessoas.query.filter_by(email = session['email']).id,
            'valor': Pedidos.calcula_valor_total_do_carrinhho(carrinho),
            'status': 'Aguardando confirmação do pagamento',
            'status_pagamento': Pedidos.verifica_pagamento(),
            'data': '27-11-2021 18:00:00'  # datetime.now() -> para testar depois
        }
        return pedido


    @staticmethod
    def verifica_pagamento():
        dados_pagamento = valida_dados_pagamento(request.form)

        if dados_pagamento.cartao_debito.data or valida_dados_pagamento.cartao_credito:
            if valida_dados_cartao.cartao_numero == 404404404404:
                return 'negado'
            else:
                return 'aprovado'
        else:
            return 'aprovado'


############################### Fim Modelo Pedidos #####################################################

