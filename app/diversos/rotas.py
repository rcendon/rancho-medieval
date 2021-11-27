from flask import render_template, session, request, redirect, url_for, flash

from app import app, db

from ..produtos.models import Produtos
from ..pedidos.models import Pedidos

from ..pedidos.forms import valida_dados_pagamento, valida_dados_cartao


##################### Rota Área de Entrega ####################################################

@app.route('/entrega')
def entrega():
    return render_template('/diversos/entrega.html')

@app.route('/pedido', methods=['POST'])
def pedido():
    if 'email' not in session:
        session['processo_pagamento'] = True
        return render_template('clientes/loginclientepagamento.html')
    else:
        Pedidos.insere_pedido()
        return render_template('index.html')

# @app.route('/processa_pagamento', methods=['POST'])







@app.route('/pagamento')
def tela_pagamento():
    carrinho = Pedidos.gera_carrinho(request.cookies)
    carrinho_valor_total = Pedidos.calcula_valor_total_do_carrinhho(carrinho)

    return render_template('diversos/pagamento.html', carrinho=carrinho, carrinho_valor_total=carrinho_valor_total)