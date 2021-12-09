from flask import render_template, session, request, redirect, url_for, flash
from flask.wrappers import Response
from werkzeug.utils import secure_filename

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from app import app, db, bcrypt

from ..produtos.models import Produtos, Insumos, Receitas
from ..pessoas.models import Pessoas, Fornecedores, Preco_insumo
from ..pedidos.models import Pedidos

from .forms import FormularioDadosPessoaisColaborador, LoginFormularioCli, FormularioRemocaoFornecedores
from ..pessoas.forms import FormularioDadosFornecedor
from ..produtos.forms import CadastroProdutos, CadastroInsumos, AdicionaProdutoEstoque, AdicionaInsumoEstoque
from .forms import FormularioBuscaProdutos, FormularioEdicaoProdutos, FormularioRemocaoColaboradores, FormularioAssociaInsumoFornecedor, FormularioDesassociaInsumoFornecedor

##################### Rota Home ####################################################

#Rota Home
@app.route('/')

def home(): 
    return render_template('index.html')

######################################################################################

##################### Rota Usuario ####################################################

#Rota Usuario
@app.route('/colaborador')
def colaborador():

    if 'email_colaborador' not in session: ###Controle de Acesso###
        flash(f'Olá, faça o login primeiro', 'danger')    
        return redirect(url_for('login_colaborador'))

    colaborador_instancia = Pessoas.query.filter_by(email=session['email_colaborador']).first()

    return render_template(
        'admin/area_colaborador.html',
        colaborador_instancia=colaborador_instancia,
        lista_produtos_sem_estoque=Produtos.lista_produtos_sem_estoque(),
        lista_produtos_com_pouco_estoque=[produto for produto in Produtos.query.all() if produto.quantidade_estoque_produto < 10 and produto.quantidade_estoque_produto > 0],
        lista_insumos_sem_estoque=Insumos.lista_insumos_sem_estoque(),
        lista_insumos_com_pouco_estoque=Insumos.lista_insumos_em_estoque(10)
    )

####################################################################################

@app.route('/login_colaborador', methods=['GET', 'POST'])
def login_colaborador():
    if 'email_colaborador' in session: ###Controle de Acesso###
        return redirect(url_for('colaborador'))

    form = LoginFormularioCli() #Retorna valores do forms.py

    if request.method == "POST" and form.validate_on_submit():

        user = Pessoas.query.filter_by(email=form.email.data).first()

        if (user and bcrypt.check_password_hash(user.senha, form.senha.data)) and user.tipo != 'C':

            session['email_colaborador'] = form.email.data
            flash(f'Bem Vindo {user.nome}', 'success')
            return redirect(request.args.get('next') or url_for('colaborador'))

        else:

            flash(f'E-mail ou Senha incorretos', 'danger')

    return render_template('admin/login_colaborador.html', form=form)

##################### Rota Logout ####################################################

@app.route("/logout_colaborador")
def logout():
    session.pop('email_colaborador')
    return redirect(url_for('login_colaborador'))

###############################################################################################

@app.route('/registrar_colaborador', methods=['GET', 'POST'])
def registrar_colaborador():
    if 'email_colaborador' not in session: ###Controle de Acesso###
        flash(f'Olá, faça o login primeiro', 'danger')
        return redirect(url_for('login'))

    form = FormularioDadosPessoaisColaborador() #Retorna valores do forms.py

    if request.method == "POST" and form.validate_on_submit():

        if form.tipo.data == 'Funcionário':

            form.tipo.data = 'F'

        elif form.tipo.data == 'Administrador':

            form.tipo.data = 'A'

        else:

            flash(f'O registro de não foi realizado, por favor verifique os dados inseridos.', 'danger')
            return redirect(url_for('registrar_colaborador'))

        Pessoas.adiciona_pessoa(form, form.tipo.data)
        flash(f'O registro de {form.nome.data} foi realizado com sucesso.', 'success')
        return redirect(url_for('colaborador'))

    return render_template('admin/registra_colaborador.html', form=form)

@app.route('/remove_colaborador', methods=['GET', 'POST'])
def remove_colaborador():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    if Pessoas.query.filter_by(email=session['email_colaborador']).first().tipo != 'A':
        flash(f'Olá, apenas administradores podem acessar essa página.', 'info')
        return redirect(url_for('login_colaborador'))

    form = FormularioRemocaoColaboradores()

    if request.method == "POST" and form.validate_on_submit():

        colaborador_instancia = Pessoas.query.filter_by(nome=form.colaborador.data).first()
        operacao = colaborador_instancia.remove_pessoa()

        if operacao:

            flash(f'Coladorador removido com sucesso ', 'success')
            return redirect(url_for('colaborador'))

        else:

            flash("Ocorreu um problema com a operação.", "danger")

    return render_template("/admin/remove_colaborador.html", form=form)

@app.route("/registra_fornecedor", methods=['GET', 'POST'])
def registra_fornecedor():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    form = FormularioDadosFornecedor()

    if request.method == "POST" and form.validate_on_submit():

        dados = {
            'nome': form.nome.data,
            'cnpj': form.cnpj.data,
            'contato': form.contato.data,
            'email': form.email.data,
            'rua': form.rua.data,
            'bairro': form.bairro.data,
            'cidade': form.cidade.data,
            'estado': form.estado.data,
            'pais': form.pais.data,
            'numero': form.numero.data,
            'complemento': form.complemento.data,
            'tipo_endereco': 'C',
            'cep': form.cep.data

        }

        operacao = Fornecedores.adiciona_fornecedor(dados)

        if operacao:

            flash(f'Fornecedor cadastrado com sucesso ', 'success')
            return redirect(url_for('colaborador'))

        else:

            flash("Ocorreu um problema com o cadastro. Por favor, certifique-se que os dados foram inseridos corretamente.", "danger")

    return render_template("/admin/registra_fornecedor.html", form=form)

@app.route("/remove_fornecedor", methods=['GET', 'POST'])
def remove_fornecedor():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    if Pessoas.query.filter_by(email=session['email_colaborador']).first().tipo != 'A':
        flash(f'Olá, apenas administradores podem acessar essa página.', 'info')
        return redirect(url_for('login_colaborador'))

    form = FormularioRemocaoFornecedores()

    if request.method == "POST" and form.validate_on_submit():

        for fornecedor in form.fornecedores.data:

            fornecedor_instancia = Fornecedores.query.filter_by(nome=fornecedor).first()
            operacao = fornecedor_instancia.remove_fornecedor()

        if operacao:

            flash(f'Fornecedor(es) removido(s) com sucesso ', 'success')
            return redirect(url_for('colaborador'))

        else:

            flash("Ocorreu um problema com a operação.", "danger")

    return render_template("/admin/remove_fornecedor.html", form=form, quantidade_fornecedores=str(len(Fornecedores.query.all())))

@app.route("/cadastro_produto", methods=['GET', 'POST'])
def cadastro_produto():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    if Pessoas.query.filter_by(email=session['email_colaborador']).first().tipo != 'A':
        flash(f'Olá, apenas administradores podem acessar essa página.', 'info')
        return redirect(url_for('login_colaborador'))

    form = CadastroProdutos()

    if request.method == "POST" and form.validate_on_submit():

        dados = {
            'nome': form.nome.data,
            'quantidade_estoque_produto': form.quantidade_estoque_produto.data,
            'valor': form.valor.data,
            'descricao': form.descricao.data,
            'imagem': 'teste', # form.imagem.data,
            'insumos_utilizados': form.insumos_utilizados.data
        }

        operacao = Produtos.adiciona_produto_cardapio_com_receita(dados)

        if operacao:

            flash(f'Produto cadastrado com sucesso ', 'success')
            return redirect(url_for('colaborador'))

        else:

            flash("Ocorreu um problema com o cadastro. Por favor, certifique-se que os dados foram inseridos corretamente.", "danger")

    return render_template("/admin/cadastro_produto.html", form=form, insumos_quantidade=str(len(Insumos.lista_insumos())))

@app.route("/busca_receita", methods=["GET", "POST"])
def busca_receita():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    if Pessoas.query.filter_by(email=session['email_colaborador']).first().tipo != 'A':

        flash(f'Olá, apenas administradores podem acessar essa página.', 'info')
        return redirect(url_for('login_colaborador'))

    form_busca_produtos = FormularioBuscaProdutos()

    if request.method == "POST" and form_busca_produtos.validate_on_submit():

        return redirect(url_for('modifica_quantidade_insumo_receita', nome_produto=form_busca_produtos.produto.data))

    return render_template("/admin/busca_receita.html", form_busca_produtos=form_busca_produtos, produtos_quantidade=str(len(Produtos.query.all())))

@app.route('/modifica_quantidade_insumo_receita/<nome_produto>', methods=['GET', 'POST'])
def modifica_quantidade_insumo_receita(nome_produto):

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    if Pessoas.query.filter_by(email=session['email_colaborador']).first().tipo != 'A':

        flash(f'Olá, apenas administradores podem acessar essa página.', 'info')
        return redirect(url_for('login_colaborador'))

    form_edicao_produtos = FormularioEdicaoProdutos(Produtos.query.filter_by(nome=nome_produto).first().id_produto)

    if request.method == "POST" and form_edicao_produtos.validate_on_submit():

        insumo = Insumos.query.filter_by(nome=form_edicao_produtos.insumo.data).first()
        quantidade = form_edicao_produtos.quantidade.data

        ingrediente_receita = Receitas.query.filter_by(id_insumo=insumo.id).first()

        ingrediente_receita.quantidade_insumo = quantidade

        db.session.add(ingrediente_receita)
        db.session.commit()

        flash("Alteração realizada com sucesso", "success")
        return redirect(url_for('login_colaborador'))

    return render_template('/admin/define_quantidade_insumo_receita.html', form_edicao_produtos=form_edicao_produtos)

@app.route("/adiciona_produto_estoque", methods=['GET', 'POST'])
def adiciona_produto_estoque():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    form = AdicionaProdutoEstoque()

    if request.method == "POST" and form.validate_on_submit():

        produto_instancia = Produtos.query.filter_by(nome=form.produto_nome.data).first()

        operacao = produto_instancia.adiciona_quantidade_produto_estoque(form.quantidade.data)

        if operacao and form.quantidade.data == 1:

            flash(f'Obrigado, foi adicionada {form.quantidade.data} unidade do produto {form.produto_nome.data} ao estoque.', 'success')
            return redirect(url_for('colaborador'))

        if operacao and form.quantidade.data > 1:

            flash(f'Obrigado, foram adicionadas {form.quantidade.data} unidades do produto {form.produto_nome.data} ao estoque.', 'success')
            return redirect(url_for('colaborador'))

        else:

            flash("Ocorreu um problema com a operação. Por favor, certifique-se que os dados foram inseridos corretamente e de que há insumos o suficiente no estoque.", "danger")

    return render_template("/admin/adiciona_produto_estoque.html", form=form)

@app.route("/cadastro_insumo", methods=['GET', 'POST'])
def cadastro_insumo():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    if Pessoas.query.filter_by(email=session['email_colaborador']).first().tipo != 'A':

        flash(f'Olá, apenas administradores podem acessar essa página.', 'info')
        return redirect(url_for('login_colaborador'))

    form = CadastroInsumos()

    if request.method == "POST" and form.validate_on_submit():

        dados = {
            'nome': form.nome.data,
            'quantidade_estoque_insumo': form.quantidade_estoque_insumo.data
        }

        operacao = Insumos.cadastra_insumo_estoque(dados)

        if operacao:

            flash(f'Insumo cadastrado com sucesso ', 'success')
            return redirect(url_for('colaborador'))

        else:

            flash("Ocorreu um problema com o cadastro. Por favor, certifique-se que os dados foram inseridos corretamente.", "danger")

    return render_template("/admin/cadastro_insumo.html", form=form)

@app.route("/adiciona_insumo_estoque", methods=['GET', 'POST'])
def adiciona_insumo_estoque():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    form = AdicionaInsumoEstoque()

    if request.method == "POST" and form.validate_on_submit():

        insumo_instancia = Insumos.query.filter_by(nome=form.insumo_nome.data).first()

        operacao = insumo_instancia.adiciona_quantidade_insumo_estoque(form.quantidade.data)

        if operacao and form.quantidade.data == 1:

            flash(f'Obrigado, foi adicionada {form.quantidade.data} unidade do insumo {form.insumo_nome.data} ao estoque.', 'success')
            return redirect(url_for('colaborador'))

        if operacao and form.quantidade.data > 1:

            flash(f'Obrigado, foram adicionadas {form.quantidade.data} unidades do produto {form.insumo_nome.data} ao estoque.', 'success')
            return redirect(url_for('colaborador'))

        else:

            flash("Ocorreu um problema com a operação. Por favor, certifique-se que os dados foram inseridos corretamente e de que há insumos o suficiente no estoque.", "danger")

    return render_template("/admin/adiciona_insumo_estoque.html", form=form)

@app.route("/associa_insumo_a_fornecedor", methods=['GET', 'POST'])
def associa_insumo_a_fornecedor():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    if Pessoas.query.filter_by(email=session['email_colaborador']).first().tipo != 'A':

        flash(f'Olá, apenas administradores podem acessar essa página.', 'info')
        return redirect(url_for('login_colaborador'))

    form = FormularioAssociaInsumoFornecedor()

    if request.method == 'POST' and form.validate_on_submit():

        dados_insumo = {'nome': form.insumo.data, 'valor': form.valor.data}

        Insumos.associa_fornecedor_a_insumo(dados_insumo, form.fornecedor.data)

        flash("Associação feita com sucesso.", "success")
        return redirect(url_for('colaborador'))

    return render_template("/admin/associa_insumo_fornecedor.html", form=form)

@app.route("/desassocia_insumo_a_fornecedor", methods=['GET', 'POST'])
def desassocia_insumo_a_fornecedor():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    if Pessoas.query.filter_by(email=session['email_colaborador']).first().tipo != 'A':

        flash(f'Olá, apenas administradores podem acessar essa página.', 'info')
        return redirect(url_for('login_colaborador'))

    form = FormularioDesassociaInsumoFornecedor()

    if request.method == 'POST' and form.validate_on_submit():

        resultado = Insumos.desassocia_fornecedor_a_insumo(form.insumo.data, form.fornecedor.data)

        if resultado:

            flash("Desassociação feita com sucesso.", "success")
            return redirect(url_for('colaborador'))

        else:

            flash("Ocorreu um erro com a desassociação. Por favor, certifique-se que o fornecedor indicado está associado ao insumo selecionado.", "danger")
            return redirect(url_for('colaborador'))

    return render_template("/admin/desassocia_insumo_fornecedor.html", form=form)

@app.route("/historico_vendas")
def historico_vendas():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    if Pessoas.query.filter_by(email=session['email_colaborador']).first().tipo != 'A':

        flash(f'Olá, apenas administradores podem acessar essa página.', 'info')
        return redirect(url_for('login_colaborador'))

    return render_template('/admin/historico_de_vendas.html', lista_pedidos=Pedidos.query.all())

@app.route('/pedidos_em_aberto')
def pedidos_em_aberto():

    return render_template('/admin/pedidos_em_aberto.html', lista_pedidos=Pedidos.query.filter_by(status='Em preparação' or 'Preparado' or 'A caminho').all())

@app.route('/lista_insumos')
def lista_insumos():

    lista_insumos_por_fornecedor = Insumos.lista_fornecedores_por_insumo()

    return render_template('/admin/lista_insumos_por_fornecedor.html', lista_insumos_por_fornecedor=lista_insumos_por_fornecedor)








