# -*- coding:utf-8 -*-
import time, os, xlrd, urllib2, StringIO
from flask import Flask
from flask import render_template, redirect, url_for, Blueprint, request
from heplers.override import tmpl
from flask_login import login_required, current_user, logout_user
from models.user import UserModel
from models.tables import StudentDoc, HomeworkDoc
from forms.excel import ExcelForm
from xlsxwriter.workbook import Workbook
from heplers.utils import export_excel
from heplers.homework import homework_match, \
    homework_analysis_display, homework_main_display, homework_detail_students, homework_detail_export_students, homework_match_one
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


__all__ = ['bp']

bp = Blueprint('homework', __name__, url_prefix='/homework')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.index'))


@bp.route('/list')
@login_required
def homework_list():
    user = current_user.name
    homework = HomeworkDoc.objects().all()
    homeworks = list(set([h.name for h in homework]))
    return tmpl(user=user, homeworks=homeworks)


@bp.route('/detail/<string:name>')
@login_required
def homework_detail(name):
    keyword = request.args.get('keyword', 'null', type=str)
    stu = None
    if keyword != 'null':
        stu = homework_match_one(name, keyword)
    students = homework_match(name)
    return tmpl(students=students, name=name, stu=stu)


@bp.route('/delete/<string:name>')
@login_required
def homework_delete(name):
    homework = HomeworkDoc.objects(name=name).all()
    stu = StudentDoc.objects().all()
    for t in homework:
        for s in stu:
            if t in s.homework:
                StudentDoc.objects(student_id=s.student_id).update_one(pull__homework=t)
                t.delete()
    return redirect(request.referrer)


@bp.route('/import', methods=['GET', 'POST'])
@login_required
def homework_import():
    form = ExcelForm()
    if form.validate_on_submit():
        excel = request.files['excel']
        if excel:
            basedir = os.getcwd() + "/website/static/excel/"
            filename = 'home' + str(int(time.time())) + '.xlsx'
            excel.save(os.path.join(basedir, filename))
            workbook = xlrd.open_workbook(os.path.join(basedir, filename))
            sheet_one = workbook.sheet_by_name('Sheet1')
            homework_name = sheet_one.row_values(0)[0]
            homework_judge = HomeworkDoc.objects(name=homework_name).all()
            if len(homework_judge) == 0:
                for rownum in range(2, sheet_one.nrows):
                    student = StudentDoc.objects(student_id=str(sheet_one.row_values(rownum)[2])).first()
                    if student != None:
                        for i in range(5, 11):
                            if sheet_one.row_values(rownum)[i] == None:
                                sheet_one.row_values(rownum)[i] = 0
                        mutual = [sheet_one.row_values(rownum)[5], sheet_one.row_values(rownum)[6],
                                  sheet_one.row_values(rownum)[7], sheet_one.row_values(rownum)[8],
                                  sheet_one.row_values(rownum)[9], sheet_one.row_values(rownum)[10]]
                        homework = HomeworkDoc(name=homework_name,
                                               score=float(sheet_one.row_values(rownum)[4]),
                                               mutual=mutual
                                               )
                        homework.save()
                        if len(student.homework) == 0:
                            student.homework = [homework]
                            student.save()
                        else:
                            hw = homework
                            StudentDoc.objects(student_id=student.student_id).update_one(push__homework=hw)
                    else:
                        for i in range(5, 11):
                            if sheet_one.row_values(rownum)[i] == None:
                                sheet_one.row_values(rownum)[i] = 0
                        mutual = [sheet_one.row_values(rownum)[5], sheet_one.row_values(rownum)[6],
                                  sheet_one.row_values(rownum)[7], sheet_one.row_values(rownum)[8],
                                  sheet_one.row_values(rownum)[9], sheet_one.row_values(rownum)[10]]
                        homework = HomeworkDoc(name=homework_name,
                                               score=float(sheet_one.row_values(rownum)[4]),
                                               mutual=mutual
                                               )
                        homework.save()
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
                                         homework=[homework])
                        stu.save()
                return redirect(url_for('homework.homework_list'))
            else:
                return redirect(url_for('homework.homework_list'))
    return tmpl(form=form)


@bp.route('/analysis')
@login_required
def homework_analysis_list():
    homeworks = homework_main_display()
    return tmpl(homeworks=homeworks)


@bp.route('/analysis/<string:name>')
@login_required
def homework_analysis(name):
    homeworks = homework_analysis_display(name)
    return tmpl(homeworks=homeworks)


@bp.route('/list/compare')
@login_required
def homework_list_compare():
    homework = HomeworkDoc.objects().all()
    homeworks = list(set([h.name for h in homework]))
    return tmpl(homeworks=homeworks)


@bp.route('/compare/students/<string:name>', methods=['GET', 'POST'])
@login_required
def homework_compare_students(name):
    student1 = request.args.get('student1', 'null', type=str)
    student2 = request.args.get('student2', 'null', type=str)
    if student1 != 'null' and student2 != 'null':
        s1 = StudentDoc.objects(student_id=student1).first()
        s2 = StudentDoc.objects(student_id=student2).first()
        return redirect(url_for('homework.homework_compare_result', s1=s1.student_id, s2=s2.student_id, name=name))
    students = homework_match(name)
    return tmpl(students=students, name=name, s1=student1, s2=student2)


@bp.route('/compare/result/<string:name>/<string:s1>/<string:s2>')
@login_required
def homework_compare_result(s1, s2, name):
    student1 = StudentDoc.objects(student_id=s1).first()
    student2 = StudentDoc.objects(student_id=s2).first()
    homeworks = HomeworkDoc.objects(name=name).all()
    stu1, stu2 = (), ()
    for t in homeworks:
        if t in student1.homework:
            index = student1.homework.index(t)
            stu1 = (student1.real_name, student1.homework[index].score, student1.homework[index].mutual[0],
                    student1.homework[index].mutual[1], student1.homework[index].mutual[2],
                    student1.homework[index].mutual[3], student1.homework[index].mutual[4],
                    student1.homework[index].mutual[5])

        if t in student2.homework:
            index = student2.homework.index(t)
            stu2 = (student2.real_name, student2.homework[index].score, student2.homework[index].mutual[0],
                    student2.homework[index].mutual[1], student2.homework[index].mutual[2],
                    student2.homework[index].mutual[3], student2.homework[index].mutual[4],
                    student2.homework[index].mutual[5])

    return tmpl(stu1=stu1, stu2=stu2, name=name, s1=s1, s2=s2)


@bp.route('/detail/<string:name>/<string:num>')
@login_required
def homework_display_detail_students(name, num):
    datas = homework_detail_students(name, num)
    word = ''
    if int(num) == 0:
        word = '<60分学生'
    elif int(num) == 1:
        word = '60-70分学生'
    elif int(num) == 2:
        word = '70-80分学生'
    elif int(num) == 3:
        word = '80-90分学生'
    elif int(num) == 4:
        word = '90-100分学生'

    return tmpl(datas=datas, name=name, word=word, num=num)


@bp.route('/detail/export/<string:name>/<string:num>')
@login_required
def homework_detail_export(name, num):
    all = homework_detail_export_students(name, num)

    word = ''
    if int(num) == 0:
        word = '<60分学生'
    elif int(num) == 1:
        word = '60-70分学生'
    elif int(num) == 2:
        word = '70-80分学生'
    elif int(num) == 3:
        word = '80-90分学生'
    elif int(num) == 4:
        word = '90-100分学生'
    filename = u'{0}{1}作业成绩表'.format(name, word)

    output = StringIO.StringIO()
    office = Workbook(output)
    worksheet = office.add_worksheet()
    row = [u'学号', u'姓名', u'成绩']
    worksheet.write_row(0, 0, row)
    for i in xrange(len(all)):
        worksheet.write_row(i + 1, 0, all[i - 1])
    office.close()
    return export_excel(filename, output)