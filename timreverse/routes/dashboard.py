from flask import request, flash

from flask import Blueprint, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from .. import db
from ..models import Client, Request
from sqlalchemy import or_


dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
def view_requests():
    if current_user:
        all_requests = Request.query.order_by(Request.id.desc()).all()

        requests_active = Request.query.filter(or_(Request.status == 'Новая',Request.status == 'В работе')).order_by(Request.id.desc()).all()
        requests_archive = Request.query.filter(or_(Request.status == 'Отклонена',Request.status == 'Завершена')).order_by(Request.id.desc()).all()
        return render_template(
            "main/dashboard.html",
            requests_active=requests_active,
            requests_archive=requests_archive,
            requests=all_requests,
            user=current_user)

@dashboard.route('/request/<int:request_id>')
@login_required
def request_detail(request_id):
    request = Request.query.get_or_404(request_id)
    return render_template('main/request_detail.html', request=request, user=current_user)

@dashboard.route('/request/<int:request_id>/status', methods=['POST'])
@login_required
def update_status(request_id):
    req = Request.query.get_or_404(request_id)
    new_status = request.form.get('status')

    if new_status in ['Новая', 'В работе', 'Завершена', 'Отклонена']:
        req.status = new_status
        db.session.commit()
        flash(f'Статус заявки успешно изменен на "{new_status}"', 'success')
    else:
        flash('Недопустимый статус', 'danger')

    return redirect(url_for('dashboard.view_requests'))