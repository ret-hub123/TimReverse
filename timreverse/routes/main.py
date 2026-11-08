from flask import Blueprint
from flask import render_template

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/main')
def main_page():
    return render_template("main/main.html")