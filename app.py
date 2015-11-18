import datetime as dt

from flask import Flask, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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

@app.route("/", methods=['POST'])
def workingfrom():
	
	slack_data = check_json(request)
	user_name, text = slack_data['user_name'], slack_data['text']

	data, action = parse_text(text)
	
	if action == 'set':
		user = User.query.filter_by(name=user_name).first()
		if user is None:
			user = User(user_name)
		
		location = data['location']
		user.where = location
		user.date = dt.datetime.now()
		
		db.session.add(user)
		db.session.commit()
		return "We'll let them know {} is working from {}.\n".\
			    format(user.name, location)
	
	elif action == 'get':
		user = User.query.filter_by(name=data['name']).first()
		if user is None:
			return "Sorry, we don't have a record for {}.\n".\
					format(data['name'])

		if user.date == dt.datetime.now().date:
			format_date = "today"
		else:
			format_date = user.date.strftime("%D")
		
		reply = "@{} is working from {}, as of {}.\n".\
				format(user.name, user.where, format_date)
		return reply

def check_json(request):
	if not request.json or request.json['token'] != app.config['TOKEN']:
		abort(400)
	else:
		return request.json

def parse_text(text):
	data = {}
	if text[0] == '@':
		action = 'get'
		data['name'] = text[1:]
	else:
		action = 'set'
		data['location'] = text
		
	return data, action

if __name__ == '__main__':
    app.run()