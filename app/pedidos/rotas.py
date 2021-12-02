from flask import render_template, session, request, redirect, url_for, flash

from app import app, db

from ..produtos.models import Produtos
from ..pedidos.models import Pedidos
from ..pessoas.models import Pessoas

from ..pedidos.forms import valida_dados_pagamento, valida_dados_cartao


##################### Rota Área de Entrega ####################################################

@app.route('/entrega')
def entrega():
    return render_template('clientes/entrega.html')

@app.route('/processa_pedido/<int:cliente_id>/<int:pedido_id>', methods=['POST'])
def processa_pedido(id_cliente, pedido_id):
    if 'email' not in session:
        session['processo_pagamento'] = True
        return render_template('clientes/loginclientepagamento.html')
    else:
        Pedidos.insere_pedido()
        return render_template('index.html')

@app.route('/pedido/<int:cliente_id>/<int:pedido_id>', methods=['POST'])
def resumo_pedido(cliente_id, pedido_id):

    if 'email' not in session:
        flash('Por favor, faça o login em sua conta antes de finalizar a compra.', 'success')
    Pessoas.query.filter_by(email=session['email']).id,

@app.route('/carrinho')
def carrinho():

    if 'email' in session:

        cliente = Pessoas.query.filter_by(email=session['email']).first()
        carrinho = Pedidos.gera_carrinho(cliente.id, request.cookies)
    carrinho_valor_total = Pedidos.calcula_valor_total_do_carrinhho(carrinho)

    return render_template('pedidos/carrinho.html', carrinho=carrinho, carrinho_valor_total=carrinho_valor_total)



    # def verifica_pagamento_com_API_externa(dados_pedido:dict):
    #
    #     dados_pagamento =
    #
    #     if dados_pagamento.cartao_debito.data or valida_dados_pagamento.cartao_credito:
    #         if valida_dados_cartao.cartao_numero == 404404404404:
    #             return 'negado'
    #         else:
    #             return 'aprovado'
    #     else:
    #         return 'aprovado'
