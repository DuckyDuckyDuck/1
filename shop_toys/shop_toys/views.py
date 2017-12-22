# -*- coding: utf-8 -*- 
from pyramid.view import view_config
from pyramid.response import Response
from models import *
import re
from datetime import *


from pyramid.security import (
remember,
forget,
)

from pyramid.httpexceptions import (
HTTPFound,
HTTPNotFound,
)


@view_config(route_name='index', renderer='templates/index.jinja2')
def index(request):
    return {'username': request.authenticated_userid}


@view_config(route_name='addComment', renderer='templates/addComment.jinja2')
def addComment(request):
	if request.method == "POST":
		session = Session(bind = engine)
		new_comment = Comments(Login = request.authenticated_userid,
								Name_com = request.params['name'],
								Text = request.params['comment'],
								Date = datetime.now())
		session.add(new_comment)
		session.commit()
		return HTTPFound(location = request.route_url('responces', _query={'username': request.authenticated_userid}))
	else:
		return { 'username': request.authenticated_userid }

@view_config(route_name='addAdress', renderer='templates/addAdress.jinja2')
def addAdress(request):
	if request.method == "POST":
		session = Session(bind = engine)
		new_adress = adress(adress = request.params['Adress'])
		session.add(new_adress)
		session.commit()
		return HTTPFound(location = request.route_url('adresses', _query={'username': request.authenticated_userid}))
	else:
		return { 'username': request.authenticated_userid }

@view_config(route_name='addGoods', renderer='templates/addGoods.jinja2')
def addGoods(request):
	if request.method == "POST":
		session = Session(bind = engine)
		new_goods = bGoods(	
								creater = request.params['creater'],
								text = request.params['text'],
								manufacturer = request.params['manufacturer'],
								date = datetime.now())
		session.add(new_goods)
		session.commit()
		return HTTPFound(location = request.route_url('goods', _query={'username': request.authenticated_userid}))
	else:
		return { 'username': request.authenticated_userid }

@view_config(route_name='responces', renderer='templates/responces.jinja2')
def responces(request):
	return {'username': request.authenticated_userid,
    		"comments" : Session(bind=engine).query(Comments).all()}

@view_config(route_name='adresses', renderer='templates/adresses.jinja2')
def responce(request):
	return {'username': request.authenticated_userid,
    		"qAdress" : Session(bind=engine).query(adress).all()}

@view_config(route_name='goods', renderer='templates/goods.jinja2')
def goods(request):
	return {'username': request.authenticated_userid,
    		"comments" : Session(bind=engine).query(bGoods).all()}

@view_config(route_name='register', renderer='templates/register.jinja2')
def register(request):
	if request.method == 'POST':
		session = Session(bind=engine)
		errors = []
		if(len(request.params['name']) <=3):
			errors.append(u"Введите имя")
		if(len(request.params['login']) <6):
			errors.append(u"Введите логин")
		if(len(request.params['password']) <=5):
			errors.append(u"Введите пароль")
		if(len(request.params['passwordTwo']) <=5):
			errors.append(u"Введите подтверждение пароля")
		if(request.params['password']!= request.params['passwordTwo']):
			errors.append(u'Пароли не совпадают')
		if(session.query(User).filter_by(Login=request.params['login']).count() != 0):
			errors.append(u'Такой логин уже существует')
		if(len(errors) != 0):
			return { 'errors' : errors ,
					 'name' : request.params['name'],
					 'login' : request.params['login'],
					 'mail' : request.params['mail'],
					 'secondName' : request.params['secondName'],
					 'username': request.authenticated_userid }
		else:
			new_user = User(request.params['login'],
							request.params['password'],
							request.params['mail'],
							request.params['name'],
							request.params['secondName']);
			session.add(new_user)
			session.commit()
			return HTTPFound(location = request.route_url('goodReg', goodReg='great', _query={'login' : request.params['login']}))
	else:
		return { 'username': request.authenticated_userid }

@view_config(route_name='logIn', renderer='templates/logIn.jinja2')
def logIn(request):
	if request.method == 'POST':
		user = Session(bind=engine).query(User).filter(User.Login == request.params['login']).first()
		if user != None and user.Password == request.params['password']:
			headers = remember(request, user.Login)			
			return HTTPFound(location = '/', headers = headers)
		else:
			return {'error': u"Введены неверные данные", 'username': request.authenticated_userid }
	else:
		return {'username' : request.authenticated_userid }

@view_config(route_name='logOut')
def logOut(request):
	headers = forget(request)
	return HTTPFound(location = '/', headers = headers)

@view_config(route_name='goodReg', renderer='templates/goodReg.jinja2')
def goodReg(request):
    return {'username': request.authenticated_userid,
    		'login' : request.params['login'] }
