from wtforms import Form, BooleanField, StringField, PasswordField, validators

#self.nome = nome
#self.login = login
#self.rg = rg
#self.cpf = cpf
#self.tipo = tipo
###########self.endereco = endereco
#self.senha = senha

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - The Forms

class RegistrationForm(Form):
    nome = StringField('Nome', [validators.Length(min=4, max=25)])
    login = StringField('Login', [validators.Length(min=2, max=35)])
    rg = StringField('RG', [validators.Length(min=2, max=35)])
    cpf = StringField('CPF', [validators.Length(min=2, max=35)])
    tipo = StringField('Tipo', [validators.Length(min=2, max=35)])    
    
    senha = PasswordField('Senha', [
        validators.DataRequired(),
        validators.EqualTo('Confirmação', message='As senhas não conferem')
    ])

    confirm = PasswordField('Repetir senha')
    #accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

