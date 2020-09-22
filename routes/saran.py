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
