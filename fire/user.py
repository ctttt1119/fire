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

    if o.expert:
        expid = o.expert.id
        o.expert = expid
    res = {}
    if isinstance(o, BaseDocument):
        data = o.to_mongo()
        data = data.to_dict()
        res = convert(data)
    res = json.dumps(res,indent=4)
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

    if o.expert:
        expid = o.expert.id
        o.expert = expid

    res = {}
    if isinstance(o, BaseDocument):
        data = o.to_mongo()
        data = data.to_dict()
        res = convert(data)
    res2 = {}
    for key, value in res.items():
        if key != 'password':
            res2[key] = value
    res2 = json.dumps(res2,indent=4)
    return res2

def convertMongoToJson3(o):
    
    def convert(dic_data):
        from bson import ObjectId
        for key, value in dic_data.items():
            if isinstance(value, ObjectId):
                dic_data[key] = str(value)
            if key == 'messages':
                for message in value:
                    message['noticeBuildTime'] = str(message['noticeBuildTime'])
        return dic_data

    if o.expert:
        expid = o.expert.id
        o.expert = expid
        expert2 = database.getExpertInfo(expid)

        res = {}
        if isinstance(o, BaseDocument):
            data = o.to_mongo()
            data = data.to_dict()
            res = convert(data)
            data2 = expert2.to_mongo()
            data2 = data2.to_dict()
            res2 = convert(data2)
        res11 = {}
        for key, value in res.items():
            if key != 'password' and key != 'expert':
                res11[key] = value
        res22 = {}
        for key, value in res2.items():
            if key == '_id' or key == 'expertName' or key == 'workplace':
                res22[key] = value
        res11['expert'] = res22
        res11 = json.dumps(res11, indent=4)
        return res11
    else:
        res = {}
        if isinstance(o, BaseDocument):
            data = o.to_mongo()
            data = data.to_dict()
            res = convert(data)
        res2 = {}
        for key, value in res.items():
            if key != 'password':
                res2[key] = value
        res2 = json.dumps(res2,indent=4)
        return res2

#登录
def login(request):
    if (request.method != 'POST'):
        msg = 'gg'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    # session
    # username = request.session.get('username')
    # if username:
    #     # msg = 'already login'
    #     # res = "{\"msg\": \"" + msg + "\"}"
    #     # return HttpResponse(res)
    #     return HttpResponse(username)

    dict = request.POST
    username=dict.get('username')
    password=dict.get('password')
    # NoneType
    if username is None or password is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    # session
    # request.session['username'] = 'usernamehaha'

    msg = valid_test.login(username, password)
    if (msg == 'illegalUsername' or msg == 'illegalPassword'):
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    result = database.login(username, password)
    if (result == 'error' or result == 'database login error'):
        res = "{\"msg\": \"" + result + "\"}"
        return HttpResponse(res)
    else:
        result = convertMongoToJson2(result)
        res = "{\"msg\": \"ok\", \"user\": " + result + "}"
        return HttpResponse(res)

#注册
def register(request):
    if (request.method != 'POST'): #
        msg = 'gg'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.POST
    username = dict.get('username')
    nickname = dict.get('nickname')
    password = dict.get('password')
    userEmail = dict.get('userEmail')
    # NoneType
    if username is None or password is None or nickname is None or userEmail is None:
        msg = 'empty input'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    msg = valid_test.register(username, nickname, password, userEmail)
    if (msg == 'illegalUsername' or msg == 'illegalNickname' or msg == 'illegalPassword' or msg == 'illegalUserEmail'):
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)

    result = database.register(username, nickname, password, userEmail)
    if (result == 'existUsername' or result == 'existUserEmail' or result == 'error' or result == 'databaseError1' or result == 'databaseError2' or result == 'databaseError3' or result == 'databaseError4'):
        res = "{\"msg\": \"" + result + "\"}"
        return HttpResponse(res)
    else:
        result = convertMongoToJson2(result)
        res = "{\"msg\": \"ok\", \"user\": " + result + "}"
        return HttpResponse(res)



#获取普通用户信息
def getUserInfo(request):
    if (request.method!='GET'):
        return None
    dict = request.GET
    userId = dict.get('userId')
    if userId == "":
        err_msg = "userId is null, please try again"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    res = database.getUserInfo(userId)
    if (res=='database getUserInfo error'):
        err_msg = "获取普通用户信息失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    elif (res=={}):
        err_msg = "该用户不存在"
        msg3 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg3)
    else :
        res1 = convertMongoToJson3(res) 
        res2 = "{\"msg\": \"ok\", \"user_info\": " + res1 + "}"
        return HttpResponse(res2)

#用户升级为管理员
def upgradeAdmin(request):
    if(request.method!='POST'):
        return None
    dict=request.POST
    userId = dict.get('userId')
    res=database.upgradeAdmin(userId)
    if (res=='database upgradeAdmin error' or res==False):
        err_msg = "用户升级为管理员失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else : 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)

#用户修改昵称
def editNick(request):
    if(request.method!='POST'):
        return None
    dict=request.POST
    userId = dict.get('userId')
    newNickname = dict.get('newNickname')
    res=database.editNick(userId,newNickname)
    if (res=='database editNick error' or res==False):
        err_msg = "用户修改昵称失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else : 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)

#用户修改简介
def editUserIntro(request):
    if(request.method!='POST'):
        return None
    dict=request.POST
    userId = dict.get('userId')
    newUserIntro = dict.get('newUserIntro')
    res=database.editUserIntro(userId,newUserIntro)
    if (res=='database editUserIntro error' or res==False):
        err_msg = "用户修改简介失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else : 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)

#用户修改密码
def changePwd(request):
    if(request.method!='POST'):
            return None
    dict=request.POST
    userId = dict.get('userId')
    newPassword = dict.get('newPassword')
    res=database.changePwd(userId,newPassword)
    if (res=='database changePwd error' or res==False):
        err_msg = "用户修改密码失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else : 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)


#生成消息
def setNewNotice(request):
    if (request.method != 'POST'):
        msg = 'gg'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.POST
    userId = dict.get('userId')
    noticeType = dict.get('noticeType')
    noticeContent = dict.get('noticeContent')
    noticePlusContent = dict.get('noticePlusContent')
    
    result = database.setNewNotice(userId, noticeType, noticeContent, noticePlusContent)
    res = "{\"msg\": \"" + result + "\"}"
    return HttpResponse(res)


# 一条消息已读
def setOneNoticeRead(request):
    if (request.method != 'POST'):
        msg = 'gg'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.POST
    userId = dict.get('userId')
    offset = dict.get('offset')

    result = database.setOneNoticeRead(userId, offset)
    res = "{\"msg\": \"" + result + "\"}"
    return HttpResponse(res)

# 所有消息已读
def setAllNoticesRead(request):
    if (request.method != 'POST'):
        msg = 'gg'
        res = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(res)
    dict = request.POST
    userId = dict.get('userId')

    result = database.setAllNoticesRead(userId)
    res = "{\"msg\": \"" + result + "\"}"
    return HttpResponse(res)

# 关注专家
def followExpert(request):
    if(request.method!='POST'):
        return None
    dict=request.POST
    userId = dict.get('userId')
    expertId = dict.get('expertId')
    res=database.followExpert(userId,expertId)
    if (res=='database followExpert error' or res==False):
        err_msg = "用户关注专家失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else : 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)

# 取消关注
def cancelFollow(request):
    if(request.method!='POST'):
            return None
    dict=request.POST
    userId = dict.get('userId')
    expertId = dict.get('expertId')
    res=database.cancelFollow(userId,expertId)
    if (res=='database cancelFollow error' or res==False):
        err_msg = "用户取消关注专家失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else : 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)

#判断是否关注
def checkFollow(request):
    if(request.method!='GET'):
            return None
    dict=request.GET
    userId = dict.get('userId')
    expertId = dict.get('expertId')
    res=database.checkFollow(userId,expertId)
    if (res=='database checkFollow error' or res==False):
        err_msg = "判断是否关注专家失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else : 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)