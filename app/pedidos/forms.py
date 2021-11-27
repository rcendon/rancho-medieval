from wtforms import Form, StringField, validators, IntegerField, DateField

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - The Forms

class valida_dados_pagamento(Form):
    cartao_credito = StringField('Cartão de Crédito', [validators.Length(min=1, max=35)])
    cartao_debito = StringField('Cartão de Débito', [validators.Length(min=1, max=10)])
    boleto = StringField('Boleto', [validators.Length(min=1, max=35)])
    pix = StringField('Pix', [validators.Length(min=1, max=35)])

class valida_dados_cartao(Form):
    cartao_numero = IntegerField('Número do cartão', [validators.Length(min=1, max=35)])
    titular_cartao_nome = IntegerField('Titular do cartão', [validators.Length(min=1, max=35)])
    titular_cartao_cpf = IntegerField('Cpf do titular do cartão', [validators.Length(min=1, max=35)])
    cartao_data_validade = DateField('Data de validade do cartão', [validators.Length(min=1, max=35)], format='%m-%Y',)
    cartao_cvc = IntegerField('CVC do cartão', [validators.Length(min=1, max=35)])
