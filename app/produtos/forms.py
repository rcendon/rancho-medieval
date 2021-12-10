from wtforms.fields import StringField, IntegerField, SubmitField, FloatField, SelectField, SelectMultipleField, FileField
from wtforms.validators import length, InputRequired, NumberRange, ValidationError
from flask_wtf import FlaskForm
from .models import Produtos, Insumos
from ..pessoas.models import Fornecedores

######################### Classe Cadastro de Produtos ##################################################

class CadastroProdutos(FlaskForm):

    nome = StringField('Nome', validators=[InputRequired(), length(min=1, max=256)])
    quantidade_estoque_produto = IntegerField('Quantidade em estoque', validators=[InputRequired(), NumberRange(min=0, max=400)])
    valor = FloatField('Valor', validators=[InputRequired(), NumberRange(min=0, max=500)])
    descricao = StringField('Descrição', validators=[InputRequired(), length(min=0, max=100)])
    imagem = FileField('Imagem')
    # mimetype = StringField('Mimetype', validators=[length(min=1, max=100)])
    insumos_utilizados = SelectMultipleField('Insumos utilizados', validators=[InputRequired()])
    submit = SubmitField('Registrar')

    def validate_nome(self, nome):
        if Produtos.query.filter_by(nome=nome.data).first():
            return ValidationError("Já existe um produto cadastrado com esse nome.")

    def __init__(self):
        super(CadastroProdutos, self).__init__()
        self.insumos_utilizados.choices = [(insumo, insumo) for insumo in Insumos.lista_insumos()]


class AdicionaProdutoEstoque(FlaskForm):
    produto_nome = SelectField('Produto', default='-', validators=[InputRequired()])
    quantidade = IntegerField('Quantidade', validators=[InputRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Adicionar')

    def validate_quantidade(self, quantidade):

        if quantidade.data <= 0:

            raise ValidationError("Por favor, insira uma quantidade maior que 0.")

    def __init__(self):
        super(AdicionaProdutoEstoque, self).__init__()
        self.produto_nome.choices = [produto.nome for produto in Produtos.query.all()]


class CadastroInsumos(FlaskForm):

    nome = StringField('Nome', validators=[InputRequired(), length(min=1, max=256)])
    quantidade_estoque_insumo = IntegerField('Quantidade em estoque', validators=[InputRequired(), NumberRange(min=0, max=100)])
    # valor = FloatField('Valor', validators=[InputRequired(), NumberRange(min=0, max=500)])
    # fornecedores = SelectMultipleField('Fornecedores', default='-', choices=Fornecedores.lista_fornecedores(), validators=[InputRequired()])
    submit = SubmitField('Registrar')

    def validate_nome(self, nome):
        if Insumos.query.filter_by(nome=nome.data).first():
            return ValidationError("Já existe um insumo cadastrado com esse nome.")

class AdicionaInsumoEstoque(FlaskForm):
    insumo_nome = SelectField('Insumo', default='-', validators=[InputRequired()])
    quantidade = IntegerField('Quantidade', validators=[InputRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Adicionar')

    def validate_quantidade(self, quantidade):

        if quantidade.data <= 0:

            raise ValidationError("Por favor, insira uma quantidade maior que 0.")

    def __init__(self):
        super(AdicionaInsumoEstoque, self).__init__()
        self.insumo_nome.choices = [insumo.nome for insumo in Insumos.query.all()]
