from flask import Blueprint, jsonify

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
	return jsonify({
		'status': 'success',
		'message': 'pong'
	})