from app import db

receita = db.Table(
    "receitas",
    db.Column('id_produto', db.Integer, db.ForeignKey('cardapio.id_produto'), primary_key=True),
    db.Column('id_insumo', db.Integer, db.ForeignKey('insumos.id'))
)

################################ Modelo Cadastro Produtos ########################################################

class Produtos(db.Model):
    __tablename__ = 'cardapio'

    id_produto = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(40))
    quantidade_estoque_produto = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float)
    descricao = db.Column(db.VARCHAR(40))
    imagem = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    receita = db.relationship('Insumos', backref='produto', secondary=receita, lazy='select', uselist=True)

    def __init__(self, nome, quantidade_estoque_produto, valor, descricao, imagem, mimetye):
        self.nome = nome
        self.quantidade_estoque_produto = quantidade_estoque_produto
        self.valor = valor
        self.descricao = descricao
        self.imagem = imagem
        self.mimetype = mimetye

    @staticmethod
    def adiciona_produto_cardapio(dados_produto):

        produto = Produtos(
            dados_produto['nome'],
            dados_produto['quantidade_estoque_produto'],
            dados_produto['valor'],
            dados_produto['descricao'],
            dados_produto['imagem'],
            dados_produto['mimetype']
        )

        for insumo in dados_produto['insumos']:
            if insumo == Insumos.query.filter_by(nome=insumo).first().nome:

                relacao = Insumos.query.filter_by(nome=insumo).first()
                produto.receita.append(relacao)

            else:
                return 'A inserção do produto não será possível pois há insumos não cadastrados. Por favor, realize o cadastro e tente novamente.'

            db.session.add(produto)
            db.session.commit()


    # @staticmethod
    # def adiciona_produto_estoque(produto, quantidade):
    #     estoque = Produtos.query.filter_by(nome=produto).first()
    #     estoque.quantidade_estoque_produto += quantidade
    #
    #
    #
    #     db.session.commit()

    @staticmethod
    def reduz_produto_estoque(produto, quantidade):
        estoque = Produtos.query.filter_by(nome=produto).first()
        estoque.quantidade_estoque_produto -= quantidade
        db.session.commit()




############################### Fim Modelo Cardápio #####################################################

################################ Modelo Cadastro Pedidos ########################################################

class Insumos(db.Model):
    __tablename__ = 'insumos'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    quantidade_estoque_insumo = db.Column(db.Integer, nullable=False)

    # @staticmethod
    # def adiciona_insumo_estoque(insumo):
    #     try:
    #
    #
    #
    # @staticmethod
    # def reduz_insumo_estoque():
    #
    #     for insumo in dados_produto['insumos']:
    #         if insumo == Insumos.query.filter_by(nome=insumo).first().nome:

############################### Fim Modelo Cardápio #####################################################
