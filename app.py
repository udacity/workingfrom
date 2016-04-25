import argparse
import datetime as dt
import os

from flask import Flask, request, abort, json
from flask.ext.sqlalchemy import SQLAlchemy

import requests

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


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

	if "-help" in text:
		return app.config["HELP_TEXT"]

	text_data, action = parse_text(text)
	
	if action == 'set':
		
		user = User.query.filter_by(name=user_name).first()
		if user is None:
			user = User(user_name)
		
		location = text_data['location']
		user.location = location
		user.date = dt.datetime.now()
		db.session.add(user)

		if text_data.get('default'):
			user.default = location
			db.session.commit()
			return "Setting your default location to {}.\n".format(location)
		else:
			db.session.commit()

		announcement = "@{} is working from {}.\n".format(user.name, location)

		channels = ['#working-from']
		if data.get('channel_name') != 'working-from':
			channels.append(data.get('channel_name'))

		if text_data.get('channels'):
			for each in text_data['channels']:
				channels.append(each.strip())

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
		user = User.query.filter_by(name=text_data['text']).first()
		if user is None:
			return "Sorry, we don't have a record for {}.\n".\
					format(text_data['text'])

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

def haschannels(words):
	for word in words:
		if word.startswith('#'):
			return True
	else:
		return False

def parse_text(text):
	data = {}
	if text[0] == '@':
		action = 'get'
		data['text'] = text[1:]
	else:
		action = 'set'
		words = text.split()

		if ' -' in text:
			data['location'] = text[:text.index(' -')]
		elif '#' in text:
			data['location'] = text[:text.index(' #')]
		else:
			data['location'] = text

		if '-default' in words:
			data['default'] = True
		
		if '-channels' in words:
			channels = ' '.join(words[words.index('-channels') + 1:])
			data['channels'] = channels.replace(',', '').split()
		elif haschannels(words):
			data['channels'] = [word for word in words if word.startswith('#')]
		


	return data, action


if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)