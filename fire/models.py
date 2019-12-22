from django.db import models
from mongoengine import *
from datetime import datetime


class Message(EmbeddedDocument):
    noticeBuildTime = DateTimeField()
    noticeType = StringField(max_length=30)
    noticeContent = StringField(max_length=500)
    noticePlusContent = StringField()
    noticeRead = StringField()

class User(Document):
    expert = GenericReferenceField()
    # expert = ReferenceField(Expert,unique=True)
    # password hash?
    password = StringField(max_length=30)
    userIntro = StringField(max_length=200)
    username = StringField(max_length=30,required=True,unique=True)
    nickname = StringField(max_length=30)
    # user/admin
    identity = StringField(max_length=30,default="user",required=True)
    userEmail = EmailField(max_length=30,required=True,unique=True)
    messages = ListField(EmbeddedDocumentField(Message))

class Expert(Document):
    user = ReferenceField(User,required=True,unique=True)
    # expertTags is limited to 3, please restrict it in your api
    expertTags = ListField(StringField(max_length=30))
    achieveIntro = StringField(max_length=500)
    expertEmail = EmailField(max_length=30,required=True,unique=True)
    emailPublicity = BooleanField(default=False)
    paperNum = IntField(default=0)
    patentNum = IntField(default=0)
    identityImage = StringField(required=True)
    workplace = StringField(max_length=200,required=True)
    expertTitle = StringField(max_length=30)
    expertName = StringField(max_length=30,required=True)
    paperList = ListField(GenericReferenceField())
    patentList = ListField(GenericReferenceField())

class Apply(Document):
    applicant = ReferenceField(User,required=True)
    # unhandled,passed,refused
    resultType = StringField(default="unhandled",max_length=30)
    resultReason = StringField(max_length=200)
    applicantImage = StringField(required=True)
    applicantWorkplace = StringField(max_length=200,required=True)
    applicantTitle = StringField(max_length=30)
    applicantName = StringField(max_length=30,required=True)
    applicantEmail = StringField(max_length=30,required=True)
    applyTime = DateTimeField(default=datetime.now(), required=True)

class Paper(Document):
    uploadExpert = ReferenceField(Expert)
    # paperTags is limited to 3, please restrict it in your api
    paperTags = ListField(StringField(max_length=30))
    DOI = StringField(max_length=50)
    paperTitle = StringField(max_length=100,required=True)
    paperTime = DateTimeField(default=datetime.now(), required=True)
    paperPublication = StringField(max_length=50)
    paperUrl = StringField()
    paperAbstract = StringField(max_length=500)
    quoteNum = IntField(default=0)
    readNum = IntField(default=0)
    starNum = IntField(default=0)
    starUser = ListField(ReferenceField(User))
    author = ListField(StringField(max_length=30,required=True),required=True)
    # author = ListField(StringField())

class Patent(Document):
    uploadExpert = ReferenceField(Expert)
    patentTags = ListField(StringField(max_length=30))
    patentName = StringField(max_length=100,required=True)
    patentNo = StringField(max_length=30,required=True)
    patentTime = DateTimeField(default=datetime.now(), required=True)
    patentAgency = StringField(max_length=30)
    patentAbstract = StringField(max_length=500)
    readNum = IntField(default=0)
    starNum = IntField(default=0)
    starUser = ListField(ReferenceField(User))
    patentAuthors = ListField(StringField(max_length=30,required=True),required=True)

class Watch(Document):
    expert = ReferenceField(Expert,required=True)
    user = ReferenceField(User,required=True)