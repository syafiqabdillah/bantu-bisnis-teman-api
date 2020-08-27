from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from datetime import datetime
import db 

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return "Hello, are you trying to hack this ? pls don't"

@app.route('/users', methods=['GET'])
def users():
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

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.json
    nama = data['nama']
    email = data['email']
    query_result = db.register(nama, email)
    message = query_result['message']
    returning_data = query_result['data']
    if message == 'success':
        return jsonify(query_result), 200
    else:
        return jsonify({
            'message': message,
        }), 500

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    email = data['email']
    password = data['password']
    try:
        message = db.login(email, password)['message']
        if message == 'success':
            return jsonify({
                'message': 'login success'
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

if __name__ == '__main__':
    app.run(debug=True)