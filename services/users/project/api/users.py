from flask import Blueprint, jsonify, request
from project.api.models import User
from project import db
from sqlalchemy import exc

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
	return jsonify({
		'status': 'success',
		'message': 'pong'
	})

@user_blueprint.route('/users', methods=['POST'])
def add_user():
	post_data = request.get_json()
	#Initializing the Response Object
	response_object = {
		'status': 'fail',
		'message': 'Invalid Payload'
	}
	#If the JSON is Empty
	if not post_data:
		return jsonify(response_object), 400
	username = post_data.get('username')
	email = post_data.get('email')
	try:
		#Checking if the Email exists in Database
		user = User.query.filter_by(email=email).first()
		#Adding User if not
		if not user:
			db.session.add(User(username=username, email=email))
			db.session.commit()
			response_object['status'] = 'success'
			response_object['message'] = f'{email} was added!'
			return jsonify(response_object), 201
		#Sending message if email already exists
		else:
			response_object['message'] = 'Sorry! That Email already exists!'
			return jsonify(response_object), 400
	#If Username or Email is not Given
	except exc.IntegrityError as e:
		db.session.rollback()
		return jsonify(response_object), 400

@user_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
	"""
	Get Single User Details
	"""
	#Initializing the response object
	response_object = {
		'status': 'fail',
		'message': 'User does not exist'
	}
	try:
		user = User.query.filter_by(id=user_id).first()
		#If the User ID does not exist in the database
		if not user:
			return jsonify(response_object), 404
		#Returning the User Detail for correct User ID
		else:
			response_object = {
				'status': 'success',
				'data': {
					'id': user.id,
					'username': user.username,
					'email': user.email,
					'active': user.active
				}
			}
			return jsonify(response_object), 200
	#If the User ID is not provided
	except exc.DataError as e:
		return jsonify(response_object), 404

@user_blueprint.route('/users', methods=['GET'])
def get_all_users():
	"""
	Get all users
	"""
	response_object = {
		'status': 'success',
		'data': {
			'users': [user.to_json() for user in User.query.all()]
		}
	}
	return jsonify(response_object), 200