from flask import render_template, session, request, redirect, url_for, flash

from app import app, db

from ..produtos.models import Produtos


##################### Rota Área de Entrega ####################################################

@app.route('/entrega')
def entrega():
    return render_template('/diversos/entrega.html')

@app.route('/processa_pagamento')
def processa_pagamento():
    if request.method == "POST":
        if 'carrinho' not in session or session['carrinho'] == '':
            session['carrinho'] = []


@app.route('/pagamento')
def tela_pagamento():
    cookies = request.cookies
    cookies_chaves = cookies.keys()
    carrinho = []
    carrinho_valor_total = 0
    for produto in Produtos.query.all():
        if produto.nome in cookies_chaves:
            valor_total = int(cookies[produto.nome]) * produto.valor
            carrinho_valor_total += valor_total
            carrinho.append({
                'nome': produto.nome,
                'quantidade': cookies[produto.nome],
                'valor': valor_total
            })
            # carrinho.sort() # - Rafael : ainda estou investigando o motivo do sort gerar um bug

    return render_template('diversos/pagamento.html', carrinho=carrinho, carrinho_valor_total=carrinho_valor_total)