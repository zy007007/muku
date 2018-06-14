# -*- coding:utf-8 -*-
from models.tables import *


def homework_match(homework_name):
    homeworks = HomeworkDoc.objects(name=homework_name).all()
    students = []
    stu = StudentDoc.objects().all()
    for h in homeworks:
        for s in stu:
            if h in s.homework:
                index = s.homework.index(h)
                detail = (s.student_id, s.real_name, s.homework[index])
                students.append(detail)
    return students


def homework_match_one(homework_name, n):
    homeworks = HomeworkDoc.objects(name=homework_name).all()
    students = []

    if len(n) != 8:
        stu = StudentDoc.objects(real_name=n).all()
    else:
        stu = StudentDoc.objects(student_id=n).all()

    for h in homeworks:
        for s in stu:
            if h in s.homework:
                index = s.homework.index(h)
                detail = (s.student_id, s.real_name, s.homework[index])
                students.append(detail)
    return students


def homework_score_analysis(homework_name):
    homeworks = HomeworkDoc.objects(name=homework_name).all()
    less_than_sixty, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred = 0, 0, 0, 0, 0
    for homework in homeworks:
        if homework.score < 60.00:
            less_than_sixty += 1
        elif 60.00 <= homework.score < 70.00:
            sixty_seventy += 1
        elif 70.00 <= homework.score < 80.00:
            seventy_eighty += 1
        elif 80.00 <= homework.score < 90.00:
            eighty_ninety += 1
        elif 90.00 <= homework.score <= 100.00:
            ninety_hundred += 1
    data = [less_than_sixty, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred]
    return data


# 需要得到的数据格式 [(第x周作业, 参与人数， 平均分, 及格率)]
# 每周作业测试每个学生只完成一次
def homework_main_display():
    datas = []
    homework = HomeworkDoc.objects().all()
    homeworks = list(set([h.name for h in homework]))
    for h in homeworks:
        hw = HomeworkDoc.objects(name=h).all()
        stu_num, pass_num, pass_rate, sum_score, aver_score = 0, 0, 0.0, 0.0, 0.0
        for w in hw:
            stu_num += 1
            sum_score += w.score
            if w.score >= 60.00:
                pass_num += 1
        aver_score = format(float(sum_score)/float(stu_num), '.2f')
        pass_rate = format(float(pass_num)/float(stu_num), '.2f')
        datas.append((h, stu_num, aver_score, pass_rate))
    result = sorted(datas, key=lambda x:x[2], reverse=True)
    return result


def homework_analysis_display(name):
    datas = []
    homework = HomeworkDoc.objects(name=name).all()
    homeworks = list(set([h.name for h in homework]))
    for h in homeworks:
        hs = HomeworkDoc.objects(name=h).all()
        less_than_sixty, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred = 0, 0, 0, 0, 0
        for hh in hs:
            if hh.score < 60.00:
                less_than_sixty += 1
            elif 60.00 <= hh.score < 70.00:
                sixty_seventy += 1
            elif 70.00 <= hh.score < 80.00:
                seventy_eighty += 1
            elif 80.00 <= hh.score < 90.00:
                eighty_ninety += 1
            elif 90.00 <= hh.score <= 100.00:
                ninety_hundred += 1
        datas.append((h, less_than_sixty, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred))
    return datas


def homework_detail_students(name, num):
    homeworks = HomeworkDoc.objects(name=name).all()
    students = []
    stu = StudentDoc.objects().all()
    if int(num) == 0:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if s.homework[index].score < 60.00:
                        detail = (s.student_id, s.real_name, s.homework[index])
                        students.append(detail)

    elif int(num) == 1:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if 60.00 <= s.homework[index].score < 70.00:
                        detail = (s.student_id, s.real_name, s.homework[index])
                        students.append(detail)

    elif int(num) == 2:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if 70.00 <= s.homework[index].score < 80.00:
                        detail = (s.student_id, s.real_name, s.homework[index])
                        students.append(detail)
    elif int(num) == 3:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if 80.00 <= s.homework[index].score < 90.00:
                        detail = (s.student_id, s.real_name, s.homework[index])
                        students.append(detail)
    elif int(num) == 4:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if 90.00 <= s.homework[index].score <= 100.00:
                        detail = (s.student_id, s.real_name, s.homework[index])
                        students.append(detail)
    return students


def homework_detail_export_students(name, num):
    homeworks = HomeworkDoc.objects(name=name).all()
    students = []
    stu = StudentDoc.objects().all()
    if int(num) == 0:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if s.homework[index].score < 60.00:
                        detail = (s.student_id, s.real_name, s.homework[index].score)
                        students.append(detail)

    elif int(num) == 1:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if 60.00 <= s.homework[index].score < 70.00:
                        detail = (s.student_id, s.real_name, s.homework[index].score)
                        students.append(detail)

    elif int(num) == 2:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if 70.00 <= s.homework[index].score < 80.00:
                        detail = (s.student_id, s.real_name, s.homework[index].score)
                        students.append(detail)
    elif int(num) == 3:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if 80.00 <= s.homework[index].score < 90.00:
                        detail = (s.student_id, s.real_name, s.homework[index].score)
                        students.append(detail)
    elif int(num) == 4:
        for t in homeworks:
            for s in stu:
                if t in s.homework:
                    index = s.homework.index(t)
                    if 90.00 <= s.homework[index].score <= 100.00:
                        detail = (s.student_id, s.real_name, s.homework[index].score)
                        students.append(detail)
    return students

