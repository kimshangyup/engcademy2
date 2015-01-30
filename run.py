#-*- coding:utf-8 -*-

from flask import request, render_template, session, Flask, redirect, url_for, flash, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import urllib

app=Flask(__name__)
app.secret_key='asdfasdf'
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://ubuntu:sy1120@localhost/ubuntu'

db= SQLAlchemy(app)


class User(db.Model):
	__tablename__= 'tabletest'	

	id= db.Column(db.Integer, primary_key=True)
	username= db.Column(db.String(), unique=True, nullable=False)
	password= db.Column(db.String(), nullable=False)

	def __init__(self, username, password):
		self.username=username
		self.password=password

	def __repr__(self):
		return "hello %s" % self.username


class Question(db.Model):
	__tablename__= 'questions'	

	id= db.Column(db.Integer, primary_key=True)
	title= db.Column(db.String(), unique=True, nullable=False)
	text= db.Column(db.String(), nullable=False)

	def __init__(self, title, text):
		self.title=title
		self.text=text

@app.route('/signup') 
def signup():
	return render_template('signup.html', title='sign up for my service')


@app.route('/signup/check', methods=['POST'])
def signup_check():
	username=request.form['username']
	password=request.form['password']
	user1=User(username,password)
	db.session.add(user1)
	db.session.commit()
	return redirect(url_for('signup'))
	#flash메세지 뜨게하기 

@app.route('/') 
def engca():
	return render_template('index.html')




@app.route('/engcademy/0')
def engcademy1():
	checklist=[]
	return render_template('engcademy0.html',checklist=checklist)


@app.route('/engcademy/1')
def engcademy2():
	checklist=[]
	return render_template('engcademy1.html',checklist=checklist)


@app.route('/engcademy/2')
def engcademy3():
	checklist=[]
	return render_template('engcademy2.html',checklist=checklist)


@app.route('/engcademy/<temp>/check',methods=['POST'])
def engcademy_check(temp):
	qlist=[]		
	anslis=['in the class','from him','at the entrance','in R&D team','with blue shirts']
	anslist=[['bought it','opened the door','saved money','changed the channel','visited me'],['to give you','to refresh the air','to travel','to watch the drama','to talk'],['for your birthday','before the meeting','during the summer vacation','after the news','in private']]
	list=[]
	for i in range(0,5):
		qlist.append(request.form['q'+str(i)])
		if anslist[int(temp)][i]==qlist[i]:
			list.append('right')
		else:
			list.append('wrong')
	return jsonify(ment=list)


@app.route('/qna') 
def qna():
	question=Question.query.all()
	return render_template('qna.html',question=question)

@app.route('/qna/getqna', methods=['POST']) 
def getqna():
	title=request.form['title']
	text=request.form['text']
	question1=Question(title,text)
	if text:
		try:
			db.session.add(question1)
			db.session.commit()
			question=Question.query.all()
			flash('Thank you, your review is succefully posted')
			return render_template('qna.html',question=question)
		except:
			return "This question already exists"
	return redirect(url_for('qna'))




@app.route('/login') 
def login():
	return render_template('login.html',title='login for my service')

@app.route('/login/check', methods=['GET','POST'])
def login_check():
	checklist=[]
	username=request.form['username']
	password=request.form['password']
	users=User.query.filter(User.username==username).all()
	if users:
		if users[0].password==password:
			return render_template('engcademy0.html',checklist=checklist,title='Welcome, '+username,users=users)
			session['logged_in']=True
		else:
			return 'wrong password'
	else:
		return 'wrong id'


if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')
