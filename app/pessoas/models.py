import bcrypt

from app import db
# from ..pedidos.models import Pedidos

enderecos = db.Table(
    'relacao_pessoas_enderecos',
    db.Column('pessoa_id', db.Integer, db.ForeignKey('pessoas.id'), primary_key=True),
    db.Column('endereco_id', db.Integer, db.ForeignKey('enderecos.id'), primary_key=True)
)


enderecos_fornecedores = db.Table(
    'relacao_fornecedores_enderecos',
    db.Column('fornecedor_id', db.Integer, db.ForeignKey('fornecedores.id'), primary_key=True),
    db.Column('endereco_id', db.Integer, db.ForeignKey('enderecos.id'), primary_key=True)
)

preco_insumo = db.Table(
    'preco_insumo',
    db.Column('id_fornecedor', db.Integer, db.ForeignKey('fornecedores.id'), primary_key=True),
    db.Column('id_insumo', db.Integer, db.ForeignKey('insumos.id'), primary_key=True),
    db.Column('valor', db.Float, nullable=False)
)

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
    pedidos = db.relationship('Pedidos', backref='pessoa', lazy='select', uselist=False)
    endereco = db.relationship('Enderecos', secondary=enderecos, lazy='select', uselist=False)


################################ FIM Modelo Pessoas ##################################################

################################ Modelo Fornecedores ##################################################

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

class Fornecedores(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    cnpj = db.Column(db.Integer, unique=True)
    contato = db.Column(db.Integer)
    email = db.Column(db.VARCHAR(256), unique=True)
    endereco = db.relationship('Enderecos', secondary=enderecos_fornecedores, lazy='select', uselist=False)
    preco_insumo = db.relationship('Insumos', backref='fornecedor', secondary=preco_insumo, lazy='select', uselist=False)

################################ FIM Modelo Pessoas ##################################################
################################ Modelo Endereço ##################################################

class Enderecos(db.Model):
    __tablename__ = 'enderecos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rua = db.Column(db.VARCHAR(100))
    bairro = db.Column(db.VARCHAR(100))
    cidade = db.Column(db.VARCHAR(50))
    estado = db.Column(db.VARCHAR(50))
    pais = db.Column(db.VARCHAR(40))
    numero = db.Column(db.Integer)
    complemento = db.Column(db.VARCHAR(100))
    tipo_endereco = db.Column(db.CHAR(1), nullable=False) # Valores possíveis -> R - Residencial ; C - Comercial


################################ FIM Modelo Endereço ##################################################
