# -*- coding:utf-8 -*-
from models.tables import *


def spoc_match(name):
    spocs = SpocScoreDoc.objects(name=name).all()
    students = []
    stu = StudentDoc.objects().all()
    for t in spocs:
        for s in stu:
            if t in s.spoc:
                index = s.spoc.index(t)
                detail = (s.student_id, s.real_name, s.spoc[index])
                students.append(detail)
    return students


def spoc_match_one(name, stu):
    spocs = SpocScoreDoc.objects(name=name).all()
    students = []

    if len(stu) != 8:
        stu = StudentDoc.objects(real_name=stu).all()
    else:
        stu = StudentDoc.objects(student_id=stu).all()

    for t in spocs:
        for s in stu:
            if t in s.spoc:
                index = s.spoc.index(t)
                detail = (s.student_id, s.real_name, s.spoc[index])
                students.append(detail)
    return students


def spoc_standard(standard, n):
    spocs = SpocScoreDoc.objects(name=n).all()
    stu = StudentDoc.objects().all()

    aver_times_aggregate, aver_long_aggregate = [], []
    students = []
    if standard == '1':
        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    aver_times_aggregate.append(s.spoc[index].look_one_num)
                    aver_long_aggregate.append(s.spoc[index].look_sum_time)

        sum_times = sum(aver_times_aggregate)
        aver_times = sum_times / len(aver_times_aggregate)

        sum_long = sum(aver_long_aggregate)
        aver_lone = sum_long / len(aver_long_aggregate)

        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)

                    if s.spoc[index].spoc_score < 60.00:
                        score = '不及格'
                    elif 60.00 <= s.spoc[index].spoc_score < 70.00:
                        score = '及格'
                    elif 70.00 <= s.spoc[index].spoc_score < 80.00:
                        score = '良好'
                    else:
                        score = '优秀'

                    if s.spoc[index].look_one_num >= aver_times:
                        at = '多'
                    else:
                        at = '少'

                    if s.spoc[index].look_sum_time >= aver_lone:
                        al = '长'
                    else:
                        al = '短'

                    rank = judge_ABC(score, at, al)

                    detail = (s.student_id, s.real_name,
                              s.spoc[index].spoc_score, score,
                              s.spoc[index].look_one_num, at,
                              s.spoc[index].look_sum_time, al,
                              rank
                              )
                    students.append(detail)
    elif standard == '2':
        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    aver_times_aggregate.append(s.spoc[index].look_one_num)
                    aver_long_aggregate.append(s.spoc[index].look_sum_time)

        middle_times = len(aver_times_aggregate) / 2
        mt = aver_times_aggregate[middle_times]

        middle_long = len(aver_long_aggregate) / 2
        ml = aver_long_aggregate[middle_long]

        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)

                    if s.spoc[index].spoc_score < 60.00:
                        score = '不及格'
                    elif 60.00 <= s.spoc[index].spoc_score < 70.00:
                        score = '及格'
                    elif 70.00 <= s.spoc[index].spoc_score < 80.00:
                        score = '良好'
                    else:
                        score = '优秀'

                    if s.spoc[index].look_one_num >= mt:
                        at = '多'
                    else:
                        at = '少'

                    if s.spoc[index].look_sum_time >= ml:
                        al = '长'
                    else:
                        al = '短'

                    rank = judge_ABC(score, at, al)

                    detail = (s.student_id, s.real_name,
                              s.spoc[index].spoc_score, score,
                              s.spoc[index].look_one_num, at,
                              s.spoc[index].look_sum_time, al,
                              rank
                              )
                    students.append(detail)

    return students


def spoc_standard_export(standard, n):
    spocs = SpocScoreDoc.objects(name=n).all()
    stu = StudentDoc.objects().all()

    aver_times_aggregate, aver_long_aggregate = [], []
    students = []
    if standard == '1':
        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    aver_times_aggregate.append(s.spoc[index].look_one_num)
                    aver_long_aggregate.append(s.spoc[index].look_sum_time)

        sum_times = sum(aver_times_aggregate)
        aver_times = sum_times / len(aver_times_aggregate)

        sum_long = sum(aver_long_aggregate)
        aver_long = sum_long / len(aver_long_aggregate)

        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    #
                    # score = judge_score(s.spoc[index].spoc_score)
                    # at = judge_num(s.spoc[index].spoc_score, aver_times)
                    # al = judge_long(s.spoc[index].spoc_score, aver_long)
                    if s.spoc[index].spoc_score < 60.00:
                        score = '不及格'
                    elif 60.00 <= s.spoc[index].spoc_score < 70.00:
                        score = '及格'
                    elif 70.00 <= s.spoc[index].spoc_score < 80.00:
                        score = '良好'
                    else:
                        score = '优秀'

                    if s.spoc[index].look_one_num >= aver_times:
                        at = '多'
                    else:
                        at = '少'

                    if s.spoc[index].look_sum_time >= aver_long:
                        al = '长'
                    else:
                        al = '短'

                    rank = judge_ABC(score, at, al)

                    detail = (
                              s.spoc[index].spoc_score,
                              s.spoc[index].look_one_num,
                              s.spoc[index].look_sum_time,
                              rank
                              )
                    students.append(detail)
    elif standard == '2':
        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    aver_times_aggregate.append(s.spoc[index].look_one_num)
                    aver_long_aggregate.append(s.spoc[index].look_sum_time)

        middle_times = len(aver_times_aggregate) / 2
        mt = aver_times_aggregate[middle_times]

        middle_long = len(aver_long_aggregate) / 2
        ml = aver_long_aggregate[middle_long]

        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)

                    # score = judge_score(s.spoc[index].spoc_score)
                    # at = judge_num(s.spoc[index].spoc_score, mt)
                    # al = judge_long(s.spoc[index].spoc_score, ml)
                    if s.spoc[index].spoc_score < 60.00:
                        score = '不及格'
                    elif 60.00 <= s.spoc[index].spoc_score < 70.00:
                        score = '及格'
                    elif 70.00 <= s.spoc[index].spoc_score < 80.00:
                        score = '良好'
                    else:
                        score = '优秀'

                    if s.spoc[index].look_one_num >= mt:
                        at = '多'
                    else:
                        at = '少'

                    if s.spoc[index].look_sum_time >= ml:
                        al = '长'
                    else:
                        al = '短'

                    rank = judge_ABC(score, at, al)

                    detail = (s.spoc[index].spoc_score,
                              s.spoc[index].look_one_num,
                              s.spoc[index].look_sum_time,
                              rank
                              )
                    students.append(detail)

    return students


def judge_ABC(score, times, long):
    if score == '不及格':
        rank = 'C'
    elif times == '多' and long == '长':
        rank = 'A'
    else:
        rank = 'B'
    return rank


def judge_score(n):
    if n < 60.00:
        score = '不及格'
    elif 60.00 <= n < 70.00:
        score = '及格'
    elif 70.00 <= n < 80.00:
        score = '良好'
    else:
        score = '优秀'
    return score


def judge_num(n, a):
    if n >= a:
        at = '多'
    else:
        at = '少'
    return at


def judge_long(n, a):
    if n >= a:
        at = '长'
    else:
        at = '短'
    return at


def spoc_main_display():
    datas = []
    spoc = SpocScoreDoc.objects().all()
    spocs = list(set(s.name for s in spoc))
    for sp in spocs:
        sc = SpocScoreDoc.objects(name=sp).all()
        stu_num, pass_num, pass_rate, sum_score, aver_score = 0, 0, 0.0, 0.0, 0.0
        for t in sc:
            stu_num += 1
            sum_score += t.spoc_score
            if t.spoc_score >= 60.00:
                pass_num += 1
        aver_score = format(float(sum_score) / float(stu_num), '.2f')
        pass_rate = format(float(pass_num) / float(stu_num), '.2f')
        datas.append((sp, stu_num, aver_score, pass_rate))
    return datas


def spoc_analysis_display_one(name):
    hs = SpocScoreDoc.objects(name=name).all()
    less_than_sixty, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred = 0, 0, 0, 0, 0
    for hh in hs:
        if hh.spoc_score < 60.00:
            less_than_sixty += 1
        elif 60.00 <= hh.spoc_score < 70.00:
            sixty_seventy += 1
        elif 70.00 <= hh.spoc_score < 80.00:
            seventy_eighty += 1
        elif 80.00 <= hh.spoc_score < 90.00:
            eighty_ninety += 1
        elif 90.00 <= hh.spoc_score <= 100.00:
            ninety_hundred += 1
    datas = (less_than_sixty, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred)
    return datas


def spoc_analysis_display_grade(name, grade):
    spocs = SpocScoreDoc.objects(name=name).all()
    stus = StudentDoc.objects(classroom=grade).all()
    less_than_sixty, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred = 0, 0, 0, 0, 0
    for h in spocs:
        for s in stus:
            if h in s.spoc:
                index = s.spoc.index(h)
                if s.spoc[index].spoc_score < 60.00:
                    less_than_sixty += 1
                elif 60.00 <= s.spoc[index].spoc_score < 70.00:
                    sixty_seventy += 1
                elif 70.00 <= s.spoc[index].spoc_score < 80.00:
                    seventy_eighty += 1
                elif 80.00 <= s.spoc[index].spoc_score < 90.00:
                    eighty_ninety += 1
                elif 90.00 <= s.spoc[index].spoc_score <= 100.00:
                    ninety_hundred += 1
    datas = (less_than_sixty, sixty_seventy, seventy_eighty, eighty_ninety, ninety_hundred)
    return datas


def spoc_look_score(name):
    datas = []
    hs = SpocScoreDoc.objects(name=name).all()
    for hh in hs:
        datas.append([hh.spoc_score, hh.look_sum_time])
    return datas


def spoc_look_score_grade(name, grade):
    datas = []
    spocs = SpocScoreDoc.objects(name=name).all()
    stus = StudentDoc.objects(classroom=grade).all()
    for h in spocs:
        for s in stus:
            if h in s.spoc:
                index = s.spoc.index(h)
                datas.append([s.spoc[index].spoc_score, s.spoc[index].look_sum_time])

    return datas


def spoc_look_num(name):
    datas = []
    hs = SpocScoreDoc.objects(name=name).all()
    for hh in hs:
        datas.append([hh.look_one_num, hh.look_times_num])
    return datas


def spoc_look_num_grade(name, grade):
    datas = []
    spocs = SpocScoreDoc.objects(name=name).all()
    stus = StudentDoc.objects(classroom=grade).all()
    for h in spocs:
        for s in stus:
            if h in s.spoc:
                index = s.spoc.index(h)
                datas.append([s.spoc[index].look_one_num, s.spoc[index].look_times_num])
    return datas


def spoc_nums_long(name):
    datas = []
    hs = SpocScoreDoc.objects(name=name).all()
    for hh in hs:
        datas.append([hh.look_one_num, hh.look_sum_time])
    return datas


def spoc_nums_long_grade(name, grade):
    datas = []
    spocs = SpocScoreDoc.objects(name=name).all()
    stus = StudentDoc.objects(classroom=grade).all()
    for h in spocs:
        for s in stus:
            if h in s.spoc:
                index = s.spoc.index(h)
                datas.append([s.spoc[index].look_one_num, s.spoc[index].look_sum_time])
    return datas


def spoc_detail_students(name, num, classroom):
    if classroom == 'null':
        spocs = SpocScoreDoc.objects(name=name).all()
        students = []
        stu = StudentDoc.objects().all()
        if int(num) == 0:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if s.spoc[index].spoc_score < 60.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)

        elif int(num) == 1:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if 60.00 <= s.spoc[index].spoc_score < 70.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)

        elif int(num) == 2:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if 70.00 <= s.spoc[index].spoc_score < 80.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)
        elif int(num) == 3:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if 80.00 <= s.spoc[index].spoc_score < 90.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)
        elif int(num) == 4:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if 90.00 <= s.spoc[index].spoc_score <= 100.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)
    else:
        spocs = SpocScoreDoc.objects(name=name).all()
        students = []
        stu = StudentDoc.objects(classroom=classroom).all()
        if int(num) == 0:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if s.spoc[index].spoc_score < 60.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)

        elif int(num) == 1:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if 60.00 <= s.spoc[index].spoc_score < 70.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)

        elif int(num) == 2:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if 70.00 <= s.spoc[index].spoc_score < 80.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)
        elif int(num) == 3:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if 80.00 <= s.spoc[index].spoc_score < 90.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)
        elif int(num) == 4:
            for t in spocs:
                for s in stu:
                    if t in s.spoc:
                        index = s.spoc.index(t)
                        if 90.00 <= s.spoc[index].spoc_score <= 100.00:
                            detail = (s.student_id, s.real_name, s.spoc[index])
                            students.append(detail)
    return students


def spoc_detail_export_students(name, num):
    spocs = SpocScoreDoc.objects(name=name).all()
    students = []
    stu = StudentDoc.objects().all()
    if int(num) == 0:
        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    if s.spoc[index].spoc_score < 60.00:
                        detail = (s.student_id, s.real_name, s.spoc[index].spoc_score, s.spoc[index].look_one_num,
                                  s.spoc[index].look_times_num, s.spoc[index].look_sum_time, s.spoc[index].titles,
                                  s.spoc[index].reviews_reply)
                        students.append(detail)

    elif int(num) == 1:
        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    if 60.00 <= s.spoc[index].spoc_score < 70.00:
                        detail = (s.student_id, s.real_name, s.spoc[index].spoc_score, s.spoc[index].look_one_num,
                                  s.spoc[index].look_times_num, s.spoc[index].look_sum_time, s.spoc[index].titles,
                                  s.spoc[index].reviews_reply)
                        students.append(detail)

    elif int(num) == 2:
        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    if 70.00 <= s.spoc[index].spoc_score < 80.00:
                        detail = (s.student_id, s.real_name, s.spoc[index].spoc_score, s.spoc[index].look_one_num,
                                  s.spoc[index].look_times_num, s.spoc[index].look_sum_time, s.spoc[index].titles,
                                  s.spoc[index].reviews_reply)
                        students.append(detail)
    elif int(num) == 3:
        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    if 80.00 <= s.spoc[index].spoc_score < 90.00:
                        detail = (s.student_id, s.real_name, s.spoc[index].spoc_score, s.spoc[index].look_one_num,
                                  s.spoc[index].look_times_num, s.spoc[index].look_sum_time, s.spoc[index].titles,
                                  s.spoc[index].reviews_reply)
                        students.append(detail)
    elif int(num) == 4:
        for t in spocs:
            for s in stu:
                if t in s.spoc:
                    index = s.spoc.index(t)
                    if 90.00 <= s.spoc[index].spoc_score <= 100.00:
                        detail = (s.student_id, s.real_name, s.spoc[index].spoc_score, s.spoc[index].look_one_num,
                                  s.spoc[index].look_times_num, s.spoc[index].look_sum_time, s.spoc[index].titles,
                                  s.spoc[index].reviews_reply)
                        students.append(detail)

    return students
