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
	progress=[20,1]
	hint=['save','change','visit','channel','buy','open','money','Tony','the','door','me']
	checklist=[]
	return render_template('engcademy0.html',checklist=checklist,hint=hint,progress=progress)


@app.route('/engcademy/1')
def engcademy2():
	progress=[40,2]
	hint= ['talk','travel','refresh','give','the','watch','air','drama','you']
	checklist=[]
	return render_template('engcademy1.html',checklist=checklist,hint=hint,progress=progress)


@app.route('/engcademy/2')
def engcademy3():
	progress=[60,3]
	hint=['news','summer vacation','birthday','private','meeting']
	checklist=[]
	return render_template('engcademy2.html',checklist=checklist,hint=hint,progress=progress)


@app.route('/engcademy/3')
def engcademy4():
	progress=[80,4]
	hint=['travel', 'watch', 'private', 'news', 'birthday', 'channel', 'talk', 'summer vacation', 'meeting', 'drama', 'talk', 'save']
	checklist=[]
	return render_template('engcademy3.html',checklist=checklist,hint=hint,progress=progress)



@app.route('/engcademy/<temp>/check',methods=['POST'])
def engcademy_check(temp):
	qlist=[]		
	anslis=['in the class','from him','at the entrance','in R&D team','with blue shirts']
	anslist=[                                                                                                                                                            #답쓸때 리스트 중간중간에 콤마(,)
	['bought it','opened the door','saved money','changed the channel','visited me'],                                           #engcademy0 answer
	['to give you','to refresh the air','to travel','to watch the drama','to talk'],                                                          #engcademy1 answer
	['for your birthday','before the meeting','during the summer vacation','after the news','in private'],                #engcademy2 answer
	['I bought it to give you for your birthday', 'We opened the door to refresh the air before the meeting', 'He saved money to travel during the summer vacation', 'I changed the channel to watch the drama after the news', 'Tony visited me to talk in private']  #engcademy3 answer

	]
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
