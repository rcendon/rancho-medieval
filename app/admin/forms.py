######## USUÁRIOS INTERNOS ########

from wtforms.fields import StringField, PasswordField, IntegerField, SelectField, SubmitField, SelectMultipleField, FloatField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import length, InputRequired, NumberRange, ValidationError
from flask_wtf import FlaskForm
from app.pessoas.models import Pessoas, Fornecedores
from app.pedidos.models import Pedidos
from app.produtos.models import Produtos, Insumos, Receitas

######################### Classe Form Cadastro ##################################################


class FormularioDadosPessoaisColaborador(FlaskForm):
    nome = StringField(
        'Nome', validators=[
            InputRequired(message="Por favor, preencha este campo antes de prosseguir."),
            length(min=1, max=50, message="Por favor, reduza a quantidade de dígitos no campo antes de prosseguir. ")
        ]
    )
    email = EmailField('E-mail', validators=[InputRequired(), length(min=2, max=35)])
    rg = IntegerField('RG', validators=[NumberRange(min=1000000000, max=9999999999)])
    cpf = IntegerField('CPF', validators=[NumberRange(min=10000000000, max=99999999999)])
    tipo = SelectField('Tipo', default='-', choices=['-', 'Funcionário', 'Administrador'], validators=[InputRequired()])
    senha = PasswordField('Senha', validators=[InputRequired(), length(min=1, max=35)])
    rua = StringField('Rua', validators=[InputRequired(), length(min=1, max=100)])
    bairro = StringField('Bairro', validators=[InputRequired(), length(min=1, max=100)])
    numero = IntegerField('Número', validators=[InputRequired(), NumberRange(min=1, max=9999)])
    complemento = StringField('Complemento', validators=[length(min=0, max=50)])
    cep = IntegerField('CEP', validators=[InputRequired(), NumberRange(min=10000000, max=99999999)])
    cidade = StringField('Cidade', validators=[InputRequired(), length(min=1, max=50)])
    estado = SelectField('Estado', validators=[InputRequired()], choices=['-', 'Bahia', 'São Paulo'])
    pais = StringField('País', validators=[InputRequired(), length(min=1, max=40)])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        pessoa_instancia = Pessoas.query.filter_by(email=email.data).first()
        if pessoa_instancia:
            raise ValidationError("Já existe usuário com esse e-mail, por favor indique outro.")

    def validate_cpf(self, cpf):
        pessoa_instancia = Pessoas.query.filter_by(cpf=cpf.data).first()
        if pessoa_instancia:
            raise ValidationError("Já existe usuário com esse CPF, por favor indique outro.")

    def validate_rg(self, rg):
        pessoa_instancia = Pessoas.query.filter_by(rg=rg.data).first()
        if pessoa_instancia:
            raise ValidationError("Já existe usuário com esse RG, por favor indique outro.")

    def validate_estado(self, estado):
        if estado.data == '-':
            raise ValidationError("Por favor, escolha alguma das opções na lista.")

    def validate_tipo(self, tipo):
        if tipo.data == '-':
            raise ValidationError("Por favor, escolha alguma das opções na lista.")

######################### Classe Form Login ##################################################


class LoginFormularioCli(FlaskForm):
    email = EmailField('E-mail', validators=[InputRequired(), length(min=2, max=35)])
    senha = PasswordField('Senha', validators=[InputRequired(), length(min=8, max=35)])
    submit = SubmitField("Login")

    def validate_email(self, email):

        pessoa_instancia = Pessoas.query.filter_by(email=email.data).first()

        if pessoa_instancia:

            if pessoa_instancia.tipo == 'C':

                raise ValidationError("Apenas usuários de colaboradores podem realizar o acesso por esta página.")


class FormularioEdicaoInsumos(FlaskForm):
    email = EmailField('E-mail', validators=[InputRequired(), length(min=2, max=35)])
    senha = PasswordField('Senha', validators=[InputRequired(), length(min=8, max=35)])
    submit = SubmitField("Login")

    def validate_email(self, email):

        pessoa_instancia = Pessoas.query.filter_by(email=email.data).first()

        if pessoa_instancia:

            if pessoa_instancia.tipo == 'C':
                raise ValidationError("Apenas usuários de colaboradores podem realizar o acesso por esta página.")


class FormularioAssociaInsumoFornecedor(FlaskForm):

    insumo = SelectField('Insumo', validators=[InputRequired()])
    fornecedor = SelectField('Fornecedor', validators=[InputRequired()])
    valor = FloatField('Valor', validators=[InputRequired(), NumberRange(min=0, max=300)])
    submit = SubmitField('Registrar')

    def __init__(self):
        super(FormularioAssociaInsumoFornecedor, self).__init__()
        self.fornecedor.choices = [(fornecedor.nome, fornecedor.nome) for fornecedor in Fornecedores.query.all()]
        self.insumo.choices = [(insumo.nome, insumo.nome) for insumo in Insumos.query.all()]


class FormularioDesassociaInsumoFornecedor(FlaskForm):

    insumo = SelectField('Insumo', validators=[InputRequired()])
    fornecedor = SelectField('Fornecedor', validators=[InputRequired()])
    submit = SubmitField('Desvincular')

    def __init__(self):
        super(FormularioDesassociaInsumoFornecedor, self).__init__()
        self.fornecedor.choices = [(fornecedor.nome, fornecedor.nome) for fornecedor in Fornecedores.query.all()]
        self.insumo.choices = [(insumo.nome, insumo.nome) for insumo in Insumos.query.all()]


class FormularioBuscaProdutos(FlaskForm):
    produto = SelectField('Produto', validators=[InputRequired()])
    submit = SubmitField('Buscar')

    def __init__(self):
        super(FormularioBuscaProdutos, self).__init__()
        self.produto.choices = [(produto.nome, produto.nome) for produto in Produtos.query.all()]


class FormularioEdicaoInsumosEmReceita(FlaskForm):

    insumo = SelectField('Insumo', validators=[InputRequired()])
    quantidade = IntegerField('Quantidade', validators=[NumberRange(min=1, max=30)])
    submit = SubmitField('Registrar quantidade na receita')

    def __init__(self, produto_id=None):
        super(FormularioEdicaoInsumosEmReceita, self).__init__()
        self.insumo.choices = [(insumo, insumo) for insumo in Produtos.lista_insumos_de_receita(produto_id)]


class FormularioEdicaoProdutos(FlaskForm):

    quantidade_estoque_produto = IntegerField('Quantidade em estoque', validators=[InputRequired(), NumberRange(min=0, max=400)])
    valor = FloatField('Valor', validators=[InputRequired(), NumberRange(min=0, max=500)])
    descricao = StringField('Descrição', validators=[InputRequired(), length(min=0, max=100)])
    imagem = FileField('Imagem')
    # mimetype = StringField('Mimetype', validators=[length(min=1, max=100)])
    insumos_utilizados = SelectMultipleField('Insumos utilizados', validators=[InputRequired()])
    submit = SubmitField('Registrar')

    def __init__(self):
        super(FormularioEdicaoProdutos, self).__init__()
        self.insumos_utilizados.choices = [(insumo, insumo) for insumo in Insumos.lista_insumos()]


class FormularioEdicaoFornecedores(FlaskForm):
    email = EmailField('E-mail', validators=[InputRequired(), length(min=2, max=35)])
    senha = PasswordField('Senha', validators=[InputRequired(), length(min=8, max=35)])
    submit = SubmitField("Login")

    def validate_email(self, email):

        pessoa_instancia = Pessoas.query.filter_by(email=email.data).first()

        if pessoa_instancia:

            if pessoa_instancia.tipo == 'C':
                raise ValidationError("Apenas usuários de colaboradores podem realizar o acesso por esta página.")


class FormularioRemocaoFornecedores(FlaskForm):
    fornecedores = SelectMultipleField('Fornecedor', validators=[InputRequired()])
    submit = SubmitField("Remover")

    def __init__(self):
        super(FormularioRemocaoFornecedores, self).__init__()
        self.fornecedores.choices = [(fornecedor.nome, fornecedor.nome) for fornecedor in Fornecedores.query.all()]


class FormularioRemocaoColaboradores(FlaskForm):
    colaborador = SelectField('Colaborador', choices=[(colaborador.nome, colaborador.nome) for colaborador in Pessoas.query.filter_by(tipo='F').all()], validators=[InputRequired()])
    submit = SubmitField("Remover")

    def __init__(self, produto_id=None):
        super(FormularioRemocaoColaboradores, self).__init__()
        self.colaborador.choices = [(colaborador.nome, colaborador.nome) for colaborador in Pessoas.query.filter_by(tipo='F').all()]


class FormularioAlteraStatusPedido(FlaskForm):
    pedido_em_aberto = SelectField('Pedido', validators=[InputRequired()])
    status = SelectField('Status', choices=['Em preparação', 'Preparado', 'A caminho', 'Entregue'])
    submit = SubmitField('Registrar')

    def __init__(self):
        super(FormularioAlteraStatusPedido, self).__init__()
        self.pedido_em_aberto.choices = [(pedido.id, pedido.id) for pedido in Pedidos.query.filter(Pedidos.status.in_(['Aguardando confirmação do pagamento', 'Em preparação', 'Preparado', 'A caminho'])).all() if pedido.status_pagamento == 'A']


class FormularioAlteraStatusPedidoParaBanca(FlaskForm):
    pedido_em_aberto = SelectField('Pedido', validators=[InputRequired()])
    status = SelectField('Status', choices=['Em preparação', 'Preparado', 'A caminho', 'Entregue', 'Negado por falta de pagamento'])
    submit = SubmitField('Registrar')

    def __init__(self):
        super(FormularioAlteraStatusPedidoParaBanca, self).__init__()
        self.pedido_em_aberto.choices = [(pedido.id, pedido.id) for pedido in Pedidos.query.filter(Pedidos.status.in_(['Aguardando confirmação do pagamento', 'Em preparação', 'Preparado', 'A caminho'])).all() if (pedido.status_pagamento == 'P' or pedido.status_pagamento == 'A')]
