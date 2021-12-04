from wtforms.fields import StringField, PasswordField, IntegerField, SelectField, SubmitField, FloatField
from wtforms.validators import length, InputRequired, NumberRange, ValidationError
from flask_wtf import FlaskForm
from .models import Produtos

######################### Classe Cadastro de Produtos ##################################################

class CadastroProdutos(FlaskForm):

    nome = StringField('Nome', validators=[InputRequired(), length(min=1, max=256)])
    quantidade_estoque_produto = IntegerField('Quantidade em estoque', validators=[InputRequired(), NumberRange(min=0, max=100)])
    valor = FloatField('Contato', validators=[InputRequired(), NumberRange(min=0, max=500)])
    descricao = StringField('Rua', validators=[InputRequired(), length(min=0, max=100)])
    imagem = StringField('Rua', validators=[InputRequired(), length(min=1, max=100)])
    mimetype = StringField('Rua', validators=[InputRequired(), length(min=1, max=100)])
