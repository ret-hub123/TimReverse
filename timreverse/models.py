from datetime import datetime, timezone
from flask_login import UserMixin
from .build import db, login_manager
from sqlalchemy import CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash


class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), nullable=False)
    second_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    requests = db.relationship('Request', backref='client', lazy=True)

    def __repr__(self):
        return f'<Client {self.email}>'

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False, default='Без темы')
    description = db.Column(db.Text,  nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    status = db.Column(db.String(20), default='Новая', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Request {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(int(user_id))

class Staff(db.Model, UserMixin):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)

    login = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'manager', 'engineer')", name='check_staff_role'),
    )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<Staff {self.full_name},{self.email}, {self.role}>'