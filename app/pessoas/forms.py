##### CLIENTES ########

from wtforms.fields import StringField, PasswordField, IntegerField, SelectField, SubmitField
from wtforms.validators import length, InputRequired, NumberRange, ValidationError
from flask_wtf import FlaskForm
from app.pessoas.models import Pessoas

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - The Forms


######################### Classe Form Cadastro ##################################################

class FormularioDadosPessoais(FlaskForm):
    nome = StringField(
        'Nome', validators=[
            InputRequired(message="Por favor, preencha este campo antes de prosseguir."),
            length(min=1, max=50, message="Por favor, reduza a quantidade de dígitos no campo antes de prosseguir. ")
        ]
    )
    email = StringField('E-mail', validators=[InputRequired(), length(min=2, max=35)])
    rg = IntegerField('RG', validators=[NumberRange(min=1000000000, max=9999999999)])
    cpf = IntegerField('CPF', validators=[NumberRange(min=10000000000, max=99999999999)])
    senha = PasswordField('Senha', validators=[InputRequired(), length(min=1, max=35)])
    rua = StringField('Rua', validators=[InputRequired(), length(min=1, max=100)])
    bairro = StringField('Bairro', validators=[InputRequired(), length(min=1, max=100)])
    numero = IntegerField('Número', validators=[InputRequired(), NumberRange(min=1, max=9999)])
    complemento = StringField('Complemento', validators=[length(min=0, max=50)])
    cep = IntegerField('CEP', validators=[InputRequired(), NumberRange(min=10000000, max=99999999)])
    cidade = StringField('Cidade', validators=[InputRequired(), length(min=1, max=50)])
    estado = SelectField('Estado', validators=[InputRequired()], choices=['-', 'Bahia', 'São Paulo'])
    pais = StringField('País', validators=[InputRequired(), length(min=1, max=40)])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        pessoa_instancia = Pessoas.query.filter_by(email=email.data).first()
        if pessoa_instancia:
            raise ValidationError("Já existe usuário com esse e-mail, por favor indique outro.")

    def validate_cpf(self, cpf):
        pessoa_instancia = Pessoas.query.filter_by(cpf=cpf.data).first()
        if pessoa_instancia:
            raise ValidationError("Já existe usuário com esse CPF, por favor indique outro.")

    def validate_rg(self, rg):
        pessoa_instancia = Pessoas.query.filter_by(rg=rg.data).first()
        if pessoa_instancia:
            raise ValidationError("Já existe usuário com esse RG, por favor indique outro.")

    def validate_estado(self, estado):
        if estado.data == '-':
            raise ValidationError("Por favor, escolha alguma das opções na lista.")

######################### Classe Form Login ##################################################

class LoginFormularioCli(FlaskForm):
    email = StringField('E-mail', validators=[length(min=2, max=35)])
    senha = PasswordField('Senha', validators=[length(min=1, max=35)])
    submit = SubmitField("Login")

    def validate_senha(self, senha):
        if len(senha.data) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 dígitos.")
