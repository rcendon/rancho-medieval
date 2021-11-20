######## USUÁRIOS INTERNOS ########

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

class RegistrationForm(Form):
    nome = StringField('Nome', [validators.Length(min=4, max=25)])
    email = StringField('E-mail', [validators.Length(min=2, max=35)])
    telefone = StringField('Telefone', [validators.Length(min=2, max=35)])
    rg = StringField('RG', [validators.Length(min=2, max=35)])
    cpf = StringField('CPF', [validators.Length(min=2, max=35)])
    endereco = StringField('Endereco', [validators.Length(min=2, max=35)])      
    senha = PasswordField('Senha', [validators.Length(min=2, max=35)]) 
   
    
######################### Classe Form Login ##################################################

class LoginFormulario(Form):    
    cpf = StringField('CPF', [validators.Length(min=2, max=35)])      
    senha = PasswordField('Senha', [validators.Length(min=2, max=35)]) 


######################### Classe Form Produtos ##################################################

#self.nome = nome
#self.quantidade_estoque = quantidade_estoque
#self.valor = valor

class CadastroProdutos(Form):    
    nome = StringField('Nome', [validators.Length(min=1, max=40)])      
    quantidade_estoque = StringField('Quantidade Estoque', [validators.Length(min=1, max=10)]) 
    valor = StringField('Valor', [validators.Length(min=1, max=10)]) 
    descricao = StringField('Descricao', [validators.Length(min=1, max=40)]) 
    imagem = StringField('Imagem', [validators.Length(min=1, max=150)]) 
    mimetype = StringField('mimetype', [validators.Length(min=1, max=150)]) 

    
    
