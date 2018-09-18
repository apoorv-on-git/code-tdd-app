from flask.cli import FlaskGroup
from project import create_app, db
import unittest
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
	db.drop_all()
	db.create_all()
	db.session.commit()

@cli.command()
def test():
	"""
	Runs The Tests without code-coverage.
	"""
	tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)
	if result.wasSuccessful():
		return 0
	return 1

@cli.command()
def seed_db():
	"""
	Seeds the Database
	"""
	db.session.add(User(username="apoorvelous", email="apoorvelous@gmail.com"))
	db.session.add(User(username="kherashanu", email="kherashanu@gmail.com"))
	db.session.commit()

if __name__ == '__main__':
	cli()