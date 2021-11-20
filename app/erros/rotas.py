from flask import render_template
from app import app

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('erros/404.html')