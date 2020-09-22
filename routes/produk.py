from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
import routes.utils.db as db
import routes.utils.auth as auth

produk = Blueprint('produk', __name__)


@produk.route('/add-product', methods=['POST'])
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


@produk.route('/update-product', methods=['POST'])
@cross_origin()
def update_product():
    data = request.json
    produk_id = data['id']
    nama = data['nama']
    kategori_id = data['kategori_id']
    harga = data['harga']
    imageUrl = data['imageUrl']
    status = data['status']
    query_result = db.update_product(
        produk_id, nama, kategori_id, harga, imageUrl, status)
    if query_result['message'] == "success":
        return jsonify(query_result), 201
    else:
        return jsonify(query_result), 500


@produk.route('/products/<toko_id>', methods=['GET'])
def products(toko_id):
    try:
        product_list = db.products(toko_id)
        return jsonify({
            'data': product_list,
            'message': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'server error',
            'error': str(e)
        }), 500


@produk.route('/products', methods=['GET'])
def all_products():
    try:
        product_list = db.all_products()
        return jsonify({
            'data': product_list,
            'message': 'success'
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'server error',
            'error': str(e)
        }), 500


@produk.route('/search-products-by-category/<kategori_id>', methods=['POST'])
def search_products_by_category(kategori_id):
    data = request.json
    search_query = data['search_query']
    try:
        if kategori_id != "0":
            product_list = db.search_products_by_category(kategori_id, search_query)
        else:
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


@produk.route('/view-sum/<produk_id>', methods=['GET'])
def get_view_sum(produk_id):
    view_sum = db.get_view_sum(produk_id)
    return jsonify({
        'produk_id': produk_id,
        'view_sum': view_sum
    })


@produk.route('/add-view/<produk_id>', methods=['POST'])
@cross_origin()
def add_view(produk_id):
    query_result = db.add_view(produk_id)
    if query_result['message'] == 'success':
        return jsonify(query_result), 200
    else:
        return jsonify(query_result), 500
