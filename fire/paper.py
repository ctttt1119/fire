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
        elif isinstance(obj, date):
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

#上传论文
def uploadPaper(request):
    
    if (request.method!='POST'):
        return None
    dict = request
    temp4 = eval(str(request.body)[1:])
    paper = json.loads(temp4)['paperEntity']

    #return HttpResponse(paper)

    uploadExpertId=paper['expertId']
    paperTags=paper['paperTags']
    #paperTags=['cs']
    DOI=paper['DOI']
    paperTitle=paper['paperTitle']
    paperTime=paper['paperTime']
    tmp_time=str(paperTime)
    tmp_time=tmp_time[:-5]
    tmp_time=tmp_time+'Z'
    time = datetime.strptime(tmp_time, '%Y-%m-%dT%H:%M:%SZ')
    paperUrl=paper['paperUrl']
    paperAbstract=paper['paperAbstract']
    author=paper['authors']
    tmp=paper['authors_id']
    paperPublication=paper['publication']
    authors=[]
    authors_id=[]
    for r in author:
        authors.append(r['name'])
    for t in tmp:
        authors_id.append(t['ID'])
    quoteNum = '0'
    readNum = '0'
    starNum = '0'
   
    msg=valid_test.repeat_doi(DOI)
    if (msg!="ok"):
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
 
    res=database.uploadPaper(uploadExpertId,paperTags,DOI,paperTitle,time,paperUrl,paperAbstract,quoteNum,readNum,starNum,authors,authors_id,paperPublication)
    if (res=='uploadPaper notUnique' or res=='database uploadPaper error'):
        err_msg = "上传论文失败！请重试。"
        err_msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(err_msg2)
    else: 
        res1 = str(res) 
        res2 = "{\"msg\": \"ok\", \"paperId\": " + res1 + "}"
        name=Expert.objects.with_id(uploadExpertId).expertName
        message = Message(
            noticeBuildTime = datetime.now(),
            noticeType = "新论文",
            noticeContent = "您关注的专家 "+name+" 上传了新论文",
            noticePlusContent = res1,
            noticeRead = "not",
        )

        result = database.noticeFollowers(uploadExpertId,message)
        if (result != True):
            res = "{\"msg\": \"" + result + "\"}"
            return HttpResponse(res)

        return HttpResponse(res2)

#获取专家的全部论文
def getAllPaperByExpertId(request):
    if(request.method!='GET'):
        return None
    dict = request.GET
    expertId = dict.get('expertId')
    res = database.getAllPaperByExpertId(expertId)
    res2 = "["
    cnt = 0
    for o in res:
        paperId = o.id
        paper = database.getPaperInfo(paperId)
        if paper == 'nothing':
            continue
        if paper == 'database getPaperInfo error':
            return HttpResponse("{\"err_msg\": \"" + "获取专家全部论文失败！" + "\"}")
        if cnt == 0:
            res2 = res2 + convertMongoToJson(paper)
        else:
            res2 = res2 + "," + convertMongoToJson(paper)
        cnt = cnt + 1
    res2 = res2 + "]"
    return HttpResponse(res2)
        

#增加论文阅读量
def addPaperReading(request):
    if (request.method!='POST'):
        return None
    dict = request.POST
    paperId = dict.get('paperId')
    res=database.addPaperReading(paperId)
    if (res=='database addPaperReading error' or res==False):
        msg="增加论文阅读量失败！请重试。"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    else :
        msg="ok"
        return HttpResponse(msg)

#增加论文star
def addPaperStar(request):
    if (request.method!='POST'):
        return None
    dict = request.POST
    paperId = dict.get('paperId')
    res=database.addPaperStar(paperId)
    if (res=='database addPaperStar error'):
        msg="增加论文star失败！请重试。"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    else :
        msg="ok"
        return HttpResponse(msg)

#增加论文引用量
def addPaperQuote(request):
    if (request.method!='POST'):
        return None
    dict = request.POST
    paperId = dict.get('paperId')
    res=database.addPaperQuote(paperId)
    if (res=='database addPaperStar error'):
        msg="增加论文引用量失败！请重试。"
        msg2 = "{\"msg\": \"" + msg + "\"}"
        return HttpResponse(msg2)
    else :
        msg="ok"
        return HttpResponse(msg)

#获取论文信息
def getPaperInfo(request):
    if (request.method!='GET'):
        return None
    dict = request.GET
    paperId = dict.get('paperId')
    res = database.getPaperInfo(paperId)
    if (res=='database getPaperInfo error'):
        err_msg = "获取论文信息失败！请重试。"
        msg2 = "{\"err_msg\": \"" + err_msg + "\"}"
        return HttpResponse(msg2) 
    else :
        res1 = convertMongoToJson(res) 
        res2 = "{\"msg\": \"ok\", \"paper_info\": " + res1 + "}"
        return HttpResponse(res2)

#获取相关论文
def getRelatedPaper(request):
    if (request.method!='GET'):
        return None
    dict = request.GET
    paperId = dict.get('paperId')
    result = database.getRelatedPaper(paperId)
    if (result == 'No results found' or result == 'database getRelatedPaper error'):
        res = "{\"msg\": \"" + result + "\"}"
        return HttpResponse(res)
    else:
        # res1 = "["
        # cnt = 0
        # for r in result:
        #     if (cnt == 0):
        #         res1 = res1 + r
        #     else:
        #         res1 = res1 + ", " + r
        #     cnt += 1
        # res1 = res1 + "]"
        # res = "{\"msg\": \"ok\", \"relatedPaperId\": " + res1 + "}"
        res2 = "["
        cnt = 0
        for o in result:
            paperId = o
            paper = database.getPaperInfo(paperId)
            if paper == 'database getPaperInfo error':
                return HttpResponse("{\"err_msg\": \"" + "获取专家全部论文失败！" + "\"}")
            if cnt == 0:
                res2 = res2 + convertMongoToJson(paper)
            else:
                res2 = res2 + "," + convertMongoToJson(paper)
            cnt = cnt + 1
        res2 = res2 + "]"
        return HttpResponse(res2)

#认领论文
def claimPaper(request):
    if request.method!='POST':
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")
    dict = request.POST
    if dict == None :
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")
    applicantId = dict.get('applicantId')
    uploadExpertId = dict.get('uploadExpertId')
    paperId = dict.get('paperId')

    try:
        applicant = Expert.objects.with_id(applicantId)
        workplace = applicant.workplace
        expertName = applicant.expertName
        paperTitle = Paper.objects.with_id(paperId).paperTitle
        expertEmail = applicant.expertEmail
        message = Message(
            noticeBuildTime = datetime.now(),
            noticeType = "论文认领",
            noticeContent = "来自 "+workplace+" 的"+expertName+" 希望认领您的论文：《 "+paperTitle+" 》，对方邮箱为 "+expertEmail,
            noticePlusContent = paperId,
            noticeRead = "not",
        )
        uploadUser = Expert.objects.with_id(uploadExpertId).user
        result = database.sendAMessage(uploadUser,message)
        if (result != True):
            res = "{\"msg\": \"" + result + "\"}"
            return HttpResponse(res)
    except Exception:
        return HttpResponse("{\"msg\": \"" + 'database claimPaper error' + "\"}")
    return HttpResponse("{\"msg\": \"" + 'ok' + "\"}")

#通过认领
def passClaim(request):
    if request.method!='POST':
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")
    dict = request.POST
    if dict == None :
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")
    paperId = dict.get('paperId')
    expertEmail = dict.get('expertEmail')

    try:
        paper = Paper.objects.with_id(paperId)
        paperTitle = paper.paperTitle
        message = Message(
            noticeBuildTime = datetime.now(),
            noticeType = "论文认领",
            noticeContent = "您认领的论文：《 "+paperTitle+" 》已经认领成功",
            noticePlusContent = paperId,
            noticeRead = "not",
        )
        applicant = Expert.objects(expertEmail = expertEmail).first()
        applicant.paperList.append(paper)
        applicant.save()
        applicantUser = applicant.user
        result = database.sendAMessage(applicantUser,message)
        if (result != True):
            res = "{\"msg\": \"" + result + "\"}"
            return HttpResponse(res)
    except Exception:
        return HttpResponse("{\"msg\": \"" + 'database passClaim error' + "\"}")
    return HttpResponse("{\"msg\": \"" + 'ok' + "\"}")

#拒绝认领
def refuseClaim(request):
    if request.method!='POST':
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")
    dict = request.POST
    if dict == None :
        return HttpResponse("{\"err_msg\": \"" + "请求失败" + "\"}")
    paperId = dict.get('paperId')
    expertEmail = dict.get('expertEmail')

    try:
        paperTitle = Paper.objects.with_id(paperId).paperTitle
        message = Message(
            noticeBuildTime = datetime.now(),
            noticeType = "论文认领",
            noticeContent = "您认领的论文：《 "+paperTitle+" 》被对方拒绝",
            noticePlusContent = paperId,
            noticeRead = "not",
        )
        applicant = Expert.objects(expertEmail = expertEmail).first().user
        result = database.sendAMessage(applicant,message)
        if (result != True):
            res = "{\"msg\": \"" + result + "\"}"
            return HttpResponse(res)
    except Exception:
        return HttpResponse("{\"msg\": \"" + 'database refuseClaim error' + "\"}")
    return HttpResponse("{\"msg\": \"" + 'ok' + "\"}")