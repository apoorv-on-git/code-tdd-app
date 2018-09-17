import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Instantiate the DB
db = SQLAlchemy()


def create_app(script_info=None):

	#Instantiate the App
	app = Flask(__name__)

	#Set Config
	app_settings = os.getenv('APP_SETTINGS')
	app.config.from_object(app_settings)

	#Set up Extention
	db.init_app(app)

	#Register Blueprints
	from project.api.users import user_blueprint
	app.register_blueprint(user_blueprint)

	#Shell context for Flask CLI
	@app.shell_context_processor
	def ctx():
		return {'app': app, 'db': db}

	return app