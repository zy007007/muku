# -*- coding:utf-8 -*-
import mongoengine as me

from flask_mongoengine import MongoEngine as ME


class MongoEngine(ME):
    def __init__(self, app=None, config=None):
        super(MongoEngine, self).__init__(app, config)
        self.me = me
        self.BinaryField = me.BinaryField
        self.BooleanField = me.BooleanField
        self.ComplexDateTimeField = me.ComplexDateTimeField
        self.DateTimeField = me.DateTimeField
        self.DecimalField = me.DecimalField
        self.DictField = me.DictField
        self.DynamicField = me.DynamicField
        self.EmailField = me.EmailField
        self.EmbeddedDocumentField = me.EmbeddedDocumentField
        self.EmbeddedDocumentListField = me.EmbeddedDocumentListField
        self.FileField = me.FileField
        self.FloatField = me.FloatField
        self.GenericEmbeddedDocumentField = me.GenericEmbeddedDocumentField
        self.GenericReferenceField = me.GenericReferenceField
        self.GeoPointField = me.GeoPointField
        self.ImageField = me.ImageField
        self.IntField = me.IntField
        self.ListField = me.ListField
        self.MapField = me.MapField
        self.ObjectIdField = me.ObjectIdField
        self.ReferenceField = me.ReferenceField
        self.SequenceField = me.SequenceField
        self.SortedListField = me.SortedListField
        self.StringField = me.StringField
        self.URLField = me.URLField
        self.UUIDField = me.UUIDField
        self.PointField = me.PointField
        self.LineStringField = me.LineStringField
        self.PolygonField = me.PolygonField
        self.MultiPointField = me.MultiPointField
        self.MultiLineStringField = me.MultiLineStringField
        self.MultiPolygonField = me.MultiPolygonField
        self.EmbeddedDocument = me.EmbeddedDocument
        self.DynamicEmbeddedDocument = me.DynamicEmbeddedDocument