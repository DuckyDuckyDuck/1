# -*- coding: utf-8 -*- 
from pyramid.config import Configurator
from shop_toys.resources import get_root
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import inspect
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Deny
from pyramid.security import Authenticated
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from models import *

class MyFactory(object):
    def __init__(self, request):
        self.__acl__ = [(Allow, Authenticated, "add")]

my_session_factory = SignedCookieSessionFactory('shop_toys')

def main(global_config, **settings):
    Base.metadata.create_all()

    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'shop_toys')

    config = Configurator(root_factory=MyFactory, settings=settings, session_factory=my_session_factory)
    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static')
    config.add_route("index" , '/')
    config.add_route("responces" , "/responces.html")
    config.add_route("goods" , "/goods.html")
    config.add_route("adresses" , "/adresses.html")

    config.add_route("goodReg", "/goodReg.html")
    config.add_route("register", "/register.html")
    config.add_route("logIn", '/logIn.html')
    config.add_route("logOut", "/logOut.html")
    config.add_route("addComment", "/addComment.html")
    config.add_route("addGoods", "/addGoods.html")
    config.add_route("addAdress", "/addAdress.html")


    authn_policy = AuthTktAuthenticationPolicy('sosecret', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.scan()
    return config.make_wsgi_app()
