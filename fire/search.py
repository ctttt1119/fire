from . import database
from . import valid_test
from django.http.response import HttpResponse
import json
import datetime
from mongoengine.base import BaseDocument

class DateEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, datetime.datetime):
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
    res2 = {}
    for key,value in res.items():
        if key == 'paperList':
            continue
        if key == 'patentList':
            continue
        res2[key] = value
    res2 = json.dumps(res2,indent=4)
    return res2

def repeatConvertMongoToJson(o):
    res = "["
    cnt = 0
    for ob in o:
        if cnt == 0:
            res = res + convertMongoToJson(ob)
        else :
            res = res + "," + convertMongoToJson(ob)
        cnt = cnt + 1
    res = res + "]"
    return res
    
def convertMongoToJson2(o):
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
    res2 = json.dumps(res, cls=DateEncoder)
    return res2

def repeatConvertMongoToJson2(o):
    res = "["
    cnt = 0
    for ob in o:
        if cnt == 0:
            res = res + convertMongoToJson2(ob)
        else :
            res = res + "," + convertMongoToJson2(ob)
        cnt = cnt + 1
    res = res + "]"
    return res

#根据keyword搜索
def searchByKeyword(request):
    if (request.method != 'GET'):
        return None
    dict = request.GET
    keyword = dict.get('keyword')
    searchType = dict.get('searchType')

    if searchType == "1":
        res = database.searchExpertByKeyword(keyword)
        if res == 'database searchExpertByKeyword error':
            msg = "数据库检索专家失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = repeatConvertMongoToJson(res)

    elif searchType == "2":
        res = database.searchPaperByKeyword(keyword)
        if res == 'database searchPaperByKeyword error':
            msg = "数据库检索论文失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = repeatConvertMongoToJson2(res)

    elif searchType == "3":
        res = database.searchExpertByKeyword(keyword)
        if res == 'database searchExpertByKeyword error':
            msg = "数据库检索专家失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = repeatConvertMongoToJson(res)
        res = database.searchPaperByKeyword(keyword)
        if res == 'database searchPaperByKeyword error':
            msg = "数据库检索论文失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = res2 + "," + repeatConvertMongoToJson2(res)

    elif searchType == "4":
        res = database.searchPatentByKeyword(keyword)
        if res == 'database searchPatentByKeyword error':
            msg = "数据库检索专利失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = repeatConvertMongoToJson2(res)

    elif searchType == "5":
        res = database.searchExpertByKeyword(keyword)
        if res == 'database searchExpertByKeyword error':
            msg = "数据库检索专家失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = repeatConvertMongoToJson(res)
        res = database.searchPatentByKeyword(keyword)
        if res == 'database searchPatentByKeyword error':
            msg = "数据库检索专利失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = res2 + "," + repeatConvertMongoToJson2(res)

    elif searchType == "6":
        res = database.searchPaperByKeyword(keyword)
        if res == 'database searchPaperByKeyword error':
            msg = "数据库检索论文失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = repeatConvertMongoToJson2(res)
        res = database.searchPatentByKeyword(keyword)
        if res == 'database searchPatentByKeyword error':
            msg = "数据库检索专利失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = res2 + "," + repeatConvertMongoToJson2(res)

    elif searchType == "7":
        res = database.searchExpertByKeyword(keyword)
        if res == 'database searchExpertByKeyword error':
            msg = "数据库检索专家失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = repeatConvertMongoToJson(res)
        res = database.searchPaperByKeyword(keyword)
        if res == 'database searchPaperByKeyword error':
            msg = "数据库检索论文失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = res2 + "," + repeatConvertMongoToJson2(res)
        res = database.searchPatentByKeyword(keyword)
        if res == 'database searchPatentByKeyword error':
            msg = "数据库检索专利失败！"
            msg2 = "{\"msg\": \"" + msg + "\"}"
            return HttpResponse(msg2)
        res2 = res2 + "," + repeatConvertMongoToJson2(res)

    else:
        res = "searchType 不合法！"
        msg2 = "{\"msg\": \"" + res + "\"}"
        return HttpResponse(msg2)

    return HttpResponse(res2)

#根据expertName搜索专利
def searchPatentByExpertName(request):
    if (request.method != 'GET'):
        msg = 'gg'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.GET
    expertName = dict.get('expertName')
    # NoneType
    if expertName is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    result = database.searchPatentByExpertName(expertName)
    if (result == 'No this expert patent' or result == 'database searchPatentByExpertName error'):
        res = "{\"msg\": \"" + result + "\"}"
        return HttpResponse(res)
    else:
        res1 = "["
        cnt = 0
        for r in result:
            if (cnt == 0):
                res1 = res1 + convertMongoToJson(r)
            else:
                res1 = res1 + ", " + convertMongoToJson(r)
            cnt += 1
        res1 = res1 + "]"
        res = "{\"msg\": \"ok\", \"paper\": " + res1 + "}"
        return HttpResponse(res)

#根据expertName搜索论文
def searchPaperByExpertName(request):
    if (request.method != 'GET'):
        msg = 'gg'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.GET
    expertName = dict.get('expertName')
    # NoneType
    if expertName is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    result = database.searchPaperByExpertName(expertName)
    if (result == 'database searchPaperByExpertName error' or result == 'No this expert paper'):
        res = "{\"msg\": \"" + result + "\"}"
        return HttpResponse(res)
    else:
        res1 = "["
        cnt = 0
        for r in result:
            if (cnt == 0):
                res1 = res1 + convertMongoToJson(r)
            else:
                res1 = res1 + ", " + convertMongoToJson(r)
            cnt += 1
        res1 = res1 + "]"
        res = "{\"msg\": \"ok\", \"paper\": " + res1 + "}"
        return HttpResponse(res)
