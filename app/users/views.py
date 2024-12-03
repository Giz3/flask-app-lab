from flask import Blueprint, render_template

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/hi/<name>')
def greetings(name):
    return render_template('hi.html', name=name)

@users_bp.route('/admin')
def admin():
    return "ADMINISTRATOR"