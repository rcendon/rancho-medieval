from appdelivery import db

#self.nome = nome
#self.login = login
#self.rg = rg
#self.cpf = cpf
#self.tipo = tipo
###########self.endereco = endereco
#self.senha = senha

#https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

class User(db.Model):
    __tablename__ = 'pessoas' 
        
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.VARCHAR(50))
    login = db.Column(db.VARCHAR(10))  
    rg = db.Column(db.String(10))
    cpf = db.Column(db.String(12))
    tipo = db.Column(db.CHAR(1))
    #endereco = db.Column(db.Integer)
    senha = db.Column(db.VARCHAR(64))

    def __repr__(self):
        return '<User %r>' % self.username