# -*- coding:utf-8 -*-
from config.ext import mongo

__all__ = ['StudentDoc', 'CourseDoc', 'HomeworkDoc', 'TestScoreDoc', 'SpocScoreDoc']


# 作业
class HomeworkDoc(mongo.DynamicDocument):
    name = mongo.StringField()
    score = mongo.FloatField()
    mutual = mongo.ListField()  # 互评


# 测试
class TestScoreDoc(mongo.DynamicDocument):
    name = mongo.StringField()
    score = mongo.FloatField()
    first_score = mongo.FloatField()
    second_score = mongo.FloatField()


# 学习数据统计
class SpocScoreDoc(mongo.DynamicDocument):
    name = mongo.StringField()
    spoc_score = mongo.FloatField()
    source_score = mongo.FloatField()
    look_one_num = mongo.IntField()
    look_times_num = mongo.IntField()
    look_sum_time = mongo.IntField()
    titles = mongo.IntField()
    reviews_reply = mongo.IntField()


# 课程数据
class CourseDoc(mongo.DynamicDocument):
    name = mongo.StringField()
    classify = mongo.StringField()
    title = mongo.StringField()
    datetime = mongo.StringField()
    status = mongo.StringField()
    score_type = mongo.StringField()    # 评分方式
    post_num = mongo.IntField()     # 提交人数
    sum_score = mongo.FloatField()
    aver_score = mongo.FloatField()


class StudentDoc(mongo.DynamicDocument):
    student_id = mongo.StringField(required=True)
    real_name = mongo.StringField(required=True)
    school = mongo.StringField()
    classroom = mongo.IntField()
    pet_name = mongo.StringField()
    homework = mongo.ListField(mongo.ReferenceField(HomeworkDoc))
    test = mongo.ListField(mongo.ReferenceField(TestScoreDoc))
    spoc = mongo.ListField(mongo.ReferenceField(SpocScoreDoc))


# 06171001-06171034  1班
# 06171035-06171073  2班
# 06171074-06171109  3班
# 06171110-06171145  4班
