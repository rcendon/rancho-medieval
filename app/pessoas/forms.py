##### CLIENTES ########

from wtforms import BooleanField, StringField, PasswordField, IntegerField, validators, SelectField
from wtforms.validators import length, DataRequired
from flask_wtf import FlaskForm

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - The Forms


######################### Classe Form Cadastro ##################################################

class FormularioDadosPessoaisPrincipais(FlaskForm):
    nome = StringField('Nome', [validators.Length(min=1, max=25)])
    email = StringField('E-mail', [validators.Length(min=2, max=35)])
    rg = StringField('RG', [validators.Length(min=1, max=35)])
    cpf = StringField('CPF', [validators.Length(min=1, max=35)])
    registro_diverso = StringField('Registro alternativo', validators=[DataRequired(), length(min=1, max=35)])
    pais_do_registro_diverso = StringField('País', validators=[DataRequired(), length(min=1, max=50)])
    senha = PasswordField('Senha', [validators.Length(min=8, max=35)])


######################### Classe Form Endereço ##################################################

class FormularioEndereco(FlaskForm):
    rua = StringField('Rua', validators=[DataRequired(), length(min=1, max=100)])
    bairro = StringField('Bairro', validators=[DataRequired(), length(min=1, max=100)])
    numero = IntegerField('Número', validators=[DataRequired(), length(min=1, max=4)])
    complemento = StringField('Complemento', validators=[length(min=0, max=50)])
    cep = IntegerField('CEP', validators=[DataRequired(), length(min=11, max=11)])
    cidade = StringField('Cidade', validators=[DataRequired(), length(min=1, max=50)])
    estado = SelectField('Estado', validators=[DataRequired()], choices=['Bahia', 'São Paulo'])
    pais = StringField('País', validators=[DataRequired(), length(min=1, max=40)])


######################### Classe Form Login ##################################################

class LoginFormularioCli(FlaskForm):
    email = StringField('E-mail', [validators.Length(min=2, max=35)])
    senha = PasswordField('senha', [validators.Length(min=1, max=35)])