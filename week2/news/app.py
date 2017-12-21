from flask import Flask,request,render_template,abort
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
	files = os.listdir('/home/shiyanlou/files')
	output = {}
	for filename in files:
		with open('/home/shiyanlou/files/{}'.format(filename),'r') as file:
			content = json.loads(file.read())
			output[filename] = content
	print(output)
	return render_template('index.html',output = output)

@app.route('/files/<filename>')
def file(filename):
	try:
		with open('/home/shiyanlou/files/{}.json'.format(filename),'r') as file:
			article = json.loads(file.read())
		return render_template('file.html', article = article)
	except FileNotFoundError:
		abort(404)

@app.errorhandler(404)
def not_found(error):
	error_name = 'shiyanlou 404'
	return render_template('404.html',error_name=error_name),404