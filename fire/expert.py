from . import database
from . import valid_test
from django.http.response import HttpResponse
import json
import datetime
from mongoengine.base import BaseDocument
import os

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
            res = res + convertMongoToJson2(ob)
        else:
            res = res + "," + convertMongoToJson2(ob)
        cnt = cnt + 1
    res = res + "]"
    return res

#获取专家信息
def getExpertInfo(request):
    if (request.method!='GET'):
        return None
    dict = request.GET
    expertId = dict.get('expertId')
    res = database.getExpertInfo(expertId)
    if (res=='database getExpertInfo error'):
        err_msg = "获取专家信息失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    elif (res=={}):
        err_msg = "该专家不存在"
        msg3 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg3)
    else :
        res1 = convertMongoToJson2(res) 
        res2 = "{\"msg\": \"ok\", \"expert_info\": " + res1 + "}"
        return HttpResponse(res2)

#上传专家认证资料
def uploadApplyInfo(request):
    if (request.method!='POST'):
        return None
    dict = request
    temp4 = eval(str(request.body)[1:])
    apply = json.loads(temp4)['expertApply']

    userId = apply['userId']
    #applicantImage = apply['identityImage']
    applicantImage='/root/getpicture/'+userId+'_application.jpg'
    applicantName = apply['expertName']
    applicantTitle = apply['expertTitle']
    applicantWorkplace = apply['workplace']
    applicantEmail = apply['expertEmail']
    resultType='unhandled'
    resultReason='unhandled'
    res=database.uploadApplyInfo(userId,applicantImage,applicantName,applicantTitle,applicantWorkplace,applicantEmail,resultType,resultReason)
    if res=='ok':
        msg="{\"msg\": \"ok\"}"
        return HttpResponse(msg)
    elif res == 'had expert':
        return HttpResponse("{\"msg\": \" 该用户已经是专家！ \"}")
    else:
        msg="{\"msg\": \"上传专家认证资料失败！请重试。\"}"
        return HttpResponse(msg)

#上传图片
def uploadImage(request):
    if request.method!='POST':
        return None
    
    myFile = request.FILES.dict()
    upload_name=list(myFile.keys())[0]
    #file_name=myFile[upload_name]
    file=myFile[upload_name]
    #file=request.FILES.get(file_name,None)
    file_name=upload_name+'_application.jpg'     #文件重命名为userID_application.jpg
    if not file:
        return HttpResponse('No files for upload.')
    dest=open(os.path.join('/root/getpicture/',file_name),'wb+')
    for chunk in file.chunks():
        dest.write(chunk)
    dest.close()
    return HttpResponse('ok')


#修改专家简介
def editExpertIntro(request):
    if(request.method!='POST'):
        return None
    dict=request.POST
    expertId = dict.get('expertId')
    newExpertIntro = dict.get('newExpertIntro')
    res=database.editExpertIntro(expertId,newExpertIntro)
    if (res=='database editIntro error' or res==False):
        err_msg = "专家修改简介失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else : 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)

def addPaper(request):
    if request.method!='POST':
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")
    
    dict = request.POST
    if dict == None :
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")

    expertId = dict.get('expertId')
    paperId = dict.get('paperId')
    res = database.addPaperForExpert(expertId,paperId)
    if (res!=True):
        err_msg = "专家添加论文失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else: 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)

def addPatent(request):
    if request.method!='POST':
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")
    
    dict = request.POST
    if dict == None :
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")
        
    expertId = dict.get('expertId')
    patentId = dict.get('patentId')
    res = database.addPatentForExpert(expertId,patentId)
    if (res!=True):
        err_msg = res
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2)
    else : 
        res2 = "{\"msg\": \"ok\"" + "}"
        return HttpResponse(res2)

def getExpertByExpertName(request):
    if request.method!='GET':
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")

    dict = request.GET
    if dict == None :
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")

    expertName = dict.get('expertName')
    res = database.getExpertByExpertName(expertName)
    if (res == 'database getExpertByExpertName error'):
        return HttpResponse("{\"err_msg\": \"" + res + "\"}")
    elif(res=={}):
        err_msg = "该专家不存在"
        msg3 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg3)
    else :
        msg = repeatConvertMongoToJson(res)
        return HttpResponse(msg)

    