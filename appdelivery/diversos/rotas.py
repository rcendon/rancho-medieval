from flask import render_template, session, request, redirect, url_for, flash

from appdelivery import app

##################### Rota Área de Entrega ####################################################

@app.route('/entrega')

def entrega(): 
    return render_template('/diversos/entrega.html')