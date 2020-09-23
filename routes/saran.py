from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
import routes.utils.db as db
import routes.utils.auth as auth

saran = Blueprint('saran', __name__)


@saran.route('/add-saran', methods=['POST'])
@cross_origin()
def add_saran():
    data = request.json
    teks = data['teks']
    email = data['email']
    result_query = db.add_saran(teks, email)
    if result_query['message'] == 'success':
        return jsonify(result_query), 201
    else:
        return jsonify(result_query), 500


@saran.route('/saran')
def get_saran():
    try:
        saran_list = db.get_saran()
        return jsonify({
            'data': saran_list,
            'message': 'success'
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'server error',
            'error': str(e)
        }), 500


@saran.route('/update-saran-status', methods=['POST'])
@cross_origin()
def update_saran():
    data = request.json
    saran_id = data['id']
    dibaca = data['dibaca']
    result_query = db.update_saran(saran_id, dibaca)
    if result_query['message'] == 'success':
        return jsonify(result_query), 200
    else:
        return jsonify(result_query), 500
