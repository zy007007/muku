# -*- coding:utf-8 -*-
import time, os, xlrd, urllib2, StringIO
from pylab import plot, show
from numpy import genfromtxt
from flask import Flask
from flask import render_template, redirect, url_for, Blueprint, request
from heplers.override import tmpl
from flask_login import login_required, current_user, logout_user
from models.user import UserModel
from models.tables import StudentDoc, TestScoreDoc
from forms.excel import ExcelForm
from xlsxwriter.workbook import Workbook
from heplers.utils import export_excel
from heplers.test import test_match, test_analysis_display, test_main_display, \
    test_detail_students, test_detail_export_students, test_match_one
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


__all__ = ['bp']

bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.index'))


@bp.route('/list')
@login_required
def test_list():
    user = current_user.name
    test = TestScoreDoc.objects().all()
    tests = list(set([h.name for h in test]))
    return tmpl(user=user, tests=tests)


@bp.route('/detail/<string:name>')
@login_required
def test_detail(name):
    keyword = request.args.get('keyword', 'null', type=str)
    stu = None
    if keyword != 'null':
        stu = test_match_one(name, keyword)
    students = test_match(name)
    return tmpl(students=students, name=name, stu=stu)


@bp.route('/delete/<string:name>')
@login_required
def test_delete(name):
    test = TestScoreDoc.objects(name=name).all()
    stu = StudentDoc.objects().all()
    for t in test:
        for s in stu:
            if t in s.test:
                StudentDoc.objects(student_id=s.student_id).update_one(pull__test=t)
                t.delete()
    return redirect(request.referrer)


@bp.route('/import', methods=['GET', 'POST'])
@login_required
def test_import():
    form = ExcelForm()
    if form.validate_on_submit():
        excel = request.files['excel']
        if excel:
            basedir = os.getcwd() + "/website/static/excel/"
            filename = 'test' + str(int(time.time())) + '.xlsx'
            excel.save(os.path.join(basedir, filename))
            workbook = xlrd.open_workbook(os.path.join(basedir, filename))
            sheet_one = workbook.sheet_by_name('Sheet1')
            test_name = sheet_one.row_values(0)[0]
            test_judge = TestScoreDoc.objects(name=test_name).all()
            if len(test_judge) == 0:
                for rownum in range(2, sheet_one.nrows):
                    student = StudentDoc.objects(student_id=str(sheet_one.row_values(rownum)[2])).first()
                    if student != None:
                        for i in range(4, 7):
                            if sheet_one.row_values(rownum)[i] == '':
                                sheet_one.row_values(rownum)[i] = 0
                        test = TestScoreDoc(name=test_name,
                                            score=float(sheet_one.row_values(rownum)[4]),
                                            first_score=float(sheet_one.row_values(rownum)[5]),
                                            second_score=float(sheet_one.row_values(rownum)[6]))
                        test.save()
                        if len(student.test) == 0:
                            student.test = [test]
                            student.save()
                        else:
                            ts = test
                            StudentDoc.objects(student_id=student.student_id).update_one(push__test=ts)
                    else:
                        for i in range(4, 7):
                            if sheet_one.row_values(rownum)[i] == '':
                                sheet_one.row_values(rownum)[i] = 0
                        test = TestScoreDoc(name=test_name,
                                            score=float(sheet_one.row_values(rownum)[4]),
                                            first_score=float(sheet_one.row_values(rownum)[5]),
                                            second_score=float(sheet_one.row_values(rownum)[6]))
                        test.save()
                        classroom = 0
                        if 6171000 < int(sheet_one.row_values(rownum)[2]) < 6171035:
                            classroom = 1
                        elif 6171034 < int(sheet_one.row_values(rownum)[2]) < 6171174:
                            classroom = 2
                        elif 6171073 < int(sheet_one.row_values(rownum)[2]) < 6171110:
                            classroom = 3
                        elif 6171109 < int(sheet_one.row_values(rownum)[2]) < 6171146:
                            classroom = 4
                        stu = StudentDoc(school=sheet_one.row_values(rownum)[3],
                                         real_name=sheet_one.row_values(rownum)[1],
                                         student_id=str(sheet_one.row_values(rownum)[2]),
                                         pet_name=sheet_one.row_values(rownum)[0],
                                         classroom=classroom,
                                         test=[test])
                        stu.save()
                return redirect(url_for('test.test_list'))
            else:
                return redirect(url_for('test.test_list'))
    return tmpl(form=form)


@bp.route('/analysis')
@login_required
def test_analysis_list():
    tests = test_main_display()
    return tmpl(tests=tests)


@bp.route('/analysis/<string:name>')
@login_required
def test_analysis(name):
    tests = test_analysis_display(name)
    return tmpl(tests=tests)


@bp.route('/list/compare')
@login_required
def test_list_compare():
    test = TestScoreDoc.objects().all()
    tests = list(set([h.name for h in test]))
    return tmpl(tests=tests)


@bp.route('/compare/students/<string:name>', methods=['GET', 'POST'])
@login_required
def test_compare_students(name):
    student1 = request.args.get('student1', 'null', type=str)
    student2 = request.args.get('student2', 'null', type=str)
    if student1 != 'null' and student2 != 'null':
        s1 = StudentDoc.objects(student_id=student1).first()
        s2 = StudentDoc.objects(student_id=student2).first()
        return redirect(url_for('test.test_compare_result', s1=s1.student_id, s2=s2.student_id, name=name))
    students = test_match(name)
    return tmpl(students=students, name=name, s1=student1, s2=student2)


@bp.route('/compare/result/<string:name>/<string:s1>/<string:s2>')
@login_required
def test_compare_result(s1, s2, name):
    student1 = StudentDoc.objects(student_id=s1).first()
    student2 = StudentDoc.objects(student_id=s2).first()
    tests = TestScoreDoc.objects(name=name).all()
    stu1, stu2 = (), ()
    for t in tests:
        if t in student1.test:
            index = student1.test.index(t)
            stu1 = (student1.real_name, student1.test[index].score, student1.test[index].first_score,
                    student1.test[index].second_score)

        if t in student2.test:
            index = student2.test.index(t)
            stu2 = (student2.real_name, student2.test[index].score, student2.test[index].first_score,
                    student2.test[index].second_score)

    return tmpl(stu1=stu1, stu2=stu2, name=name, s1=s1, s2=s2)


@bp.route('/detail/<string:name>/<string:num>')
@login_required
def test_display_detail_students(name, num):
    datas = test_detail_students(name, num)
    word = ''
    if int(num) == 0:
        word = '0分学生'
    elif int(num) == 1:
        word = '2分学生'
    elif int(num) == 2:
        word = '4分学生'
    elif int(num) == 3:
        word = '6分学生'
    elif int(num) == 4:
        word = '8分学生'
    elif int(num) == 5:
        word = '10分学生'

    return tmpl(datas=datas, name=name, word=word, num=num)


@bp.route('/detail/export/<string:name>/<string:num>')
@login_required
def test_detail_export(name, num):
    all = test_detail_export_students(name, num)

    word = ''
    if int(num) == 0:
        word = '0分学生'
    elif int(num) == 1:
        word = '2分学生'
    elif int(num) == 2:
        word = '4分学生'
    elif int(num) == 3:
        word = '6分学生'
    elif int(num) == 4:
        word = '8分学生'
    elif int(num) == 5:
        word = '10分学生'
    filename = u'{0}{1}测验成绩表'.format(name, word)

    output = StringIO.StringIO()
    office = Workbook(output)
    worksheet = office.add_worksheet()
    row = [u'学号', u'姓名', u'成绩', u'第一次得分', u'第二次得分']
    worksheet.write_row(0, 0, row)
    for i in xrange(len(all)):
        worksheet.write_row(i + 1, 0, all[i - 1])
    office.close()
    return export_excel(filename, output)