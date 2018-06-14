# -*- coding:utf-8 -*-
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from me import MongoEngine

__all__ = ['db', 'bootstrap', 'user_login_manager', 'mongo']

db = SQLAlchemy()
bootstrap = Bootstrap()
user_login_manager = LoginManager()
mongo = MongoEngine()


