from app import db
from sqlalchemy import func
from flask import session
from ..pessoas.models import Fornecedores, Preco_insumo


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
    descricao = db.Column(db.VARCHAR(100))
    imagem = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    receita = db.relationship('Receitas', backref='receita')


    def __init__(self, nome, quantidade_estoque_produto, valor, descricao, imagem=None, mimetype=None):
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

        for insumo in dados_produto['insumos_utilizados']:

            if insumo == Insumos.query.filter_by(nome=insumo).first().nome:

                relacao = Receitas(
                    Produtos.query.filter_by(nome=dados_produto['nome']).first().id_produto,
                    Insumos.query.filter_by(nome=insumo).first().id,
                    1
                )

            else:

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
            'A'
        )

        if Produtos.query.filter_by(nome=dados_produto['nome']).first():

            return False

        else:

            db.session.add(produto)
            # db.session.commit()
            return produto

    def adiciona_quantidade_produto_estoque(self, quantidade):

        self.quantidade_estoque_produto += quantidade
        lista_insumos_utilizados = []
        lista_insumos_validados = []

        for insumo_utilizado in Receitas.query.all():

            if insumo_utilizado.id_produto == self.id_produto:

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

        db.session.add(self)
        db.session.commit()
        return True

    def reduz_quantidade_produto_estoque(self, quantidade):

        if self.quantidade_estoque_produto < quantidade:

            return False

        else:

            self.quantidade_estoque_produto -= quantidade
            db.session.add(self)
            db.session.commit()
            return True

    def altera_descricao_produto(self, nova_descricao):

        self.descricao = nova_descricao

        db.session.add(self)
        db.session.commit()
        return True

    def altera_imagem_produto(self, nova_imagem):

        self.imagem = nova_imagem

        db.session.add(self)
        db.session.commit()
        return True

    def altera_valor_produto(self, novo_valor):

        self.valor = novo_valor

        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def lista_produtos_em_estoque(quantidade_maxima_para_exibicao):

        lista_produtos_com_estoque = []

        lista_produtos = Produtos.query.all()

        if lista_produtos == None:

            return False

        else:

            for produto in lista_produtos:

                if produto.quantidade_estoque_produto > 0 and produto.quantidade_estoque_produto < quantidade_maxima_para_exibicao:

                    lista_produtos_com_estoque.append(produto)

        return lista_produtos_com_estoque

    @staticmethod
    def lista_produtos_sem_estoque():

        lista_produtos_sem_estoque = []

        lista_produtos = Produtos.query.all()

        if lista_produtos == None:

            return False

        else:

            for produto in lista_produtos:

                if Produtos.quantidade_em_estoque_do_produto(produto.nome) == 0:

                    lista_produtos_sem_estoque.append(produto)

        return lista_produtos_sem_estoque

    @staticmethod
    def quantidade_em_estoque_do_produto(produto):

        produto_instancia = Produtos.query.filter_by(nome=produto).first()

        if produto_instancia == None:

            return False

        else:

            return produto_instancia.quantidade_estoque_produto

############################### Fim Modelo Cadastro de Produtos #####################################################

################################ Modelo Insumos  ########################################################

class Insumos(db.Model):
    __tablename__ = 'insumos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50), unique=True, nullable=False)
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
    def associa_fornecedor_a_insumo(dados_insumo:dict, fornecedor):

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
    def desassocia_fornecedor_a_insumo(insumo, fornecedor):

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
    def altera_valor_insumo_por_fornecedor(dados_insumo:dict, fornecedor):

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

    @staticmethod
    def lista_fornecedores_por_insumo(insumo, fornecedor=None):

        lista_fornecedores = [insumo]
        insumo_instancia = Insumos.query.filter_by(nome=insumo).first()

        if fornecedor == None:

            fornecedores = Fornecedores.query.all()

        else:

            fornecedores = Fornecedores.query.filter_by(nome=fornecedor).all()

        if fornecedores == None or insumo_instancia == None:

            return False

        precos_insumo = Preco_insumo.query.filter_by(id_insumo=insumo_instancia.id).all()

        if precos_insumo == None:

            return False

        else:

            for preco_insumo in precos_insumo:

                for fornecedor in fornecedores:

                    if preco_insumo.id_fornecedor == fornecedor.id:
                        lista_fornecedores.append(fornecedor)

            return lista_fornecedores

    @staticmethod
    def lista_insumos():

        lista_insumos = []

        for insumo in Insumos.query.all():

            lista_insumos.append(insumo.nome)

        return sorted(lista_insumos)

    @staticmethod
    def lista_insumos_sem_estoque():

        lista_insumos_sem_estoque = []

        lista_insumos = Insumos.query.all()

        if lista_insumos == None:

            return False

        else:

            for insumo in lista_insumos:

                if insumo.quantidade_estoque_insumo == 0:

                    lista_insumos_sem_estoque.append(insumo)

        return lista_insumos_sem_estoque

    @staticmethod
    def lista_insumos_em_estoque(quantidade_maxima_para_exibicao=0):

        lista_insumos_com_estoque = []

        lista_insumos = Insumos.query.all()

        if lista_insumos == None:

            return False

        else:

            for insumo in lista_insumos:

                if insumo.quantidade_estoque_insumo > 0 and insumo.quantidade_estoque_insumo < quantidade_maxima_para_exibicao:
                    lista_insumos_com_estoque.append(insumo)

        return lista_insumos_com_estoque

############################### Fim Modelo Insumos #####################################################
