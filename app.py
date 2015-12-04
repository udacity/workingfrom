import datetime as dt
import os

from flask import Flask, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('settings.py')
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
	
	slack_data = check_json(request)
	user_name, text = slack_data['user_name'], slack_data['text']

	data, action = parse_text(text)
	
	if action == 'set':
		user = User.query.filter_by(name=user_name).first()
		if user is None:
			user = User(user_name)
		
		location = data['location']
		
		if '--help' in data:
			return data['--help']

		if '--default' in data and data['--default']:
			user.default = location
			db.session.add(user)
			db.session.commit()
			return "Setting your default location to {}.\n".\
			    	format(location)

		user.location = location
		user.date = dt.datetime.now()
		db.session.add(user)
		db.session.commit()
		
		return "We'll let them know @{} is working from {}.\n".\
			    format(user.name, location)
	
	elif action == 'get':
		user = User.query.filter_by(name=data['name']).first()
		if user is None:
			return "Sorry, we don't have a record for {}.\n".\
					format(data['name'])

		if user.date == dt.datetime.now().date():
			format_date = "today"
		else:
			format_date = user.date.strftime("%D")
		
		reply = "@{} is working from {}, as of {}.".\
				format(user.name, user.location, format_date)
		if user.default is not None and format_date != "today":
			reply = reply + " Typically working from {}.".format(user.default)
		return reply + "\n"

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
		# Find options
		words = text.split()
		# Option indices
		opt_indices = [i for i, word in enumerate(words) if '--' in word]
		if opt_indices:
			# Rebuild location string from words before the first option
			data['location'] = ' '.join(words[:opt_indices[0]])
			
			# Grab the options and send text data to appropriate functions
			options = [words[each] for each in opt_indices]
			for opt_ind in opt_indices:
				option = words[opt_ind]
				# Calling the functions with words and opt_ind because some
				# options might need to use these in the future.
				data[option] = option_funcs[option](words, opt_ind)

		else:
			data['location'] = text
		
	return data, action

def default_location(a, b):
	return True

def call_help(a, b):
	help_text = """ Help for /workingfrom command.

		Use /workingfrom to let your coworkers know where you are. 

		It's pretty simple! Enter /workingfrom [location] to set where you're working from, where [location] can be any text, up to 500 characters. For instance, you can just say /workingfrom SF, or /workingfrom MTV. You can also write something longer: /workingfrom Out of office until January 14th.

		You can check someone's location with /workingfrom @[user].

		To set your default location, use the '--default' option: /workingfrom SF --default. This will let people know where you are if you haven't used /workingfrom recently.

		"""

	return help_text

option_funcs = {'--default': default_location,
				'--help': call_help}


if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)