from wtforms.fields import StringField, IntegerField, SubmitField, DateField, RadioField
from wtforms.validators import InputRequired, NumberRange, ValidationError
from flask_wtf import FlaskForm
from app.pessoas.models import Pessoas

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - The Forms

class dados_pagamento(FlaskForm):
    opcoes_pagamento = RadioField(choices=['Cartão de crédito', 'Cartão de débito', 'Boleto', 'Pix'])
    submit = SubmitField('Finalizar pedido')

class valida_dados_cartao(FlaskForm):
    cartao_numero = IntegerField('Número do cartão', validators=[NumberRange(min=1000000000000000, max=9999999999999999)])
    titular_cartao_nome = StringField('Titular do cartão')
    titular_cartao_cpf = IntegerField('CPF', validators=[NumberRange(min=10000000000, max=99999999999)])
    cartao_data_validade = DateField('Data de validade do cartão', format='%m-%Y',)
    cartao_cvc = IntegerField('CVC do cartão', validators=[NumberRange(min=3, max=3)])
