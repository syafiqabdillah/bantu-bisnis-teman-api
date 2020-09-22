from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
import routes.utils.db as db
import routes.utils.auth as auth

kategori = Blueprint('kategori', __name__)


@kategori.route('/add-kategori', methods=['POST'])
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


@kategori.route("/all-kategori", methods=['GET'])
def all_kategori():
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


@kategori.route("/kategori", methods=['GET'])
def get_kategori():
    try:
        list_kategori = db.active_kategori()
        return jsonify({
            "data": list_kategori,
            "message": "success"
        })
    except:
        return jsonify({
            "message": "failed"
        })


@kategori.route("/update-kategori", methods=['POST'])
def update_kategori_status():
    new_kategori = request.json
    result_query = db.update_kategori(new_kategori)
    if result_query['message'] == 'success':
        return jsonify(result_query), 200
    else:
        return jsonify(result_query), 500
