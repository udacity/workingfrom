from flask import Flask, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.String, unique=True)
	user = db.Column(db.String(50), unique=True)
	where = db.Column(db.String(100))

	def __init__(self, id, user, where):
		self.id = id
		self.user = user
		self.where = where

	def __repr__(self):
		return '<User {} is working from {}>'.format(self.user, self.where)

"""
token=Mxv5RXsVVXGlTGWNkuXhQJrX
team_id=T0001
team_domain=example
channel_id=C2147483705
channel_name=test
user_id=U2147483697
user_name=Steve
command=/weather
text=94070
"""

@app.route("/workingfrom", methods=['POST'])
def workingfrom():
	
	blob = check_json(request)
	user_id, user, text = blob['user_id'], blob['user_name'], blob['text']

	location = process_text(text)
	return "{} is working from {}".format(user), 200

@app.route("/whereis", methods=['POST'])
def whereis():
	blob = check_json(request)

def check_json(request):
	if not request.json or request.json['token'] != app.config['TOKEN']:
		abort(400)
	else:
		return request.json

def process_text(text):

	text.split()