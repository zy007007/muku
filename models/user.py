# -*- coding:utf-8 -*-
from config.ext import db
from flask_login import UserMixin
from config.ext import user_login_manager


@user_login_manager.user_loader
def user_loader(user_id):
    user = UserModel.query.filter_by(id=user_id).first()
    return user


class UserModel(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(64))
    mobile = db.Column(db.String(11))
    position = db.Column(db.String(32))
    password = db.Column(db.String(128))
    classroom = db.Column(db.Integer)



