from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Optional, Length, Email


class RequestForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(message="Введите имя"), Length(max=30)])
    second_name = StringField('Фамилия', validators=[DataRequired(message="Введите фамилию"), Length(max=30)])
    email = StringField('Почта', validators=[DataRequired(message="Введите почту"), Email(message="Некорректный email")])
    phone = StringField('Телефон', validators=[Optional(), Length(max=20)])

    title = StringField('Тема заявки', validators=[DataRequired(message="Укажите тему"), Length(max=100)])
    description = TextAreaField('Описание задачи', validators=[DataRequired(message="Опишите, что нужно сделать"), Length(max=2000)])

    submit = SubmitField('Отправить заявку')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(message="Введите логин")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Введите пароль")])
    submit = SubmitField('Войти')