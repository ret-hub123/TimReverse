from flask import Blueprint, render_template, request, url_for
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import redirect

from ..build import db
from ..forms import RequestForm
from ..models import Client, Request

requests = Blueprint('requests', __name__)

@requests.route('/request_form', methods=['GET', 'POST'])
def request_form():
    csrf_token = generate_csrf()
    form = RequestForm()
    if form.validate_on_submit():
        try:
            client = Client.query.filter_by(email=form.email.data).first()

            if not client:
                client = Client(first_name=form.first_name.data, second_name=form.second_name.data,
                                email=form.email.data, phone=form.phone.data)
                db.session.add(client)
                db.session.commit()

            new_request = Request(client_id = client.id, title=form.title.data, description = form.description.data)

            db.session.add(new_request)
            db.session.commit()

            return redirect(url_for('main.main_page'))

        except Exception as e:
            db.session.rollback()
            print(f"Ошибка БД: {e}")

    return render_template('main/request_form.html', form=form)