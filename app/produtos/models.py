from app import db
from sqlalchemy import func
from flask import session

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

            return 'A inserção do produto não será possível pois já há um produto registrado com o mesmo nome.'

        for insumo in dados_produto['insumos']:

            if insumo['nome'] == Insumos.query.filter_by(nome=insumo['nome']).first().nome:

                    relacao = Receitas(
                        Produtos.query.filter_by(nome=dados_produto['nome']).first().id_produto,
                        Insumos.query.filter_by(nome=insumo['nome']).first().id,
                        insumo['quantidade']
                    )

            else:

                return 'A inserção do produto não será possível pois há insumos não cadastrados. Por favor, realize o cadastro e tente novamente.'

            lista_relacoes_produto_insumos.append(relacao)

        for relacao in lista_relacoes_produto_insumos:

            db.session.add(relacao)
            db.session.commit()

        return 'A inserção do produto foi bem sucedida.'

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





############################### Fim Modelo Cardápio #####################################################

################################ Modelo Cadastro Pedidos ########################################################


class Insumos(db.Model):
    __tablename__ = 'insumos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    quantidade_estoque_insumo = db.Column(db.Integer, nullable=False)

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




############################### Fim Modelo Cardápio #####################################################
