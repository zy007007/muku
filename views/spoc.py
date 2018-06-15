# -*- coding:utf-8 -*-
import time, os, xlrd, urllib2, StringIO
from flask import Flask, flash, make_response
from flask import render_template, redirect, url_for, Blueprint, request
from heplers.override import tmpl
from heplers.utils import export_excel
from flask_login import login_required, current_user, logout_user
from models.user import UserModel
from models.tables import StudentDoc, SpocScoreDoc
from forms.excel import ExcelForm
from xlsxwriter.workbook import Workbook
from heplers.spoc import spoc_match, spoc_analysis_display_one, \
    spoc_look_score, spoc_look_num, spoc_detail_students, \
    spoc_main_display, spoc_nums_long, \
    spoc_detail_export_students, spoc_match_one, \
    spoc_standard, spoc_standard_export, spoc_analysis_display_grade, \
    spoc_look_score_grade, spoc_look_num_grade, spoc_nums_long_grade
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


__all__ = ['bp']

bp = Blueprint('spoc', __name__, url_prefix='/spoc')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.index'))


@bp.route('/list')
@login_required
def spoc_list():
    spoc = SpocScoreDoc.objects().all()
    spocs = list(set([h.name for h in spoc]))
    return tmpl(spocs=spocs)


@bp.route('/detail/<string:name>')
@login_required
def spoc_detail(name):
    keyword = request.args.get('keyword', 'null', type=str)
    stu = None
    if keyword != 'null':
        stu = spoc_match_one(name, keyword)
    students = spoc_match(name)
    return tmpl(students=students, name=name, stu=stu)


@bp.route('/delete/<string:name>')
@login_required
def spoc_delete(name):
    spoc = SpocScoreDoc.objects(name=name).all()
    stu = StudentDoc.objects().all()
    for t in spoc:
        for s in stu:
            if t in s.spoc:
                StudentDoc.objects(student_id=s.student_id).update_one(pull__spoc=t)
                t.delete()
    return redirect(request.referrer)


@bp.route('/import', methods=['GET', 'POST'])
@login_required
def spoc_import():
    form = ExcelForm()
    if form.validate_on_submit():
        excel = request.files['excel']
        if excel:
            basedir = os.getcwd() + "/website/static/excel/"
            filename = 'spoc' + str(int(time.time())) + '.xlsx'
            excel.save(os.path.join(basedir, filename))
            workbook = xlrd.open_workbook(os.path.join(basedir, filename))
            sheet_one = workbook.sheet_by_name('Sheet1')
            spoc_name = sheet_one.row_values(0)[0]
            spoc_judge = SpocScoreDoc.objects(name=spoc_name).all()
            if len(spoc_judge) == 0:
                for rownum in range(2, sheet_one.nrows):
                    student = StudentDoc.objects(student_id=str(sheet_one.row_values(rownum)[2])).first()
                    if student != None:
                        spoc = SpocScoreDoc(name=spoc_name,
                                            spoc_score=float(sheet_one.row_values(rownum)[4]),
                                            look_one_num=sheet_one.row_values(rownum)[6],
                                            look_times_num=sheet_one.row_values(rownum)[7],
                                            look_sum_time=sheet_one.row_values(rownum)[8],
                                            titles=sheet_one.row_values(rownum)[9],
                                            reviews_reply=sheet_one.row_values(rownum)[10]
                                            )
                        spoc.save()
                        if len(student.spoc) == 0:
                            student.spoc = [spoc]
                            student.save()
                        else:
                            hw = spoc
                            StudentDoc.objects(student_id=student.student_id).update_one(push__spoc=hw)
                    else:
                        spoc = SpocScoreDoc(name=spoc_name,
                                            spoc_score=float(sheet_one.row_values(rownum)[4]),
                                            look_one_num=sheet_one.row_values(rownum)[6],
                                            look_times_num=sheet_one.row_values(rownum)[7],
                                            look_sum_time=sheet_one.row_values(rownum)[8],
                                            titles=sheet_one.row_values(rownum)[9],
                                            reviews_reply=sheet_one.row_values(rownum)[10]
                                            )
                        spoc.save()
                        classroom = 0
                        if 6171000 < int(sheet_one.row_values(rownum)[2]) < 6171035:
                            classroom = 1
                        elif 6171034 < int(sheet_one.row_values(rownum)[2]) < 6171174:
                            classroom = 2
                        elif 6171073 < int(sheet_one.row_values(rownum)[2]) < 6171110:
                            classroom = 3
                        elif 6171109 < int(sheet_one.row_values(rownum)[2]) < 6171146:
                            classroom = 4
                        stu = StudentDoc(school=sheet_one.row_values(rownum)[0],
                                         real_name=sheet_one.row_values(rownum)[1],
                                         student_id=str(sheet_one.row_values(rownum)[2]),
                                         pet_name=sheet_one.row_values(rownum)[0],
                                             classroom=classroom,
                                         spoc=[spoc])
                        stu.save()
                return redirect(url_for('spoc.spoc_list'))
            else:
                flash(u'已导入此成绩')
                return redirect(url_for('spoc.spoc_list'))
    return tmpl(form=form)


@bp.route('/analysis')
@login_required
def spoc_analysis_list():
    spocs = spoc_main_display()
    return tmpl(spocs=spocs)


@bp.route('/analysis/<string:name>')
@login_required
def spoc_analysis(name):
    grade = request.args.get('grade', 'null', type=str)
    if grade != 'null':
        spocs = spoc_analysis_display_grade(name, grade)
        spoc_look = spoc_look_score_grade(name, grade)
        look_times = spoc_look_num_grade(name, grade)
        nums_long = spoc_nums_long_grade(name, grade)
    else:
        spocs = spoc_analysis_display_one(name)
        spoc_look = spoc_look_score(name)
        look_times = spoc_look_num(name)
        nums_long = spoc_nums_long(name)
    return tmpl(spocs=spocs, spoc_look=spoc_look, look_times=look_times, nums_long=nums_long, name=name, grade=grade)


@bp.route('/list/compare')
@login_required
def spoc_list_compare():
    spoc = SpocScoreDoc.objects().all()
    spocs = list(set([h.name for h in spoc]))
    return tmpl(spocs=spocs)


@bp.route('/compare/students/<string:name>', methods=['GET', 'POST'])
@login_required
def spoc_compare_students(name):
    student1 = request.args.get('student1', 'null', type=str)
    student2 = request.args.get('student2', 'null', type=str)
    if student1 != 'null' and student2 != 'null':
        s1 = StudentDoc.objects(student_id=student1).first()
        s2 = StudentDoc.objects(student_id=student2).first()
        return redirect(url_for('spoc.spoc_compare_result', s1=s1.student_id, s2=s2.student_id, name=name))
    students = spoc_match(name)
    return tmpl(students=students, name=name, s1=student1, s2=student2)


@bp.route('/compare/result/<string:name>/<string:s1>/<string:s2>')
@login_required
def spoc_compare_result(s1, s2, name):
    student1 = StudentDoc.objects(student_id=s1).first()
    student2 = StudentDoc.objects(student_id=s2).first()
    spocs = SpocScoreDoc.objects(name=name).all()
    stu1, stu2 = (), ()
    for t in spocs:
        if t in student1.spoc:
            index = student1.spoc.index(t)
            stu1 = (student1.real_name, student1.spoc[index].spoc_score, student1.spoc[index].look_one_num,
                    student1.spoc[index].look_times_num, student1.spoc[index].look_sum_time,
                    student1.spoc[index].titles, student1.spoc[index].reviews_reply)

        if t in student2.spoc:
            index = student2.spoc.index(t)
            stu2 = (student2.real_name, student2.spoc[index].spoc_score, student2.spoc[index].look_one_num,
                    student2.spoc[index].look_times_num, student2.spoc[index].look_sum_time,
                    student2.spoc[index].titles, student2.spoc[index].reviews_reply)

    return tmpl(stu1=stu1, stu2=stu2, name=name, s1=s1, s2=s2)


@bp.route('/detail/<string:name>/<string:classroom>/<string:num>')
@login_required
def spoc_display_detail_students(name, num, classroom):
    datas = spoc_detail_students(name, num, classroom)
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
def spoc_detail_export(name, num):
    all = spoc_detail_export_students(name, num)

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
    filename = u'{0}{1}spoc成绩表'.format(name, word)

    output = StringIO.StringIO()
    office = Workbook(output)
    worksheet = office.add_worksheet()
    row = [u'学号', u'姓名', u'spoc成绩', u'视频观看个数', u'视频观看次数', u'视频观看时长' ,u'讨论区主题数', u'讨论区评论数+回复数']
    worksheet.write_row(0, 0, row)
    for i in xrange(len(all)):
        worksheet.write_row(i + 1, 0, all[i - 1])
    office.close()
    return export_excel(filename, output)


@bp.route('/tree/<string:name>')
@login_required
def spoc_tree(name):
    standard = request.args.get('standard', 'null', type=str)
    stu = None
    if standard != 'null':
        stu = spoc_standard(standard, name)
    students = spoc_match(name)
    return tmpl(students=students, name=name, stu=stu, standard=standard)


@bp.route('/tree/export/<string:name>/<string:standard>')
@login_required
def spoc_tree_export(name, standard):
    student = spoc_standard_export(standard, name)
    labels = ['score', 'nums', 'longs']

    from sklearn import tree
    from sklearn.cross_validation import train_test_split

    FeatureSet = []
    Label = []
    for i in student:
        FeatureSet.append(i[:-1])
        Label.append(i[-1])
    X_train, X_test, y_train, y_test = train_test_split(FeatureSet, Label, random_state=1)

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)

    with open("./static/image/result.dot", 'w') as f:
        f = tree.export_graphviz(clf, out_file=f)
    import os
    os.unlink('./static/image/result.dot')
    from sklearn.externals.six import StringIO
    import pydot
    dot_data = StringIO()

    target_name = ['A', 'B', 'C']

    tree.export_graphviz(clf, out_file=dot_data, class_names=target_name, feature_names=labels,
                         filled=True, rounded=True, special_characters=True)
    graph = pydot.graph_from_dot_data(dot_data.getvalue())
    graph[0].write_pdf("./static/image/result.pdf")

    return tmpl(name=name, standard=standard)
