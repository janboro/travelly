from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('main/home.html')


@main.route('/about')
def about():
    return render_template('main/about.html')