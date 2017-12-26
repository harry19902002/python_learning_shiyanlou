from flask import Flask,request,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

client = MongoClient('127.0.0.1', 27017)
mongo_db = client.shiyanlou


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

	def add_tag(self, tag_name):
		mongo_db.user.insert_one({'id':self.id,'tag':tag_name})
	def remove_tag(self, tag_name):
		mongo_db.user.delete_one({'id':self.id,'tag':tag_name})

	@property
	def tags(self):
		tag_list = []
		for user in mongo_db.user.find({'id':self.id}):
			tag_list.append(user['tag'])
		return tag_list


class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return str(self.id)

@app.route('/')
def index():
	title_list = {}
	tag_list = {}
	db_list = db.session.query(File).all()
	for file_db in db_list:
		title_list[file_db.title] = '/files/' + str(file_db.id)
		tag_list[file_db.title] = file_db.tags
	return render_template('index.html',title_list = title_list, tag_list = tag_list)

@app.route('/files/<input>')
def file(input):
	id = int(input)
	db_list = db.session.query(File).all()
	for file_db in db_list:	
		print(file_db.id)	
		if id == file_db.id:
			print('True')
			file_db = db.session.query(File).filter(File.id == id).first()
			return render_template('file.html', file = file_db)
	abort(404)

@app.route('/address')
def address():
	return(os.path.realpath(__file__))

@app.errorhandler(404)
def not_found(error):
	error_name = 'shiyanlou 404'
	return render_template('404.html',error_name=error_name),404