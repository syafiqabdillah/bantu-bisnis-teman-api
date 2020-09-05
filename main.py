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

@app.route('/kontak-toko/<toko_id>', methods=['GET'])
def kontak_toko(toko_id):
    try:
        toko = db.kontak_toko(toko_id)
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
    kategori_id = data['kategori_id']
    nama = data['nama']
    harga = data['harga']
    imageUrl = data['imageUrl']
    query_result = db.add_product(toko_id, kategori_id, nama, harga, imageUrl)
    if query_result['message'] == "success":
        return jsonify(query_result), 201
    else:
        return jsonify(query_result), 500

@app.route('/update-product', methods=['POST'])
@cross_origin()
def update_product():
    data = request.json
    produk_id = data['id']
    nama = data['nama']
    kategori_id = data['kategori_id']
    harga = data['harga']
    imageUrl = data['imageUrl']
    status = data['status']
    query_result = db.update_product(produk_id, nama, kategori_id, harga, imageUrl, status)
    if query_result['message'] == "success":
        return jsonify(query_result), 201
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

@app.route('/search-products/<search_query>', methods=['GET'])
def search_products(search_query):
    try:
        product_list = db.search_products(search_query)
        return jsonify({
            'data': product_list,
            'message': 'success'
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'server error'
        }), 500

@app.route('/search-products-by-category/<kategori_id>', methods=['GET'])
def search_products_by_category(kategori_id):
    try:
        if kategori_id != "0":
            product_list = db.search_products_by_category(kategori_id)
        else:
            product_list = db.all_products()
        return jsonify({
            'data': product_list,
            'message': 'success'
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'server error'
        }), 500

# KATEGORI
@app.route('/add-kategori', methods=['POST'])
@cross_origin()
def add_kategori():
    data = request.json
    nama = data['nama']
    query_result = db.add_kategori(nama)
    print(query_result)
    if query_result['message'] == "success":
        return jsonify(query_result), 201
    else:
        return jsonify(query_result), 500

@app.route("/kategori", methods=['GET'])
def kategori():
    try:
        list_kategori = db.kategori()
        return jsonify({
            "data": list_kategori,
            "message": "success"
        })
    except:
        return jsonify({
            "message": "failed"
        })

@app.route('/email-available', methods=['POST'])
@cross_origin()
def email_available():
    data = request.json
    query_result = db.email_available(data['email'])
    return jsonify({
        "email_available": query_result 
    })

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

# Product view 

@app.route('/view-sum/<produk_id>', methods=['GET'])
def get_view_sum(produk_id):
    view_sum = db.get_view_sum(produk_id)
    return jsonify({
        'produk_id': produk_id,
        'view_sum': view_sum
    })

@app.route('/add-view/<produk_id>', methods=['POST'])
@cross_origin()
def add_view(produk_id):
    query_result = db.add_view(produk_id)
    if query_result['message'] == 'success':
        return jsonify(query_result), 200
    else:
        return jsonify(query_result), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')