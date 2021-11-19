from appdelivery import db

enderecos = db.Table(
    'relacao_pessoas_enderecos',
    db.Column('pessoa_id', db.Integer, db.ForeignKey('pessoas.id'), primary_key=True),
    db.Column('endereco_id', db.Integer, db.ForeignKey('enderecos.id'))
)

################################ Modelo Pessoas ##################################################

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

class Pessoas(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    email = db.Column(db.VARCHAR(256), unique=True, nullable=False)
    rg = db.Column(db.Integer, unique=True)
    cpf = db.Column(db.Integer, unique=True)
    registro_diverso = db.Column(db.VARCHAR(20), unique=True)
    pais_do_registro_diverso = db.Column(db.VARCHAR(20))
    tipo = db.Column(db.CHAR(1))
    senha = db.Column(db.VARCHAR(128))
    pedidos = db.relationship('Pedidos', lazy='select', uselist=False)
    endereco = db.relationship('Enderecos', secondary=enderecos, lazy='select', uselist=False)


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
    tipo_endereco = db.Column(db.CHAR(1)) # Valores possíveis -> R - Residencial ; C - Comercial


################################ FIM Modelo Pessoas ##################################################
