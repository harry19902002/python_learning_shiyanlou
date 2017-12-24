from flask import Flask,request,render_template,abort
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

class File(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(80))
	create_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	content = db.Column(db.Text)
	category = db.relationship('Category',backref = db.backref('post',lazy = 'dynamic'))

	def __init__(self,title,create_time,category,content):
		self.title = title
		self.create_time = create_time
		self.category = category
		self.content = content

	def __repr__(self):
		return str(self.id)

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return str(self.id)

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
	id_list = db.session.query(File).all()
	if filename in id_list:
		file_db = db_session.query(File).filter(File.id == id).first()
		print (file_db.title)
	else:
		abort(404)

@app.route('/address')
def address():
	return(os.path.realpath(__file__))

@app.errorhandler(404)
def not_found(error):
	error_name = 'shiyanlou 404'
	return render_template('404.html',error_name=error_name),404