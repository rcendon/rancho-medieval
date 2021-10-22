##### CLIENTES ########

from wtforms import Form, BooleanField, StringField, PasswordField, validators

#self.nome = nome
#self.email = email
#self.telefone = telefone
#self.rg = rg
#self.cpf = cpf
#self.endereco = endereco
#self.senha = senha

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - The Forms

######################### Classe Form Cadastro ##################################################

class RegistrationFormCli(Form):
    nome = StringField('Nome', [validators.Length(min=4, max=25)])
    email = StringField('E-mail', [validators.Length(min=2, max=35)])
    telefone = StringField('Telefone', [validators.Length(min=2, max=35)])
    rg = StringField('RG', [validators.Length(min=2, max=35)])
    cpf = StringField('CPF', [validators.Length(min=2, max=35)])
    endereco = StringField('Endereco', [validators.Length(min=2, max=35)])      
    senha = PasswordField('Senha', [validators.Length(min=2, max=35)]) 
   
    
######################### Classe Form Login ##################################################

class LoginFormularioCli(Form):    
    email = StringField('E-mail', [validators.Length(min=2, max=35)])      
    senha = PasswordField('Senha', [validators.Length(min=2, max=35)]) 