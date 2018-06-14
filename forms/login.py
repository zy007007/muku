# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField, SelectField, IntegerField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length

__all__ = ['LoginForm', 'RegisterForm']


class LoginForm(FlaskForm):
    name = StringField(u'用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'下次自动登录')
    submit = SubmitField(u'登录')


class RegisterForm(FlaskForm):
    name = StringField(u'姓名')
    password = StringField(u'密码')
    position = SelectField(u'职位', choices=[(u'校长', u'校长'), (u'教师', u'教师'), (u'管理员', u'管理员')])
    classroom = IntegerField(u'班级')
    submit = SubmitField(u'注册')
