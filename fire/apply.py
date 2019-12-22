from . import database
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
    res = json.dumps(res, cls=DateEncoder)
    return res

def getAllApplyInfo(request):
    if (request.method != 'GET'):
        msg = 'gg'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    result = database.getAllApplyInfo()
    if (result == 'getAllApplyInfo error' or result == 'database getAllApplyInfo error'):
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
        res = "{\"msg\": \"ok\", \"apply\": " + res1 + "}"
        return HttpResponse(res)

def applyPassed(request):
    if(request.method != 'POST'):
        msg = "POST me please"
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    
    dict = request.POST
    apply_id = dict.get('applyId')
    resultReason = dict.get('resultReason')
    res=database.applyPassed(apply_id,resultReason)
    if(res == 'database applyPassed error1'):
        msg = "没有找到对应的apply！"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    elif(res == 'database applyPassed error2'):
        msg = "专家创建失败！"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    elif(res == 'database applyPassed error3'):
        msg = "没有找到新创建的专家！"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    elif(res == 'database applyPassed error4'):
        msg = "为用户关联专家失败！"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    elif(res == 'database applyPassed error5'):
        msg = "修改apply状态失败！"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    elif(res == 'database applyPassed error6'):
        msg = "发送消息失败！"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    elif res == 'had passed':
        return HttpResponse("{\"msg\": \"" + "通过了通过了，别点了！" + "\"}")
    elif res == 'had refused':
        return HttpResponse("{\"msg\": \"" + "拒绝过了，不准通过。" + "\"}")
    elif res == True:
        msg = "ok"
        return HttpResponse(msg)
    elif res == False:
        return HttpResponse(res)
    else:
        return HttpResponse(res)

def applyRefused(request):
    if(request.method != 'POST'):
        msg = "POST me please"
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    
    dict = request.POST
    apply_id = dict.get('applyId')
    resultReason = dict.get('resultReason')
    res=database.applyRefused(apply_id,resultReason)
    if (res=='database applyRefused error'):
        msg = "拒绝专家认证失败！"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    if (res=='database applyRefused error2'):
        msg = "发送消息失败！"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    elif res == 'had passed':
        return HttpResponse("{\"msg\": \"" + "已经通过了，不准拒绝。" + "\"}")
    elif res == 'had refused':
        return HttpResponse("{\"msg\": \"" + "不准拒绝拒绝过的。" + "\"}")
    else:
        msg = "ok"
        return HttpResponse(msg)

# 获取用户专家认证状态
def getApplyState(request):
    if (request.method != 'GET'): #
        msg = 'gg'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.GET
    userId = dict.get('userId')

    result = database.getApplyState(userId)
    if (result == 'database getApplyState error1' or result == 'database getApplyState error2' or result == 'database getApplyState error3'):
        res = "{\"msg\": \"" + result + "\"}"
        return HttpResponse(res)
    else: 
        # if(result == 'unhandled'):
        #     res = "{\"msg\": \"ok\", \"applyState\": " + "0" + "}"
        #     return HttpResponse(res)
        # else:
        #     res = "{\"msg\": \"ok\", \"applyState\": " + str(result) + "}"
        #     return HttpResponse(res)
        res = "{\"msg\": \"ok\", \"applyState\": " + str(result) + "}"
        return HttpResponse(res)