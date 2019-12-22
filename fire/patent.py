from . import database
from . import valid_test
from django.http.response import HttpResponse
import json
from datetime import datetime,date
from mongoengine.base import BaseDocument
from .models import *

class DateEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def convertMongoToJson(o):
    def convert(dic_data):
        from bson import ObjectId
        for key, value in dic_data.items():
            if isinstance(value, ObjectId):
                dic_data[key] = str(value)
            if key == 'messages':
                for message in value:
                    message['noticeBuildTime'] = str(message['noticeBuildTime'])
        return dic_data

    res = {}
    if isinstance(o, BaseDocument):
        data = o.to_mongo()
        data = data.to_dict()
        res = convert(data)
    res = json.dumps(res, cls=DateEncoder)
    return res


#上传专利
def uploadPatent(request):
    if (request.method!='POST'):
        return None
    dict = request
    temp4 = eval(str(request.body)[1:])
    patent = json.loads(temp4)['patentEntity']

    uploadExpertId=patent['expertId']
    patentTags=patent['patentTags']
    #patentTags=['cs']
    patentName=patent['patentName']
    patentNo=patent['patentNo']
    patentTime=patent['patentTime']
    tmp_time=str(patentTime)
    tmp_time=tmp_time[:-5]
    tmp_time=tmp_time+'Z'
    time = datetime.strptime(tmp_time, '%Y-%m-%dT%H:%M:%SZ')
    patentAbstract=patent['patentAbstract']
    patentAuthors=patent['patentAuthors']
    tmp=patent['patentAuthors_id']
    authors=[]
    patentAuthors_id=[]
    for r in patentAuthors:
        authors.append(r['name'])
    for t in tmp:
        patentAuthors_id.append(t['ID'])
    #patentAuthors=['ct']
    readNum = '0'
    starNum = '0'
    msg=valid_test.repeat_patentNo(patentNo)
    if (msg!="ok"):
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    res = database.uploadPatent(uploadExpertId,patentTags,patentName,patentNo,time,patentAbstract,readNum,starNum,authors,patentAuthors_id)
    if (res=='uploadPatent notUnique' or res=='database uploadPatent error'):
        err_msg = "上传专利失败！请重试。"
        err_msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(err_msg2)
    else:
        res1 = str(res) 
        res2 = "{\"msg\": \"ok\", \"patentNo\": " + res1 + "}"
        name=Expert.objects.with_id(uploadExpertId).expertName
        message = Message(
            noticeBuildTime = datetime.now(),
            noticeType = "新专利",
            noticeContent = "您关注的专家 "+name+" 上传了新专利",
            noticePlusContent = res1,
            noticeRead = "not",
        )
        result = database.noticeFollowers(uploadExpertId,message)
        if (result != True):
            res = "{\"msg\": \"" + result + "\"}"
            return HttpResponse(res)
        return HttpResponse(res2)


#增加专利阅读量
def addPatentReading(request):
    if (request.method!='POST'):
        return None
    dict = request.POST
    patentId = dict.get('patentId')
    res=database.addPatentReading(patentId)
    if (res=='database addPatentReading error' or res==False):
        msg="增加专利阅读量失败！请重试。"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    else :
        msg="ok"
        return HttpResponse(msg)
        


#增加专利star
def addPatentStar(request):
    if (request.method!='POST'):
        return None
    dict = request.POST
    patentId = dict.get('patentId')
    res=database.addPatentStar(patentId)
    if (res=='database addPatentStar error' or res==False):
        msg="增加专利star失败！请重试。"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    else :
        msg="ok"
        return HttpResponse(msg)

#获取专利信息
def getPatentInfo(request):
    if (request.method!='GET'):
        return None
    dict = request.GET
    patentId = dict.get('patentId')
    res = database.getPatentInfo(patentId)
    if (res=='database getPatentInfo error' or res=={}):
        err_msg = "获取普通专利信息失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)   
    else :
        res1 = convertMongoToJson(res) 
        res2 = "{\"msg\": \"ok\", \"patent_info\": " + res1 + "}"
        return HttpResponse(res2)
def testprint(s):
    with open('/home/testfile','w') as f:
        print(s,file=f)

#获取专家的全部专利
def getAllPatentByExpertId(request):
    if(request.method!='GET'):
        return None
    dict = request.GET
    expertId = dict.get('expertId')
    res = database.getAllPatentByExpertId(expertId)
    res2 = "["
    cnt = 0
    for o in res:
        patentId = o.id
        patent = database.getPatentInfo(patentId)
        if patent == 'database getPatentInfo error':
            return HttpResponse("{\"err_msg\": \"" + "获取专家全部专利失败！" + "\"}")
        if cnt == 0:
            res2 = res2 + convertMongoToJson(patent)
        else:
            res2 = res2 + "," + convertMongoToJson(patent)
        cnt = cnt + 1
    res2 = res2 + "]"
    return HttpResponse(res2)
