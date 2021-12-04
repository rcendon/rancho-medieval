from app import bcrypt

from app import db


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
    tipo = db.Column(db.CHAR(1), nullable=False) # Três tipos: "C" para clientes ; "F" para funcionarios ; "A" para administradores
    senha = db.Column(db.VARCHAR(256), nullable=False)
    endereco = db.relationship('Enderecos', secondary=enderecos, lazy='select', uselist=True)
    pedidos = db.relationship('Pedidos', backref='pessoa', lazy='select', uselist=True)

    def __init__(self, nome, email, rg, cpf, tipo, senha):
        self.nome = nome
        self.email = email
        self.rg = rg
        self.cpf = cpf
        self.tipo = tipo
        self.senha = senha


    @staticmethod
    def adiciona_pessoa(dados_pessoais):

        pessoa = Pessoas(
            dados_pessoais.nome.data,
            dados_pessoais.email.data,
            dados_pessoais.rg.data,
            dados_pessoais.cpf.data,
            'C',
            bcrypt.generate_password_hash(dados_pessoais.senha.data).decode('utf-8')
        )

        endereco = Enderecos(
            dados_pessoais.rua.data,
            dados_pessoais.bairro.data,
            dados_pessoais.cidade.data,
            dados_pessoais.estado.data,
            dados_pessoais.pais.data,
            dados_pessoais.numero.data,
            dados_pessoais.complemento.data,
            'C',
            dados_pessoais.cep.data
        )

        pessoa.endereco.append(endereco)
        db.session.add(pessoa)
        db.session.commit()

        return True




    # @staticmethod
    # def remove_pessoa():


################################ FIM Modelo Pessoas ##################################################

################################ Modelo Fornecedores ##################################################

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

class Fornecedores(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    cnpj = db.Column(db.BigInteger, unique=True, nullable=False)
    contato = db.Column(db.BigInteger)
    email = db.Column(db.VARCHAR(256), unique=True, nullable=False)
    endereco = db.relationship('Enderecos', secondary=enderecos_fornecedores, cascade="all, delete", passive_deletes=True, lazy='select', uselist=True)
    preco_insumo = db.relationship('Preco_insumo', backref='preco_insumo', cascade="all, delete", passive_deletes=True)

    def __init__(self, nome, cnpj, contato, email):
        self.nome = nome
        self.cnpj = cnpj
        self.contato = contato
        self.email = email

    @staticmethod
    def adiciona_fornecedor(dados_fornecedor:dict):

        # if Pessoas.verifica_duplicidade_registro(dados_pessoais):  #or not Enderecos.verifica_possibilidade_endereco(dados_endereco)

        fornecedor = Fornecedores(
            dados_fornecedor['nome'],
            dados_fornecedor['cnpj'],
            dados_fornecedor['contato'],
            dados_fornecedor['email'],
        )

        endereco = Enderecos(
            dados_fornecedor['rua'],
            dados_fornecedor['bairro'],
            dados_fornecedor['cidade'],
            dados_fornecedor['estado'],
            dados_fornecedor['pais'],
            dados_fornecedor['numero'],
            dados_fornecedor['complemento'],
            dados_fornecedor['tipo_endereco'],
            dados_fornecedor['cep']
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

    @staticmethod
    def lista_fornecedores():

        lista_fornecedores = []

        for fornecedor in Fornecedores.query.all():

            lista_fornecedores.append(fornecedor.nome)

        return sorted(lista_fornecedores)



################################ FIM Modelo Pessoas ##################################################
################################ Modelo Endereço ##################################################

class Enderecos(db.Model):
    __tablename__ = 'enderecos'

    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    rua = db.Column(db.VARCHAR(100))
    bairro = db.Column(db.VARCHAR(100))
    numero = db.Column(db.Integer)
    complemento = db.Column(db.VARCHAR(100))
    tipo_endereco = db.Column(db.CHAR(1), nullable=False) # Valores possíveis -> R - Residencial ; C - Comercial
    cep = db.Column(db.BigInteger, nullable=False)
    cidade = db.Column(db.VARCHAR(50))
    estado = db.Column(db.VARCHAR(50))
    pais = db.Column(db.VARCHAR(40))

    def __init__(self, rua, bairro, cidade, estado, pais, numero, complemento, tipo_endereco, cep):

        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
        self.numero = numero
        self.complemento = complemento
        self.tipo_endereco = tipo_endereco # Valores possíveis -> R - Residencial ; C - Comercial
        self.cep = cep

################################ FIM Modelo Endereço ##################################################
