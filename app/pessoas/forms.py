##### CLIENTES ########

from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField, validators

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - The Forms

######################### Classe Form Cadastro ##################################################

class RegistrationFormCli(Form):
    nome = StringField('Nome', [validators.Length(min=1, max=25)])
    email = StringField('E-mail', [validators.Length(min=2, max=35)])
    rg = StringField('RG', [validators.Length(min=1, max=35)])
    cpf = StringField('CPF', [validators.Length(min=1, max=35)])
    senha = PasswordField('Senha', [validators.Length(min=1, max=35)])
   
    
######################### Classe Form Login ##################################################

class LoginFormularioCli(Form):
    cpf = IntegerField('cpf', [validators.Length(min=1, max=35)])
    email = StringField('E-mail', [validators.Length(min=2, max=35)])
    senha = PasswordField('senha', [validators.Length(min=1, max=35)])