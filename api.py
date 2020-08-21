from flask import Blueprint, request, jsonify
from database import Database as db

api = Blueprint('api', __name__)

@api.route('/test')
def api_test():
	id = request.args.get('id', default='1')
	res = db.get_db().query("select * from users where id="+id)
	return jsonify({'message': res})
