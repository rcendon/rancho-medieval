from flask import render_template, session, request, redirect, url_for, flash

from app import app, db
from ..produtos.models import Produtos
from ..pedidos.models import Pedidos
from ..pessoas.models import Pessoas

from ..pedidos.forms import dados_pagamento, valida_dados_cartao


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

@app.route('/pedido')
@app.route('/pedido/<int:cliente_instancia_id>/<int:pedido_realizado_id>', methods=['GET'])
def pedido(cliente_instancia=None, pedido_realizado=None):

   if 'email' in session:

        if cliente_instancia and pedido_realizado:

            return render_template('/pedidos/detalhes_do_pedido.html', pedido_pagamento=Pedidos.query.filter_by(id=pedido_realizado.id, id_cliente=cliente_instancia.id).all()[-1])

        else:

            return render_template('/pedidos/detalhes_do_pedido.html', pedido_consulta=Pedidos.query.filter_by(id_cliente=Pessoas.query.filter_by(email=session['email']).first().id).all()[-1])

   else:

        flash('Por favor, faça o login primeiro para verificar a situação de seu último pedido.', 'info')
        return redirect(url_for('login'))




@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():

    form_opcoes_pagamento = dados_pagamento()
    form_valida_cartao = valida_dados_cartao()

    if request.method == 'POST':

        if 'email' not in session:

            flash('Por favor, faça o login em sua conta antes de finalizar a compra.', 'info')
            return redirect(url_for('login'))

        cliente_instancia = Pessoas.query.filter_by(email=session['email']).first()

        pedido_realizado = Pedidos.gera_pedido(
            {'cliente_id': cliente_instancia.id, 'estoque': Produtos.lista_produtos_em_estoque()},
            Pedidos.gera_carrinho(request.cookies, Produtos.lista_produtos_em_estoque())
        )

        if type(pedido_realizado) == bool:

            flash('Oops, pedimos desculpas mas, infelizmente, não poderemos finalizar seu pedido neste momento pois estamos momentaneamente com falta de estoque. Por favor, selecione outros itens ou uma quantidade menor dos já escolhidos.')
            return redirect(url_for('carrinho'))

        else:

            return redirect(url_for('pedido', cliente_instancia_id=cliente_instancia.id, pedido_realizado_id=pedido_realizado.id))

    carrinho_com_itens = Pedidos.gera_carrinho(request.cookies, Produtos.lista_produtos_em_estoque())
    carrinho_valor_total = Pedidos.calcula_valor_total_do_carrinhho(carrinho_com_itens)

    return render_template(
        'pedidos/carrinho.html',
        carrinho_com_itens=carrinho_com_itens,
        carrinho_valor_total=carrinho_valor_total,
        form_valida_cartao=form_valida_cartao,
        form_opcoes_pagamento=form_opcoes_pagamento
    )



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
