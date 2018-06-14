# -*- coding:utf-8 -*-
import time, os, xlrd, urllib2, StringIO
from pylab import plot, show
from numpy import genfromtxt
from flask import Flask
from flask import render_template, redirect, url_for, Blueprint, request
from heplers.override import tmpl
from flask_login import login_required, current_user, logout_user
from models.user import UserModel
from models.tables import *
from forms.excel import ExcelForm
from heplers.utils import export_excel
from xlsxwriter.workbook import Workbook
from heplers.student import student_analysis_temp, student_analysis_temps, student_detail
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


__all__ = ['bp']

bp = Blueprint('student', __name__, url_prefix='/student')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.index'))


@bp.route('/students')
@login_required
def students_list():
    keyword = request.args.get('keyword', 'null', type=str)
    stu = None
    if keyword != 'null':
        if len(keyword) != 8:
            stu = StudentDoc.objects(real_name=keyword).all()
        else:
            stu = StudentDoc.objects(student_id=keyword).all()
    user = current_user.name
    students = StudentDoc.objects.all()
    return tmpl(students=students, user=user, stu=stu, keyword=keyword)


@bp.route('/delete/<string:id>')
@login_required
def students_delete(id):
    stu = StudentDoc.objects.get_or_404(id=id)
    stu.delete()
    return redirect(request.referrer)


@bp.route('/detail/<string:id>')
@login_required
def students_detail(id):
    stu = student_detail(id)
    return tmpl(stu=stu)


@bp.route('/analysis')
@login_required
def students_analysis():
    test = request.args.get('test', 0.0, type=float)
    homework = request.args.get('homework', 0.0, type=float)
    studentss = None
    if test != 0.0 and homework != 0.0:
        studentss = student_analysis_temps(test, homework)
    students = student_analysis_temp()
    return tmpl(students=students, studentss=studentss, test=test*100, homework=homework*100, t=test, h=homework)


@bp.route('/export/<float:test>/<float:homework>')
@login_required
def students_quan_export(test, homework):
    all = student_analysis_temps(test, homework)

    filename = u'{0}%测试，{1}%作业'.format(test*100, homework*100)

    output = StringIO.StringIO()
    office = Workbook(output)
    worksheet = office.add_worksheet()
    row = [u'学号', u'姓名', u'第一周作业', u'第二周作业', u'第三周作业', u'第四周作业', u'第六周作业',
           u'第一单元测验', u'第二单元测验', u'第三单元测验', u'第四单元测验', u'第五单元测验(1)', u'第五单元测验(2)',
           u'第六单元测验', u'作业总和', u'测验总和', u'总和(百分制)', u'权分(百分制)']
    worksheet.write_row(0, 0, row)
    for i in xrange(len(all)):
        worksheet.write_row(i + 1, 0, all[i - 1])
    office.close()
    return export_excel(filename, output)


