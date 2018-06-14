# -*- coding:utf-8 -*-
from models.tables import *


def test_match(name):
    tests = TestScoreDoc.objects(name=name).all()
    students = []
    stu = StudentDoc.objects().all()
    for t in tests:
        for s in stu:
            if t in s.test:
                index = s.test.index(t)
                detail = (s.student_id, s.real_name, s.test[index])
                students.append(detail)
    return students


def test_match_one(name, n):
    tests = TestScoreDoc.objects(name=name).all()
    students = []

    if len(n) != 8:
        stu = StudentDoc.objects(real_name=n).all()
    else:
        stu = StudentDoc.objects(student_id=n).all()

    for t in tests:
        for s in stu:
            if t in s.test:
                index = s.test.index(t)
                detail = (s.student_id, s.real_name, s.test[index])
                students.append(detail)
    return students


def test_main_display():
    datas = []
    test = TestScoreDoc.objects().all()
    tests = list(set(t.name for t in test))
    for tt in tests:
        ts = TestScoreDoc.objects(name=tt).all()
        stu_num, pass_num, pass_rate, sum_score, aver_score = 0, 0, 0.0, 0.0, 0.0
        for t in ts:
            stu_num += 1
            sum_score += t.score
            if t.score >= 6.00:
                pass_num += 1
        aver_score = format(float(sum_score) / float(stu_num), '.2f')
        pass_rate = format(float(pass_num) / float(stu_num), '.2f')
        datas.append((tt, stu_num, aver_score, pass_rate))
    result = sorted(datas, key=lambda x:x[2], reverse=True)
    return result


def test_analysis_display(name):
    datas = []
    test = TestScoreDoc.objects(name=name).all()
    tests = list(set([h.name for h in test]))
    for h in tests:
        hs = TestScoreDoc.objects(name=h).all()
        less_than_sixty, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred, two = 0, 0, 0, 0, 0, 0
        for hh in hs:
            if hh.score < 2.00:
                less_than_sixty += 1
            elif 2.00 <= hh.score < 4.00:
                two += 1
            elif 4.00 <= hh.score < 6.00:
                sixty_seventy += 1
            elif 6.00 <= hh.score < 8.00:
                seventy_eighty += 1
            elif 8.00 <= hh.score < 10.00:
                eighty_ninety += 1
            elif 10.00 <= hh.score:
                ninety_hundred += 1
        datas.append((h, less_than_sixty, two, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred))
    return datas


def test_detail_students(name, num):
    tests = TestScoreDoc.objects(name=name).all()
    students = []
    stu = StudentDoc.objects().all()
    if int(num) == 0:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if s.test[index].score < 2.00:
                        detail = (s.student_id, s.real_name, s.test[index])
                        students.append(detail)

    elif int(num) == 1:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 2.00 <= s.test[index].score < 4.00:
                        detail = (s.student_id, s.real_name, s.test[index])
                        students.append(detail)

    elif int(num) == 2:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 4.00 <= s.test[index].score < 6.00:
                        detail = (s.student_id, s.real_name, s.test[index])
                        students.append(detail)
    elif int(num) == 3:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 6.00 <= s.test[index].score < 8.00:
                        detail = (s.student_id, s.real_name, s.test[index])
                        students.append(detail)
    elif int(num) == 4:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 8.00 <= s.test[index].score < 10.00:
                        detail = (s.student_id, s.real_name, s.test[index])
                        students.append(detail)

    elif int(num) == 5:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 10.00 <= s.test[index].score:
                        detail = (s.student_id, s.real_name, s.test[index])
                        students.append(detail)

    return students


def test_detail_export_students(name, num):
    tests = TestScoreDoc.objects(name=name).all()
    students = []
    stu = StudentDoc.objects().all()
    if int(num) == 0:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if s.test[index].score < 2.00:
                        detail = (s.student_id, s.real_name, s.test[index].score,
                                  s.test[index].first_score, s.test[index].second_score)
                        students.append(detail)

    elif int(num) == 1:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 2.00 <= s.test[index].score < 4.00:
                        detail = (s.student_id, s.real_name, s.test[index].score,
                                  s.test[index].first_score, s.test[index].second_score)
                        students.append(detail)

    elif int(num) == 2:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 4.00 <= s.test[index].score < 6.00:
                        detail = (s.student_id, s.real_name, s.test[index].score,
                                  s.test[index].first_score, s.test[index].second_score)
                        students.append(detail)
    elif int(num) == 3:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 6.00 <= s.test[index].score < 8.00:
                        detail = (s.student_id, s.real_name, s.test[index].score,
                                  s.test[index].first_score, s.test[index].second_score)
                        students.append(detail)
    elif int(num) == 4:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 8.00 <= s.test[index].score < 10.00:
                        detail = (s.student_id, s.real_name, s.test[index].score,
                                  s.test[index].first_score, s.test[index].second_score)
                        students.append(detail)

    elif int(num) == 5:
        for t in tests:
            for s in stu:
                if t in s.test:
                    index = s.test.index(t)
                    if 10.00 <= s.test[index].score:
                        detail = (s.student_id, s.real_name, s.test[index].score,
                                  s.test[index].first_score, s.test[index].second_score)
                        students.append(detail)

    return students