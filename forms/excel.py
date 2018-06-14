# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField, SelectField
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired

__all__ = ['ExcelForm']


class ExcelForm(Form):
    excel = FileField(u'excel', validators=[DataRequired()])
    submit = SubmitField(u'确定')

