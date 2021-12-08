from flask import render_template, session, request, redirect, url_for, flash
from flask.wrappers import Response
from werkzeug.utils import secure_filename

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from app import app, db, bcrypt

from ..produtos.models import Produtos, Insumos
from ..pessoas.models import Pessoas, Fornecedores

from .forms import FormularioDadosPessoaisColaborador, LoginFormularioCli
from ..pessoas.forms import FormularioDadosFornecedor
from ..produtos.forms import CadastroProdutos, CadastroInsumos, AdicionaProdutoEstoque, AdicionaInsumoEstoque

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
        lista_produtos_com_pouco_estoque=Produtos.lista_produtos_em_estoque(10),
        lista_insumos_sem_estoque=Insumos.lista_insumos_sem_estoque(),
        lista_insumos_com_pouco_estoque=Insumos.lista_insumos_em_estoque(10)
    )

####################################################################################

################## Rota Registrar ##################################################   

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - In the View

#RegistrationForm

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

##################################################################################################


################## Rota Login Formulario ########################################################

#LoginFormulario

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

###############################################################################################

##################### Rota Logout ####################################################

@app.route("/logout_colaborador")
def logout():
    session.pop('email_colaborador')
    return redirect(url_for('login_colaborador'))

##################### Rota Exibir Imagem ####################################################

# @app.route("/<int:id>")
# def get_img(id):
#     img = Produtos.query.filter_by(id=id).first()
#
#     if request.method == "POST":
#         ### iMG ##########################################
#         pic = request.files['pic']
#         filename = secure_filename(pic.filename)
#         mimetype = pic.mimetype
#
#     return Response(img.imagem, mimetype=img.mimetype)

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





@app.route("/cadastro_produto", methods=['GET', 'POST'])
def cadastro_produto():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
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

