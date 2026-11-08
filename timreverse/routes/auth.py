from flask import request, url_for

from flask import Blueprint, flash, redirect
from flask import render_template
from ..forms import LoginForm
from ..models import Staff
from flask_login import login_user, logout_user, login_manager, login_required

auth = Blueprint('auth', __name__)

@auth.route('/auth', methods=['GET', 'POST'])
def auth_page():
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(login = form.login.data).first()

        if staff and staff.check_password(form.password.data):
            login_user(staff)
            flash('Вы успешно вошли в систему.', 'success')

            return redirect(url_for('dashboard.view_requests'))
        else:
            flash('Неверный логин или пароль.', 'danger')

    return render_template("main/auth.html", form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('auth.auth_page'))