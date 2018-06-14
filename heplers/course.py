# -*- coding:utf-8 -*-
from models.tables import *


def course_test_display(name):
    courses = CourseDoc.objects(name=name).all()
    course = list(set([c.name for c in courses]))
    datas = []
    first, second, third, fourth, fifth, sixth = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for c in course:
        temp = CourseDoc.objects(name=c, classify='单元测验').all()
        for t in temp:
            if '第一' in t.title:
                first = t.aver_score
            elif '第二' in t.title:
                second = t.aver_score
            elif '第三' in t.title:
                third = t.aver_score
            elif '第四' in t.title:
                fourth = t.aver_score
            elif '第五' in t.title:
                fifth = t.aver_score
            elif '第六' in t.title:
                sixth = t.aver_score
        datas.append((c, first, second, third, fourth, fifth, sixth))
    return datas


def course_homework_display(name):
    courses = CourseDoc.objects(name=name).all()
    course = list(set([c.name for c in courses]))
    datas = []
    first, second, third, fourth, fifth, sixth = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for c in course:
        temp = CourseDoc.objects(name=c, classify='单元作业').all()
        for t in temp:
            if '第一' in t.title:
                first = t.aver_score
            elif '第二' in t.title:
                second = t.aver_score
            elif '第三' in t.title:
                third = t.aver_score
            elif '第四' in t.title:
                fourth = t.aver_score
            elif '第五' in t.title:
                fifth = t.aver_score
            elif '第六' in t.title:
                sixth = t.aver_score
        datas.append((c, first, second, third, fourth, fifth, sixth))
    return datas


def course_exam_display(name):
    courses = CourseDoc.objects(name=name).all()
    course = list(set([c.name for c in courses]))
    datas = []
    first, second, third, fourth = 0.0, 0.0, 0.0, 0.0
    for c in course:
        temp = CourseDoc.objects(name=c, classify='考试').all()
        for t in temp:
            if '第一' in t.title:
                first = t.aver_score
            elif '期中' in t.title:
                second = t.aver_score
            elif '第二' in t.title:
                third = t.aver_score
            elif '期末' in t.title:
                fourth = t.aver_score
        datas.append((c, first, second, third, fourth))
    return datas


def course_main_display():
    course = CourseDoc.objects().all()
    courses = list(set(s.name for s in course))
    return courses
