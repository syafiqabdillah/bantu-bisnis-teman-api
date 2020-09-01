from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from datetime import datetime
import auth
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

@app.route('/toko/<user_id>', methods=['GET'])
def toko(user_id):
    try:
        toko = db.get_toko(user_id)
        return jsonify({
            'data': toko,
            'message': 'success'
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'server error'
        }), 500 

@app.route('/update-toko', methods=['POST'])
@cross_origin()
def update_toko():
    data = request.json
    toko_id = data['toko_id']
    nama = data['nama']
    alamat = data['alamat']
    nohp = data['nohp']
    shopee = data['shopee']
    tokopedia = data['tokopedia']
    instagram = data['instagram']
    query_result = db.update_toko(toko_id, nama, alamat, nohp, shopee, tokopedia, instagram)
    message = query_result['message']
    if message == 'success':
        return jsonify({
            'message': "update success",
        }), 200
    else:
        return jsonify({
            'message': "update failed",
        }), 500

# PRODUCT 

@app.route('/add-product', methods=['POST'])
@cross_origin()
def add_product():
    data = request.json
    toko_id = data['toko_id']
    nama = data['nama']
    harga = data['harga']
    imageUrl = data['imageUrl']
    query_result = db.add_product(toko_id, nama, harga, imageUrl)
    message = query_result['message']
    if message == "success":
        data['product_id'] = query_result['product_id']
        return jsonify(data), 201
    else:
        return jsonify(query_result), 500

@app.route('/products/<toko_id>', methods=['GET'])
def products(toko_id):
    try:
        product_list = db.products(toko_id)
        return jsonify({
            'data': product_list,
            'message': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'server error'
        }), 500 

@app.route('/products', methods=['GET'])
def all_products():
    try:
        product_list = db.all_products()
        return jsonify({
            'data': product_list,
            'message': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'server error'
        }), 500

@app.route('/add-kategori', methods=['POST'])
@cross_origin()
def add_kategori():
    data = request.json
    nama = data['nama']
    

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.json
    nama = data['nama']
    email = data['email']
    password = data['password']
    query_result = db.register(nama, email, password)
    message = query_result['message']
    returning_data = query_result['data']
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

@app.route('/login', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')