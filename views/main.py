# -*- coding:utf-8 -*-
import time, os, xlrd
from flask import Flask
from flask import render_template, redirect, url_for, Blueprint, request
from heplers.override import tmpl
from flask_login import login_required, current_user, logout_user
from models.user import UserModel
from models.tables import StudentDoc, HomeworkDoc
from forms.excel import ExcelForm
from heplers.homework import homework_main_display
from heplers.test import test_main_display
from heplers.spoc import spoc_main_display
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


__all__ = ['bp']

bp = Blueprint('main', __name__, url_prefix='/main')


@bp.route("/page")
@login_required
def main():
    user = current_user.name
    return tmpl(user=user)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.index'))
