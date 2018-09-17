from flask import Flask, jsonify

#Instantiate the App
app = Flask(__name__)

#Set Config
app.config.from_object('project.config.DevelopmentConfig') #New

@app.route('/users/ping', methods=['GET'])
def ping_pong():
	return jsonify({
		'status': 'success',
		'message': 'pong'
		})