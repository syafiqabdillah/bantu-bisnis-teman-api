from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

# importing the blueprints
from routes.saran import saran
from routes.user import user
from routes.toko import toko
from routes.produk import produk
from routes.kategori import kategori

app = Flask(__name__)

# registering the blueprints
app.register_blueprint(saran)
app.register_blueprint(user)
app.register_blueprint(toko)
app.register_blueprint(produk)
app.register_blueprint(kategori)

CORS(app)


@app.route('/', methods=['GET'])
def hello():
    return "Pls no"


# @app.route('/viewer-stats', methods=['GET'])
# def viewer_stats():
#     try:
#         stats = db.viewer_stats()
#         return jsonify({
#             'data': stats,
#             'message': 'success'
#         }), 200
#     except Exception as e:
#         print(e)
#         return jsonify({
#             'message': 'server error'
#         }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
