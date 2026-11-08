from flask import Blueprint, jsonify,  Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from ..build import csrf, db
from flask import request

from ..models import Staff

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/help', methods=['GET'])
@csrf.exempt
def api_help():
    text = """
    1. ВХОД (получить токен):
        curl.exe -X POST http://127.0.0.1:5000/api/admin/login -H "Content-Type: application/json" -d "{\\"login\\":\\"BigBOSS\\",\\"password\\":\\"12345\\"}"
            
    2. РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ:
        curl.exe -X POST http://127.0.0.1:5000/api/admin/create_staff -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d "{\\"login\\":\\"manager1\\",\\"password\\":\\"123\\",\\"email\\":\\"m@test.ru\\",\\"full_name\\":\\"Петров П.\\",\\"role\\":\\"manager\\"}"
        """
    return Response(text, mimetype='text/plain; charset=utf-8')


@api.route('/admin/login', methods=['POST'])
@csrf.exempt
def admin_login():
    data = request.get_json()

    if not data or not data.get('login') or not data.get('password'):
        return jsonify({"msg": "Не хватает логина или пароля"}), 400

    staff = Staff.query.filter_by(login = data['login']).first()

    if not staff or not staff.check_password(data['password']):
        return jsonify({"msg": "Неверный логин или пароль"}), 401

    if staff.role != 'admin':
        return jsonify({"msg": "Доступ запрещен. Требуются права администратора."}), 403


    access_token = create_access_token(identity='str(staff.id)',
        additional_claims={"role": staff.role})

    return jsonify({
        "msg": "Успешный вход",
        "access_token": access_token,
        "role": staff.role,
        "full_name": staff.full_name
    }), 200


@api.route('/admin/create_staff', methods=['POST'])
@csrf.exempt
@jwt_required()
def staff_create():
    claims = get_jwt()

    if claims.get('role') != 'admin':
        return jsonify({"msg": "Доступ запрещен. Требуются права администратора."}), 403

    data = request.get_json()

    required_fields = ['login', 'password', 'email', 'full_name']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"msg": f"Все поля обязательны: {required_fields}"}), 400

    role = data.get('role', 'manager')
    allowed_roles = ['admin', 'manager', 'engineer']
    if role not in allowed_roles:
        return jsonify({"msg": f"Неверная роль. Допустимые: {allowed_roles}"}), 400

    if Staff.query.filter_by(login = data['login']).first(): return jsonify({"msg": "Сотрудник с таким логином уже существует"}), 409
    if Staff.query.filter_by(login = data['email']).first(): return jsonify({"msg": "Сотрудник с таким email уже существует"}), 409

    try:
        new_staff = Staff(
            login = data['login'],
            email = data['email'],
            full_name = data['full_name'],
            role = role)

        new_staff.set_password(data['password'])

        db.session.add(new_staff)
        db.session.commit()

        return jsonify({
        "msg": f"Пользователь {data['full_name']}",
        "staff_id": new_staff.id,
        "login": new_staff.login,
        "role": new_staff.role
    }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Внутренняя ошибка сервера: {str(e)}"}), 500