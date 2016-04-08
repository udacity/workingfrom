import argparse
from collections import namedtuple
import datetime as dt
import os

from flask import Flask, request, abort, json
from flask.ext.sqlalchemy import SQLAlchemy

import requests

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# This is for parsing the command
parser = argparse.ArgumentParser()
parser.add_argument('location', type=str)
parser.add_argument('-default', action='store_true')
parser.add_argument('-channels', type=str)
parser.add_argument('-help', action='store_true')

# This for making a fake parser object, duck typing thing
Data = namedtuple('Data', ['name'])

class User(db.Model):
	name = db.Column(db.String(50), primary_key=True)
	location = db.Column(db.String(500))
	default = db.Column(db.String(500))
	date = db.Column(db.Date)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<User {} is working from {}>".format(self.name, self.location)


@app.route("/", methods=['POST'])
def workingfrom():
	
	data = check_request(request)
	user_name, text = data.get('user_name'), data.get('text')

	parsed_text, action = parse_text(text)
	
	if action == 'set':
		
		if parsed_text.help:
			return app.config["HELP_TEXT"]

		user = User.query.filter_by(name=user_name).first()
		if user is None:
			user = User(user_name)
		
		location = parsed_text.location
		user.location = location
		user.date = dt.datetime.now()
		db.session.add(user)

		if parsed_text.default:
			user.default = location
			db.session.commit()
			return "Setting your default location to {}.\n".format(location)
		else:
			db.session.commit()

		announcement = "@{} is working from {}.\n".format(user.name, location)

		channels = ['#working-from']
		if data.get('channel_name') != 'working-from':
			channels.append(data.get('channel_name'))

		for each in parsed_text.channels.split(','):
			channels.append(each)

		for channel in channels:
			if channel[0] != '#':
				channel = '#' + channel
			payload = {"text": announcement,
				       "channel": channel,
				       "username": "workingfrom"}
			json_data = json.dumps(payload)
			requests.post(app.config["WEBHOOK_URL"], data=json_data)

		return "Got it, you're working from {}".format(location)
	
	elif action == 'get':
		user = User.query.filter_by(name=parsed_text.name).first()
		if user is None:
			return "Sorry, we don't have a record for {}.\n".\
					format(parsed_text['name'])

		if user.date == dt.datetime.now().date():
			format_date = "today"
		else:
			format_date = user.date.strftime("%D")
		
		reply = "@{} is working from {}, as of {}.".\
				format(user.name, user.location, format_date)
		if user.default is not None and format_date != "today":
			reply = reply + " Typically working from {}.".format(user.default)
		return reply + "\n"

def check_request(request):
	data = request.form
	if data.get('token') != app.config['TOKEN']:
		return abort(403)
	else:
		return data

def parse_text(text):
	
	if text[0] == '@':
		action = 'get'
		data = Data(text[1:])
	else:
		action = 'set'
		data = parser.parse_args(text.split())
		
	return data, action


if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)