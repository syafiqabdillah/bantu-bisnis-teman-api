from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
import routes.utils.db as db
import routes.utils.auth as auth

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    email = data['email']
    password = data['password']
    try:
        result = db.login(email, password)
        message = result['message']
        if message == 'success':
            return jsonify({
                'message': 'login success',
                'jwt': auth.create_jwt(result).decode()
            }), 200
        else:
            return jsonify({
                'message': 'login failed'
            }), 401
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'server error'
        }), 500


@user.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.json
    nama = data['nama']
    email = data['email']
    password = data['password']
    query_result = db.register(nama, email, password)
    message = query_result['message']

    if message == 'success':
        result = {
            'nama': nama,
            'email': email,
            'user_id': query_result['data']['user_id'],
            'toko_id': query_result['data']['toko_id']
        }
        return jsonify({
            'message': message,
            'jwt': auth.create_jwt(result).decode()
        }), 200
    else:
        return jsonify({
            'message': message,
        }), 500


@user.route('/email-available', methods=['POST'])
@cross_origin()
def email_available():
    data = request.json
    query_result = db.email_available(data['email'])
    return jsonify({
        "email_available": query_result
    })


@user.route('/users/<token>', methods=['GET'])
@cross_origin()
def users(token):
    if token and auth.read_jwt(token)['email'] == "syafiq.abdillah@ui.ac.id":
        try:
            users_list = db.get_all_users()
            return jsonify({
                'data': users_list,
                'message': 'success'
            }), 200
        except:
            return jsonify({
                'message': 'server error'
            }), 500
    else:
        return jsonify({
            'message': 'unauthorized'
        }), 430


@user.route('/update-user-status', methods=['POST'])
@cross_origin()
def update_user():
    data = request.json
    email = data['email']
    active = data['active']
    result_query = db.update_user(email, active)
    if result_query['message'] == 'success':
        return jsonify(result_query), 200
    else:
        return jsonify(result_query), 500

@user.route('/user-is-active/<user_id>')
def user_is_active(user_id):
    result_query = db.user_is_active(user_id)
    return jsonify({
        'data': {
            'is_active': result_query
        }
    }), 200