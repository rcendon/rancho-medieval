from flask import render_template, session, request, redirect, url_for, flash
from flask.wrappers import Response
from werkzeug.utils import secure_filename

#Importa a variaveis APP e DB do "__init__.py" = (loja).
from app import app, db, bcrypt

from ..produtos.models import Produtos, Insumos
from ..pessoas.models import Pessoas

from .forms import FormularioDadosPessoaisColaborador, LoginFormularioCli
from ..produtos.forms import CadastroProdutos, CadastroInsumos

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

    return render_template('admin/area_colaborador.html', colaborador_instancia=colaborador_instancia)

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

    return render_template('admin/registrar_colaborador.html', form=form)

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

##################### Rota Adicionar Produto ####################################################

@app.route('/manipulacao_cardapio', methods=['GET', 'POST'])
def manipulacao_cardapio():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    return render_template('admin/manipulacao_cardapio.html', lista_produtos_sem_estoque=Produtos.lista_produtos_sem_estoque()) #ELSE mostra pagina ADD

@app.route('/manipulacao_insumos', methods=['GET', 'POST'])
def manipulacao_insumos():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    return render_template('admin/manipulacao_insumos.html', lista_insumos_sem_estoque=Insumos.lista_insumos_sem_estoque())

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

@app.route("/cadastro_produto", methods=['GET', 'POST'])
def cadastro_produto():

    if 'email_colaborador' not in session:
        flash(f'Olá, faça o login primeiro', 'info')
        return redirect(url_for('login_colaborador'))

    form = CadastroProdutos()

    if request.method == "POST" and form.validate_on_submit():

        operacao = Produtos.adiciona_produto_cardapio_com_receita(form)

        if operacao:

            flash(f'Produto cadastrado com sucesso ', 'success')
            return redirect(url_for('colaborador'))  # Se o metodo POST for OK retornar para o INDEX

        else:

            flash("Ocorreu um problema com o cadastro. Por favor, certifique-se que os dados foram inseridos corretamente.", "danger")

    return redirect(url_for('cadastro_produto'))
