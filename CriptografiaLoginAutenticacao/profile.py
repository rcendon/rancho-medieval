from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from flask_login import LoginManager
from __init__ import db

main = Blueprint('main', __name__)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', nome=current_user.nome)