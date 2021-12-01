import bcrypt

from app import db
# from ..produtos.models import Insumos
# from ..pedidos.models import Pedidos


enderecos = db.Table(
    'relacao_pessoas_enderecos',
    db.Column('pessoa_id', db.BigInteger, db.ForeignKey('pessoas.id'), primary_key=True),
    db.Column('endereco_id', db.BigInteger, db.ForeignKey('enderecos.id'), primary_key=True)
)


enderecos_fornecedores = db.Table(
    'relacao_fornecedores_enderecos',
    db.Column('fornecedor_id', db.BigInteger, db.ForeignKey('fornecedores.id', ondelete='CASCADE'), primary_key=True),
    db.Column('endereco_id', db.BigInteger, db.ForeignKey('enderecos.id', ondelete='CASCADE'), primary_key=True)
)

# preco_insumo = db.Table(
#     'preco_insumo',
#     db.Column('id_fornecedor', db.Integer, db.ForeignKey('fornecedores.id'), primary_key=True),
#     db.Column('id_insumo', db.Integer, db.ForeignKey('insumos.id'), primary_key=True),
#     db.Column('valor', db.Float, nullable=False)
# )

class Preco_insumo(db.Model):
    __tablename__ = 'preco_insumo'

    id_fornecedor = db.Column('id_fornecedor', db.BigInteger, db.ForeignKey('fornecedores.id', ondelete='CASCADE'), primary_key=True)
    id_insumo = db.Column('id_insumo', db.BigInteger, db.ForeignKey('insumos.id', ondelete='CASCADE'), primary_key=True)
    valor = db.Column('valor', db.Float, nullable=False)

    def __init__(self, id_insumo, id_fornecedor, valor):
        self.id_insumo = id_insumo
        self.id_fornecedor = id_fornecedor
        self.valor = valor


################################ Modelo Pessoas ##################################################

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

class Pessoas(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50), nullable=False)
    email = db.Column(db.VARCHAR(256), unique=True, nullable=False)
    rg = db.Column(db.BigInteger, unique=True)
    cpf = db.Column(db.BigInteger, unique=True)
    registro_diverso = db.Column(db.VARCHAR(20), unique=True)
    pais_do_registro_diverso = db.Column(db.VARCHAR(20))
    tipo = db.Column(db.CHAR(1), nullable=False)
    senha = db.Column(db.VARCHAR(256), nullable=False)
    endereco = db.relationship('Enderecos', secondary=enderecos, lazy='select', uselist=True)
    pedidos = db.relationship('Pedidos', backref='pessoa', lazy='select', uselist=True)

    def __init__(self, nome, email, rg, cpf, registro_diverso, pais_do_registro_diverso, tipo, senha):
        self.nome = nome
        self.email = email
        self.rg = rg
        self.cpf = cpf
        self.registro_diverso = registro_diverso
        self.pais_do_registro_diverso = pais_do_registro_diverso
        self.tipo = tipo
        self.senha = senha


    @staticmethod
    def adiciona_pessoa(dados_pessoais:dict, dados_endereco:dict):

        # if Pessoas.verifica_duplicidade_registro(dados_pessoais):  #or not Enderecos.verifica_possibilidade_endereco(dados_endereco)

        pessoa = Pessoas(
            dados_pessoais['nome'],
            dados_pessoais['email'],
            dados_pessoais['rg'],
            dados_pessoais['cpf'],
            dados_pessoais['registro_diverso'],
            dados_pessoais['pais_do_registro_diverso'],
            dados_pessoais['tipo'],
            dados_pessoais['senha']
        )

        endereco = Enderecos(
            dados_endereco['rua'],
            dados_endereco['bairro'],
            dados_endereco['cidade'],
            dados_endereco['estado'],
            dados_endereco['pais'],
            dados_endereco['numero'],
            dados_endereco['complemento'],
            dados_endereco['tipo_endereco']
        )

        pessoa.endereco.append(endereco)
        db.session.add(pessoa)
        db.session.commit()

        return True

    # @staticmethod
    # def verifica_duplicidade_registro(dados_pessoais):
    #
    #     dados_pessoais_essenciais = ['registro_diverso', 'cpf', 'rg', 'email']
    #
    #     for key in dados_pessoais_essenciais:
    #         if :
    #
    #             return False
    #
    #     return True


    # @staticmethod
    # def remove_pessoa():


# teste de inserção de pessoa no banco de dados -> Pessoas.adiciona_pessoa({'nome': 'Teste', 'email': 'teste@email.com', 'rg': 1111111111, 'cpf': 11111111111, 'registro_diverso': None, 'pais_do_registro_diverso': None, 'tipo': 'C', 'senha': '123'}, {'rua': 'Teste', 'bairro': 'Teste', 'cidade': 'Teste', 'estado': 'Teste', 'pais': 'teste', 'numero': 'Teste', 'complemento': 'Teste', 'tipo_endereco': 'R'})

################################ FIM Modelo Pessoas ##################################################

################################ Modelo Fornecedores ##################################################

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

class Fornecedores(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    cnpj = db.Column(db.BigInteger, unique=True)
    contato = db.Column(db.BigInteger)
    email = db.Column(db.VARCHAR(256), unique=True)
    endereco = db.relationship('Enderecos', secondary=enderecos_fornecedores, cascade="all, delete", passive_deletes=True, lazy='select', uselist=True)
    preco_insumo = db.relationship('Preco_insumo', backref='preco_insumo', cascade="all, delete", passive_deletes=True)

    def __init__(self, nome, cnpj, contato, email):
        self.nome = nome
        self.cnpj = cnpj
        self.contato = contato
        self.email = email

    @staticmethod
    def adiciona_fornecedor(dados_fornecedor:dict, dados_endereco:dict):

        # if Pessoas.verifica_duplicidade_registro(dados_pessoais):  #or not Enderecos.verifica_possibilidade_endereco(dados_endereco)

        fornecedor = Fornecedores(
            dados_fornecedor['nome'],
            dados_fornecedor['cnpj'],
            dados_fornecedor['contato'],
            dados_fornecedor['email'],
        )

        endereco = Enderecos(
            dados_endereco['rua'],
            dados_endereco['bairro'],
            dados_endereco['cidade'],
            dados_endereco['estado'],
            dados_endereco['pais'],
            dados_endereco['numero'],
            dados_endereco['complemento'],
            dados_endereco['tipo_endereco']
        )

        fornecedor.endereco.append(endereco)
        db.session.add(fornecedor)
        db.session.commit()

        return True

    @staticmethod
    def remove_fornecedor(fornecedor):

        fornecedor_instancia = Fornecedores.query.filter_by(nome=fornecedor).first()

        if fornecedor_instancia == None:

            return False

        else:

            for insumo in Preco_insumo.query.all():
                if insumo.id_fornecedor == fornecedor_instancia.id:
                    fornecedor_instancia.preco_insumo.append(insumo)

            # for endereco in enderecos_fornecedores:
            #
            #     das

            db.session.delete(fornecedor_instancia)
            db.session.commit()
            return True







# Fornecedores.adiciona_fornecedor({'nome': 'Teste', 'email': 'teste@email.com', 'cnpj': 11111111111, 'contato': None}, {'rua': 'Teste', 'bairro': 'Teste', 'cidade': 'Teste', 'estado': 'Teste', 'pais': 'teste', 'numero': 123, 'complemento': 'Teste', 'tipo_endereco': 'R'})

################################ FIM Modelo Pessoas ##################################################
################################ Modelo Endereço ##################################################

class Enderecos(db.Model):
    __tablename__ = 'enderecos'

    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    rua = db.Column(db.VARCHAR(100))
    bairro = db.Column(db.VARCHAR(100))
    cidade = db.Column(db.VARCHAR(50))
    estado = db.Column(db.VARCHAR(50))
    pais = db.Column(db.VARCHAR(40))
    numero = db.Column(db.Integer)
    complemento = db.Column(db.VARCHAR(100))
    tipo_endereco = db.Column(db.CHAR(1), nullable=False) # Valores possíveis -> R - Residencial ; C - Comercial

    def __init__(self, rua, bairro, cidade, estado, pais, numero, complemento, tipo_endereco):

        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
        self.numero = numero
        self.complemento = complemento
        self.tipo_endereco = tipo_endereco # Valores possíveis -> R - Residencial ; C - Comercial

    # @staticmethod
    # def adiciona_endereco(dados_endereco):
    #
    #     # if Enderecos.verifica_possibilidade_endereco(dados_endereco):
    #
    #     endereco = Enderecos(
    #         dados_endereco['rua'],
    #         dados_endereco['bairro'],
    #         dados_endereco['cidade'],
    #         dados_endereco['estado'],
    #         dados_endereco['pais'],
    #         dados_endereco['numero'],
    #         dados_endereco['complemento'],
    #         dados_endereco['tipo_endereco']
    #     )
    #
    #     db.session.add(endereco)
    #     db.session.commit()
    #     return True

    # @staticmethod
    # def verifica_possibilidade_endereco(dados_endereco):





################################ FIM Modelo Endereço ##################################################
