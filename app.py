import datetime as dt

from flask import Flask, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	name = db.Column(db.String(50), primary_key=True)
	where = db.Column(db.String(140))
	default = db.Column(db.String(140))
	date = db.Column(db.Date)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<User {} is working from {}>".format(self.name, self.where)

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

@app.route("/wf", methods=['POST'])
def workingfrom():
	
	data = check_json(request)
	user_name, text = data['user_name'], data['text']

	data, action = parse_text(text)
	
	if action == 'set':
		user = User.query.filter_by(name=user_name).first()
		if user is None:
			user = User(user_name)
		
		location = data['location']
		user.where = location
		user.date = dt.datetime.now()
		
		db.session.add(user)
		db.commit()
		return "We'll let them know {} is working from {}".\
			    format(user.name, location)
	
	elif action == 'get':
		user = User.query.filter_by(name=data['user_name']).first()
		if user is None:
			return "Sorry, we don't have a record for {}".\
					format(data['user_name'])

		if user.date == dt.datetime.now().date:
			format_date = "today"
		else:
			format_date = user.date
		
		reply = "{} is working from {}, as of {}.".\
				format(user.name, user.where, format_date)
		return 
		

def check_json(request):
	if not request.json or request.json['token'] != app.config['TOKEN']:
		abort(400)
	else:
		return request.json

def parse_text(text):
	pass
		




	