import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User

def add_user(username, email):
	user = User(username=username, email=email)
	db.session.add(user)
	db.session.commit()
	return user

class TestUserService(BaseTestCase):
	"""
	Tests for the Users Service.
	"""

	def test_user(self):
		"""
		Ensure the /users/ping route behaves correctly.
		"""
		response = self.client.get('/users/ping')
		data = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 200)
		self.assertIn('pong', data['message'])
		self.assertIn('success', data['status'])

	def test_add_user(self):
		"""
		Ensure a new user can be added to the Database.
		"""
		with self.client:
			response = self.client.post(
				'/users',
				data=json.dumps({
					'username': 'apoorvelous',
					'email': 'apoorvelous@gmail.com'
				}),
				content_type='application/json',
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 201)
			self.assertIn('apoorvelous@gmail.com was added!', data['message'])
			self.assertIn('success', data['status'])

	def test_add_user_invalid_json(self):
		"""
		Ensure Error is thrown if the JSON object is Empty.
		"""
		with self.client:
			response = self.client.post(
				'/users',
				data = json.dumps({}),
				content_type='application/json',
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('Invalid Payload', data['message'])
			self.assertIn('fail', data['status'])

	def test_add_user_invalid_json_keys(self):
		"""
		Ensure Error is Thrown if the JSON object does not have a username key.
		"""
		with self.client:
			response = self.client.post(
				'/users',
				data = json.dumps({'email': 'apoorvelous@gmail.com'}),
				content_type='application/json',
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('Invalid Payload', data['message'])
			self.assertIn('fail', data['status'])

	def test_add_user_duplicate_email(self):
		"""
		Ensure Error is Thrown if the Email already exists.
		"""
		with self.client:
			self.client.post(
				'/users',
				data = json.dumps({
					'username': 'apoorvelous',
					'email': 'apoorvelous@gmail.com'
				}),
				content_type='application/json',
			)
			response = self.client.post(
				'/users',
				data = json.dumps({
					'username': 'apoorvelous',
					'email': 'apoorvelous@gmail.com'
				}),
				content_type='application/json',
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn(
				'Sorry! That Email already exists!', data['message']
			)
			self.assertIn('fail', data['status'])

	def test_single_user(self):
		"""
		Ensure Get Single User Behaves Correctly
		"""
		user = add_user('apoorvelous', 'apoorvelous@gmail.com')
		with self.client:
			response = self.client.get(f'/users/{user.id}')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 200)
			self.assertIn('apoorvelous', data['data']['username'])
			self.assertIn('apoorvelous@gmail.com', data['data']['email'])
			self.assertIn('success', data['status'])

	def test_single_user_no_id(self):
		"""
		Ensure Error is thrown if the ID is not Provided
		"""
		with self.client:
			response = self.client.get('/users/blah')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 404)
			self.assertIn('User does not exist', data['message'])
			self.assertIn('fail', data['status'])

	def test_single_user_incorrect_id(self):
		"""
		Ensire Error is thrown if the ID does not exists
		"""
		with self.client:
			response = self.client.get('/users/333')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 404)
			self.assertIn('User does not exist', data['message'])
			self.assertIn('fail', data['status'])

	def test_all_users(self):
		"""
		Ensure get all users behaves correctly
		"""
		add_user('apoorvelous', 'apoorvelous@gmail.com')
		add_user('kherashanu', 'kherashanu@gmail.com')
		with self.client:
			response = self.client.get('/users')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 200)
			self.assertEqual(len(data['data']['users']), 2)
			self.assertIn('apoorvelous', data['data']['users'][0]['username'])
			self.assertIn('apoorvelous@gmail.com', data['data']['users'][0]['email'])
			self.assertIn('kherashanu', data['data']['users'][1]['username'])
			self.assertIn('kherashanu@gmail.com', data['data']['users'][1]['email'])
			self.assertIn('success', data['status'])

if __name__ == '__main__':
	unittest.main()