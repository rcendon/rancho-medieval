from wtforms import Form, StringField, validators

#https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/ - The Forms

######################### Classe Form Login ##################################################

#self.nome = nome
#self.quantidade_estoque = quantidade_estoque
#self.valor = valor

class CadastroProdutos(Form):    
    nome = StringField('Nome', [validators.Length(min=2, max=35)])      
    quantidade_estoque = StringField('Quantidade Estoque', [validators.Length(min=1, max=10)]) 
    valor = StringField('Valor', [validators.Length(min=1, max=35)]) 
    #Upload Imagem