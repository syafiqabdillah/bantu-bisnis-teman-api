from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
import routes.utils.db as db
import routes.utils.auth as auth

toko = Blueprint('toko', __name__)


@toko.route('/toko/<user_id>', methods=['GET'])
def get_toko(user_id):
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


@toko.route('/view-toko/<toko_id>', methods=['GET'])
def view_toko(toko_id):
    try:
        toko = db.view_toko(toko_id)
        return jsonify({
            'data': toko,
            'message': 'success'
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'server error'
        }), 500


@toko.route('/kontak-toko/<toko_id>', methods=['GET'])
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


@toko.route('/update-toko', methods=['POST'])
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
    query_result = db.update_toko(
        toko_id, nama, alamat, nohp, shopee, tokopedia, instagram)
    message = query_result['message']
    if message == 'success':
        return jsonify({
            'message': "update success",
        }), 200
    else:
        return jsonify({
            'message': "update failed",
        }), 500


@toko.route('/ecom-view-sum/<toko_id>', methods=['GET'])
def get_ecom_view_sum(toko_id):
    view_sum = db.get_ecom_view_sum(toko_id)
    return jsonify({
        'toko_id': toko_id,
        'view_sum': view_sum
    })


@toko.route('/add-ecom-view/<toko_id>', methods=['POST'])
@cross_origin()
def add_ecom_view(toko_id):
    query_result = db.add_ecom_view(toko_id)
    if query_result['message'] == 'success':
        return jsonify(query_result), 200
    else:
        return jsonify(query_result), 500


@toko.route('/toko', methods=['GET'])
def all_toko():
    list_toko = db.all_toko()
    return jsonify({
        'list_toko': list_toko
    })