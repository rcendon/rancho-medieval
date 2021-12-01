from app import db
from sqlalchemy import func
from flask import session
from ..pessoas.models import Fornecedores, Preco_insumo

# receita = db.Table(
#     "receitas",
#     db.Column('id_produto', db.Integer, db.ForeignKey('cardapio.id_produto'), primary_key=True),
#     db.Column('id_insumo', db.Integer, db.ForeignKey('insumos.id'), primary_key=True)
# )

class Receitas(db.Model):
    __tablename__ = 'receitas'

    id_produto = db.Column(db.BigInteger, db.ForeignKey('cardapio.id_produto'), primary_key=True)
    id_insumo = db.Column(db.BigInteger, db.ForeignKey('insumos.id'), primary_key=True)
    quantidade_insumo = db.Column(db.Integer, nullable=False)
    insumo = db.relationship('Insumos', backref='receita')

    def __init__(self, id_produto, id_insumo, quantidade_insumo):
        self.id_produto = id_produto
        self.id_insumo = id_insumo
        self.quantidade_insumo = quantidade_insumo


################################ Modelo Cadastro Produtos ########################################################

class Produtos(db.Model):
    __tablename__ = 'cardapio'

    id_produto = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(40), unique=True, nullable=False)
    quantidade_estoque_produto = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.VARCHAR(40))
    imagem = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    receita = db.relationship('Receitas', backref='receita')
    # receita = db.relationship('Insumos', backref='produto', secondary=receita, lazy='select', uselist=True)

    def __init__(self, nome, quantidade_estoque_produto, valor, descricao, imagem, mimetype):
        self.nome = nome
        self.quantidade_estoque_produto = quantidade_estoque_produto
        self.valor = valor
        self.descricao = descricao
        self.imagem = imagem
        self.mimetype = mimetype

    @staticmethod
    def adiciona_produto_cardapio_com_receita(dados_produto:dict):

        lista_relacoes_produto_insumos = []

        produto = Produtos.adiciona_produto_cardapio(dados_produto)

        if produto == False:

            # return 'A inserção do produto não será possível pois já há um produto registrado com o mesmo nome.'
            return False

        for insumo in dados_produto['insumos']:

            if insumo['nome'] == Insumos.query.filter_by(nome=insumo['nome']).first().nome:

                    relacao = Receitas(
                        Produtos.query.filter_by(nome=dados_produto['nome']).first().id_produto,
                        Insumos.query.filter_by(nome=insumo['nome']).first().id,
                        insumo['quantidade']
                    )

            else:

                # return 'A inserção do produto não será possível pois há insumos não cadastrados. Por favor, realize o cadastro e tente novamente.'
                return False

            lista_relacoes_produto_insumos.append(relacao)

        for relacao in lista_relacoes_produto_insumos:

            db.session.add(relacao)
            db.session.commit()

        return True
        # return 'A inserção do produto foi bem sucedida.'

    @staticmethod
    def adiciona_produto_cardapio(dados_produto:dict):

        produto = Produtos(
            dados_produto['nome'],
            dados_produto['quantidade_estoque_produto'],
            dados_produto['valor'],
            dados_produto['descricao'],
            dados_produto['imagem'],
            dados_produto['mimetype']
        )

        if Produtos.query.filter_by(nome=dados_produto['nome']).first():

            return False

        else:

            db.session.add(produto)
            db.session.commit()
            return produto

    @staticmethod
    def adiciona_quantidade_produto_estoque(produto, quantidade):

        estoque_produto = Produtos.query.filter_by(nome=produto).first()
        estoque_produto.quantidade_estoque_produto += quantidade
        lista_insumos_utilizados = []
        lista_insumos_validados = []


        for insumo_utilizado in Receitas.query.all():

            if insumo_utilizado.id_produto == estoque_produto.id_produto:

                lista_insumos_utilizados.append(insumo_utilizado)


        for item in range(0, quantidade):

            for insumo in lista_insumos_utilizados:

                estoque_insumo = Insumos.query.filter_by(id=insumo.id_insumo).first()

                if insumo.quantidade_insumo > estoque_insumo.quantidade_estoque_insumo:

                    return False

                else:

                    lista_insumos_validados.append(estoque_insumo)

        for insumo_validado in lista_insumos_validados:

            Insumos.reduz_quantidade_insumo_estoque(
                insumo_validado.nome,
                Receitas.query.filter_by(id_insumo=insumo_validado.id).first().quantidade_insumo
            )

        db.session.add(estoque_produto)
        db.session.commit()
        return True

    @staticmethod
    def reduz_quantidade_produto_estoque(produto, quantidade):
        estoque = Produtos.query.filter_by(nome=produto).first()

        if estoque.quantidade_estoque_produto < quantidade:

            return False

        else:

            estoque.quantidade_estoque_produto -= quantidade
            db.session.add(estoque)
            db.session.commit()
            return True

    @staticmethod
    def altera_descricao_produto(produto, nova_descricao):

        produto_localizado = Produtos.query.filter_by(nome=produto).first()

        if produto_localizado:

            produto_localizado.descricao = nova_descricao

            db.session.add(produto_localizado)
            db.session.commit()
            return True

        else:

            return False

    @staticmethod
    def altera_imagem_produto(produto, nova_imagem):

        produto_localizado = Produtos.query.filter_by(nome=produto).first()

        if produto_localizado:

            produto_localizado.imagem = nova_imagem

            db.session.add(produto_localizado)
            db.session.commit()
            return True

        else:

            return False

    @staticmethod
    def altera_valor_produto(produto, novo_valor):

        produto_localizado = Produtos.query.filter_by(nome=produto).first()

        if produto_localizado:

            produto_localizado.valor = novo_valor

            db.session.add(produto_localizado)
            db.session.commit()
            return True

        else:

            return False



############################### Fim Modelo Cadastro de Produtos #####################################################

################################ Modelo Insumos  ########################################################

class Insumos(db.Model):
    __tablename__ = 'insumos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    quantidade_estoque_insumo = db.Column(db.Integer, nullable=False)
    preco_insumo = db.relationship('Preco_insumo', backref='preco_insumo_insumos', cascade="all, delete", passive_deletes=True)

    def __init__(self, nome, quantidade):
        self.nome = nome
        self.quantidade_estoque_insumo = quantidade

    @staticmethod
    def cadastra_insumo_estoque(insumo):

        if Insumos.query.filter_by(nome=insumo).first():

            return False

        insumo = Insumos(insumo, 0)

        db.session.add(insumo)
        db.session.commit()
        return True

    @staticmethod
    def adiciona_quantidade_insumo_estoque(insumo, quantidade):

        estoque = Insumos.query.filter_by(nome=insumo).first()
        estoque.quantidade_estoque_insumo += quantidade
        db.session.add(estoque)
        db.session.commit()
        return True

    @staticmethod
    def reduz_quantidade_insumo_estoque(insumo, quantidade):

        estoque = Insumos.query.filter_by(nome=insumo).first()

        if estoque.quantidade_estoque_insumo < quantidade:

            return False

        else:

            estoque.quantidade_estoque_insumo -= quantidade
            db.session.add(estoque)
            db.session.commit()
            return True

    @staticmethod
    def associa_fornecedor_a_insumo(fornecedor, dados_insumo:dict):

        fornecedor_instancia = Fornecedores.query.filter_by(nome=fornecedor).first()

        insumo_instancia = Insumos.query.filter_by(nome=dados_insumo['nome']).first()

        if not fornecedor_instancia:

            return False

        if not insumo_instancia:

            return False

        relacao = Preco_insumo(
            insumo_instancia.id,
            fornecedor_instancia.id,
            dados_insumo['valor']
        )

        relacao.insumo = insumo_instancia
        fornecedor_instancia.preco_insumo.append(relacao)
        db.session.add(fornecedor_instancia)
        db.session.commit()
        return True

    @staticmethod
    def desassocia_fornecedor_a_insumo(fornecedor, insumo):

        if (
            Fornecedores.query.filter_by(nome=fornecedor).first() == None
            or
            Insumos.query.filter_by(nome=insumo).first() == None
        ):

            return False

        for preco_insumo in Preco_insumo.query.all():

            if (
                    preco_insumo.id_insumo == Insumos.query.filter_by(nome=insumo).first().id
                    and
                    preco_insumo.id_fornecedor == Fornecedores.query.filter_by(nome=fornecedor).first().id
            ):

                db.session.delete(preco_insumo)
                db.session.commit()

        return True

    @staticmethod
    def altera_valor_insumo_por_fornecedor(fornecedor, dados_insumo:dict):

        insumo_localizado = Insumos.query.filter_by(nome=dados_insumo['nome']).first()

        fornecedor_localizado = Fornecedores.query.filter_by(nome=fornecedor).first()

        if(
                insumo_localizado != None
                and
                fornecedor_localizado != None
        ):

            for preco_insumo in Preco_insumo.query.all():

                if(
                        preco_insumo.id_insumo == insumo_localizado.id
                        and
                        preco_insumo.id_fornecedor == fornecedor_localizado.id
                ):

                    preco_insumo.valor = dados_insumo['valor']
                    db.session.add(preco_insumo)
                    db.session.commit()
                    return True
        else:

            return False

    @staticmethod
    def descadastra_insumo(insumo):

        insumo_instancia = Insumos.query.filter_by(nome=insumo).first()

        if insumo_instancia == None:

            return False

        else:

            for preco_insumo in Preco_insumo.query.all():
                if preco_insumo.id_insumo == insumo_instancia.id:
                    insumo_instancia.preco_insumo.append(preco_insumo)

            db.session.delete(insumo_instancia)
            db.session.commit()
            return True

############################### Fim Modelo Insumos #####################################################
