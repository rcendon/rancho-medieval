from wtforms.fields import StringField, IntegerField, SubmitField, FloatField, SelectField, SelectMultipleField, FileField
from wtforms.validators import length, InputRequired, NumberRange, ValidationError
from flask_wtf import FlaskForm
from .models import Produtos, Insumos
from ..pessoas.models import Fornecedores

######################### Classe Cadastro de Produtos ##################################################

class CadastroProdutos(FlaskForm):

    nome = StringField('Nome', validators=[InputRequired(), length(min=1, max=256)])
    quantidade_estoque_produto = IntegerField('Quantidade em estoque', validators=[InputRequired(), NumberRange(min=0, max=100)])
    valor = FloatField('Valor', validators=[InputRequired(), NumberRange(min=0, max=500)])
    descricao = StringField('Descrição', validators=[InputRequired(), length(min=0, max=100)])
    imagem = FileField('Imagem')
    mimetype = StringField('Mimetype', validators=[length(min=1, max=100)])
    insumos_utilizados = SelectMultipleField('Insumos utilizados', choices=Insumos.lista_insumos(), validators=[InputRequired()])
    submit = SubmitField('Registrar')

    def validate_nome(self, nome):
        if Produtos.query.filter_by(nome=nome.data).first():
            return ValidationError("Já existe um produto cadastrado com esse nome.")

class CadastroInsumos(FlaskForm):

    nome = StringField('Nome', validators=[InputRequired(), length(min=1, max=256)])
    quantidade_estoque_insumo = IntegerField('Quantidade em estoque', validators=[InputRequired(), NumberRange(min=0, max=100)])
    valor = FloatField('Valor', validators=[InputRequired(), NumberRange(min=0, max=500)])
    fornecedores = SelectMultipleField('Fornecedores', default='-', choices=Fornecedores.lista_fornecedores(), validators=[InputRequired()])
    descricao = StringField('Descricao', validators=[length(min=0, max=100)])
    submit = SubmitField('Registrar')

    def validate_nome(self, nome):
        if Produtos.query.filter_by(nome=nome.data).first():
            return ValidationError("Já existe um insumo cadastrado com esse nome.")
