# -*- coding:utf-8 -*-
import time, os, xlrd
from flask import Flask
from flask import render_template, redirect, url_for, Blueprint, request
from heplers.override import tmpl
from flask_login import login_required, current_user, logout_user
from models.user import UserModel
from models.tables import CourseDoc
from forms.excel import ExcelForm
from heplers.course import course_exam_display, course_homework_display, course_test_display, course_main_display
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


__all__ = ['bp']

bp = Blueprint('course', __name__, url_prefix='/course')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.index'))


@bp.route('/list')
@login_required
def course_list():
    course = CourseDoc.objects().all()
    courses = list(set([h.name for h in course]))
    return tmpl(courses=courses)


@bp.route('/detail/<string:name>')
@login_required
def course_detail(name):
    courses = CourseDoc.objects(name=name).all()
    return tmpl(courses=courses, name=name)


@bp.route('/delete/<string:name>')
@login_required
def course_delete(name):
    courses = CourseDoc.objects(name=name).all()
    for c in courses:
        c.delete()
    return redirect(request.referrer)


@bp.route('/import', methods=['GET', 'POST'])
@login_required
def course_import():
    form = ExcelForm()
    if form.validate_on_submit():
        excel = request.files['excel']
        if excel:
            basedir = os.getcwd() + "/website/static/excel/"
            filename = 'course' + str(int(time.time())) + '.xlsx'
            excel.save(os.path.join(basedir, filename))
            workbook = xlrd.open_workbook(os.path.join(basedir, filename))
            sheet_one = workbook.sheet_by_name('Sheet1')
            course_name = sheet_one.row_values(0)[0]
            for rownum in range(2, sheet_one.nrows):
                course = CourseDoc(name=course_name,
                                   classify=sheet_one.row_values(rownum)[0],
                                   title=sheet_one.row_values(rownum)[1],
                                   datetime=sheet_one.row_values(rownum)[2],
                                   status=sheet_one.row_values(rownum)[3],
                                   score_type=sheet_one.row_values(rownum)[4],
                                   post_num=sheet_one.row_values(rownum)[5],
                                   sum_score=float(sheet_one.row_values(rownum)[6]),
                                   aver_score=float(sheet_one.row_values(rownum)[7]))
                course.save()
        return redirect(url_for('course.course_list'))
    return tmpl(form=form)


@bp.route('/analysis/list')
@login_required
def course_analysis_list():
    courses = course_main_display()
    return tmpl(courses=courses)


@bp.route('/analysis/<string:name>')
@login_required
def course_analysis(name):
    test = course_test_display(name)
    homework = course_homework_display(name)
    exam = course_exam_display(name)
    return tmpl(test=test, homework=homework, exam=exam)
