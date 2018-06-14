# -*- coding:utf-8 -*-
from models.tables import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def student_analysis_temp():
    stus = StudentDoc.objects.all()
    datas = []
    for s in stus:
        homework1, homework2, homework3, homework4, homework6, test1, test2, test3, test4, test51, test52, test6 \
            = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        for t in s.test:
            test = TestScoreDoc.objects(id=t.id).first()
            if test != None:
                if '第一周测试' in test.name:
                    test1 = test.score
                elif '第二周测试' in test.name:
                    test2 = test.score
                elif '第三周测试' in test.name:
                    test3 = test.score
                elif '第四周测试' in test.name:
                    test4 = test.score
                elif '第五周测试（一）' in test.name:
                    test51 = test.score
                elif '第五周测试（二）' in test.name:
                    test52 = test.score
                elif '第六周测试' in test.name:
                    test6 = test.score

        for h in s.homework:
            homework = HomeworkDoc.objects(id=h.id).first()
            if homework != None:
                if '第一' in homework.name:
                    homework1 = homework.score
                elif '第二' in homework.name:
                    homework2 = homework.score
                elif '第三' in homework.name:
                    homework3 = homework.score
                elif '第四' in homework.name:
                    homework4 = homework.score
                elif '第六' in homework.name:
                    homework6 = homework.score

        sum_homework = homework1 + homework6 + homework4 + homework2 + homework3
        sum_test = test1 + test2 + test3 + test4 + test51 + test52 + test6
        sum_ht = sum_homework + sum_test*10

        detail = (s.student_id, s.real_name, homework1, homework2, homework3, homework4, homework6,
                  test1, test2, test3, test4, test51, test52, test6, sum_homework, sum_test, sum_ht)
        datas.append(detail)
    result = sorted(datas, key=lambda x:x[0], reverse=True)
    return result


def student_analysis_temps(ttt, hhh):
    stus = StudentDoc.objects.all()
    datas = []
    for s in stus:
        homework1, homework2, homework3, homework4, homework6, test1, test2, test3, test4, test51, test52, test6 \
            = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        for t in s.test:
            test = TestScoreDoc.objects(id=t.id).first()
            if test != None:
                if '第一周测试' in test.name:
                    test1 = test.score
                elif '第二周测试' in test.name:
                    test2 = test.score
                elif '第三周测试' in test.name:
                    test3 = test.score
                elif '第四周测试' in test.name:
                    test4 = test.score
                elif '第五周测试（一）' in test.name:
                    test51 = test.score
                elif '第五周测试（二）' in test.name:
                    test52 = test.score
                elif '第六周测试' in test.name:
                    test6 = test.score

        for h in s.homework:
            homework = HomeworkDoc.objects(id=h.id).first()
            if homework != None:
                if '第一' in homework.name:
                    homework1 = homework.score
                elif '第二' in homework.name:
                    homework2 = homework.score
                elif '第三' in homework.name:
                    homework3 = homework.score
                elif '第四' in homework.name:
                    homework4 = homework.score
                elif '第六' in homework.name:
                    homework6 = homework.score

        sum_homework = homework1 + homework6 + homework4 + homework2 + homework3
        sum_test = test1 + test2 + test3 + test4 + test51 + test52 + test6
        sum_ht = sum_homework + sum_test * 10
        H, T = float(hhh), float(ttt)
        sum_ht_quan = sum_homework*H + sum_test*T*10

        detail = (s.student_id, s.real_name, homework1, homework2, homework3, homework4, homework6,
                  test1, test2, test3, test4, test51, test52, test6, sum_homework, sum_test, sum_ht, sum_ht_quan)
        datas.append(detail)
    result = sorted(datas, key=lambda x: x[0], reverse=True)
    return result


def student_detail(id):
    s = StudentDoc.objects.get_or_404(id=id)
    homework1, homework2, homework3, homework4, homework6, test1, test2, test3, test4, test51, test52, test6 \
        = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for t in s.test:
        test = TestScoreDoc.objects(id=t.id).first()
        if test != None:
            if '第一周测试' in test.name:
                test1 = test.score
            elif '第二周测试' in test.name:
                test2 = test.score
            elif '第三周测试' in test.name:
                test3 = test.score
            elif '第四周测试' in test.name:
                test4 = test.score
            elif '第五周测试（一）' in test.name:
                test51 = test.score
            elif '第五周测试（二）' in test.name:
                test52 = test.score
            elif '第六周测试' in test.name:
                test6 = test.score

    for h in s.homework:
        homework = HomeworkDoc.objects(id=h.id).first()
        if homework != None:
            if '第一' in homework.name:
                homework1 = homework.score
            elif '第二' in homework.name:
                homework2 = homework.score
            elif '第三' in homework.name:
                homework3 = homework.score
            elif '第四' in homework.name:
                homework4 = homework.score
            elif '第六' in homework.name:
                homework6 = homework.score

    datas = (s.student_id, s.real_name, homework1, homework2, homework3, homework4, homework6,
              test1, test2, test3, test4, test51, test52, test6)
    return datas
