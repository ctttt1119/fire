from .models import *
import json
import datetime
from mongoengine.base import BaseDocument

#登录
def login(username, password):
    try:
        result = User.objects(username=username, password=password).first()
    except Exception:
        return 'database login error'
    if result:
        return result 
    else:
        return 'error'
#注册
def register(username, nickname, password, userEmail):
    try:
        result = User.objects.filter(username=username)
    except Exception:
        return 'database register error1'
    if result:
        return 'existUsername'
    try:
        result = User.objects.filter(userEmail=userEmail)
    except Exception:
        return 'database register error2'
    if result:
        return 'existUserEmail'
    try:
        User.objects.create(username=username, nickname=nickname, password=password, userEmail=userEmail)
    except Exception:
        return 'database register error3'
    try:
        result = User.objects(username=username).first()
    except Exception:
        return 'database register error4'
    if result:
        return result 
    else:
        return 'database register error' 
    

#搜索论文
def searchPaperByExpertName(expertName):
    # result = Paper.objects.filter(author__in = "author1")
    try:
        result = Paper.objects.filter(author=expertName)
    except Exception:
        return 'database searchPaperByExpertName error'
    if result:
        return result
    else:
        return 'No this expert paper'

#搜索专利
def searchPatentByExpertName(expertName):
    try:
        result = Patent.objects.filter(patentAuthors=expertName)
    except Exception:
        return 'database searchPatentByExpertName error'
    if result:
        return result
    else:
        return 'No this expert patent'

#上传论文
def uploadPaper(uploadExpertId,paperTags,DOI,paperTitle,paperTime,paperUrl,paperAbstract,quoteNum,readNum,starNum,author,authors_id,paperPublication):
    try:
        uploadExpert = Expert.objects.with_id(uploadExpertId)
        Paper.objects.create(uploadExpert=uploadExpert,paperTags=paperTags,DOI=DOI,paperTitle=paperTitle,paperTime=paperTime,paperUrl=paperUrl,paperAbstract=paperAbstract,quoteNum=quoteNum,readNum=readNum,starNum=starNum,author=author,paperPublication=paperPublication)
        res = Paper.objects.filter(DOI = DOI)
        for exp_id in authors_id:
            exp=Expert.objects.with_id(exp_id)
            list_tmp=exp.paperList
            list_tmp.append(res[0])
            exp.update(set__paperList=list_tmp)
    except NotUniqueError:
        return 'uploadPaper notUnique'
    except Exception:
        return 'database uploadPaper error'
    return res[0].id

#上传专利
def uploadPatent(uploadExpertId,patentTags,patentName,patentNo,patentTime,patentAbstract,readNum,starNum,patentAuthors,patentAuthors_id):
    try:
        uploadExpert = Expert.objects.with_id(uploadExpertId)
        Patent.objects.create(uploadExpert=uploadExpert,patentTags=patentTags,patentName=patentName,patentNo=patentNo,patentTime=patentTime,patentAbstract=patentAbstract,readNum=readNum,starNum=starNum,patentAuthors=patentAuthors)
        res = Patent.objects.filter(patentNo = patentNo)
        for exp_id in patentAuthors_id:
            exp=Expert.objects.with_id(exp_id)
            list_tmp=exp.paperList
            list_tmp.append(res[0])
            exp.update(set__patentList=list_tmp)
    except NotUniqueError:
        return 'uploadPatent notUnique'
    except Exception:
        return 'database uploadPatent error'
    return res[0].id

#上传专家认证资料
def uploadApplyInfo(userId,applicantImage,applicantName,applicantTitle,applicantWorkplace,applicantEmail,resultType,resultReason):    
    try:
        usr=User.objects.with_id(userId)
        if usr.expert is not None:
            return 'had expert'
        res=Apply.objects.create(applicant=usr,resultType=resultType,resultReason=resultReason,applicantImage=applicantImage,applicantWorkplace=applicantWorkplace,applicantTitle=applicantTitle,applicantName=applicantName,applicantEmail=applicantEmail)
    except Exception:
        return 'database uploadApplyInfo error'
    if res:
        return 'ok'
    else:
        return 'error'



#增加论文阅读量
def addPaperReading(paperId):
    try:
        res = Paper.objects.with_id(paperId).update(inc__readNum=1)
    except Exception:
        return 'database addPaperReading error'
    if res:
        return True
    else:
        return False

#增加论文引用量
def addPaperQuote(paperId):
    try:
        paper = Paper.objects.with_id(paperId)
        res=paper.update(inc__quoteNum=1)
    except Exception:
        return 'database addPaperQuote error'
    if res:
        return True
    else:
        return False

#增加专利阅读量
def addPatentReading(patentId):
    try:
        res = Patent.objects.with_id(patentId).update(inc__readNum=1)
    except Exception:
        return 'database addPatentReading error'
    if res:
        return True
    else:
        return False

#增加论文star
def addPaperStar(paperId):
    try:
        res = Paper.objects.with_id(paperId).update(inc__starNum=1)
    except Exception:
        return 'database addPaperStar error'
    if res:
        return True
    else:
        return False

#增加专利star
def addPatentStar(patentId):
    try:
        res = Patent.objects.with_id(patentId).update(inc__starNum=1)
    except Exception:
        return 'database addPatentStar error'
    if res:
        return True
    else:
        return False

#获取普通用户信息
def getUserInfo(userId):
    try:
        res = User.objects.with_id(userId)
    # res = User.objects.with_id(userId).first()
    except Exception:
        return 'database getUserInfo error'
    if res:
        return res
    else:
        return {}

#获取专家信息
def getExpertInfo(expertId):
    try:
        res = Expert.objects.with_id(expertId)
    except Exception:
        return 'database getExpertInfo error'
    if res:
        return res
    else:
        return {}


#获取论文信息
def getPaperInfo(paperId):
    try:
        res = Paper.objects.with_id(paperId)
    except Exception:
        return 'database getPaperInfo error'
    if res:
        return res
    else:
        return 'nothing'

#获取专利信息
def getPatentInfo(patentId):
    try:
        res = Patent.objects.with_id(patentId)
    except Exception:
        return 'database getPatentInfo error'
    if res:
        return res
    else:
        return {}

#根据expertName查找所有expert
def getExpertByExpertName(expertName):
    #return Expert.objects.find({"expertName":expertName}, {'paperList':0, 'patentList':0})
    try:
        res = Expert.objects.filter(expertName = expertName)
    except Exception:
        return 'database getExpertByExpertName error'
    if res:
        return res
    else:
        return {}

#按expertId查找全部论文
def getAllPaperByExpertId(expertId):
    try:
        res = list(Expert.objects.with_id(expertId).paperList)
    except Exception:
        return 'database getAllPaperByExpertId error'
    return res

#按expertId查找全部专利
def getAllPatentByExpertId(expertId):
    try:
        res = list(Expert.objects.with_id(expertId).patentList)
    except Exception:
        return 'database getAllPatentByExpertId error'
    return res

#按doi查找论文，看该论文是否已在数据库中，如果是则返回搜索结果，否则返回空
def findPaperDoi(DOI):
    #try:
    res = Paper.objects.filter(DOI=DOI).first()
    # except Exception:
    #     return 'database findPaperDoi error'
    if res:
        return res
    else:
        return []

#按专利号查找专利，看该专利是否已在数据库中，如果是则返回搜索结果，否则返回空
def findPatentNo(patentNo):
    try:
        res = Patent.objects.filter(patentNo=patentNo)
    except Exception:
        return 'database findPaperDoi error'
    if res:
        return res[0]
    else:
        return []

#根据keyword在expertName和achieveIntro中搜索匹配专家
def searchExpertByKeyword(kw):
    try:
    #ret = search_expert_by_expertName(kw) | search_expert_by_achieveIntro(kw)
        res = Expert.objects.filter(Q(expertName__contains = kw) | Q(achieveIntro__contains = kw))
    except Exception:
        return 'database searchExpertByKeyword error'
    if res == None:
        return []
    else:
        return res

#根据keyword在paperTitle和paperAbstract中搜索匹配论文
def searchPaperByKeyword(kw):
    try:
    #ret = search_paper_by_paperTitle(kw) | search_paper_by_paperAbstract(kw)
        res = Paper.objects.filter(Q(paperTitle__contains = kw) | Q(paperAbstract__contains = kw))
    except Exception:
        return 'database searchPaperByKeyword error'
    if res == None:
        return []
    else:
        return res

#根据keyword在patentName和patentAbstract中搜索匹配专利
def searchPatentByKeyword(kw):
    try:
    #ret = search_patent_by_patentName(kw) | search_patent_by_patentAbstract(kw)
        res = Patent.objects.filter(Q(patentName__contains = kw) | Q(patentAbstract__contains = kw))
    except Exception:
        return 'database searchPatentByKeyword error'
    if res == None:
        return []
    else:
        return res

#获取所有专家认证资料
def getAllApplyInfo():
    try:
        result = Apply.objects.all()
    except Exception:
        return 'database getAllApplyInfo error'
    if result:
        return result
    else:
        return 'getAllApplyInfo error'

#获取相关论文信息
def getRelatedPaper(paperId):
    try:
        res = []
        tags = Paper.objects.with_id(paperId).paperTags
        for r in tags:
            #tmp_ids = Paper.objects.filter(Q(paperTags__contains = r)).id
            papers = list(Paper.objects(paperTags=r))
            for paper in papers:
                tmp = paper.id
                res.append(tmp)
        res = res[0:5]
    except Exception:
        return 'database getRelatedPaper error'
    if res:
        return res
    else :
        return 'No results found'

#通过专家认证
def applyPassed(applyId,resultReason):
    try:
        apy = Apply.objects.with_id(applyId)
    except Exception:
        return 'database applyPassed error1'
    applicant = apy.applicant
    applicantEmail = apy.applicantEmail
    applicantImage = apy.applicantImage
    applicantWorkplace = apy.applicantWorkplace
    applicantTitle = apy.applicantTitle
    applicantName = apy.applicantName
    if apy.resultType == 'Passed':
        return 'had passed'
    elif apy.resultType == 'Refused':
        return 'had refused'
    try:
        res2 = Expert.objects.create(user=applicant,expertTags=[],achieveIntro="",expertEmail=applicantEmail,identityImage=applicantImage,workplace=applicantWorkplace,expertTitle=applicantTitle,expertName=applicantName)
    except Exception:
        return 'database applyPassed error2'
    try:
        expert = Expert.objects.filter(expertEmail=applicantEmail).first()
    except Exception:
        return 'database applyPassed error3'
    try:
        res3 = applicant.update(set__expert = expert)
    except Exception:
        return 'database applyPassed error4'
    try:
        res1 = apy.update(set__resultType = "Passed", set__resultReason = resultReason)
    except Exception:
        return 'database applyPassed error5'
    try:
        res4 = setNewNotice(applicant.id, "专家认证", "您的专家身份： "+applicantName+" - "+applicantWorkplace+" 已经认证成功！","")
    except Exception:
        return 'database applyPassed error6'
    if res1:
        if res2:
            if res3:
                if res4:
                    return True
    return False

#拒绝专家认证
def applyRefused(applyId,resultReason):
    try:
        apy = Apply.objects.with_id(applyId)
        if apy.resultType == 'Passed':
            return 'had passed'
        elif apy.resultType == 'Refused':
            return 'had refused'
        res = apy.update(set__resultType = "Refused", set__resultReason = resultReason)
    except Exception:
        return 'database applyRefused error'
    applicant = apy.applicant
    try:
        res2 = setNewNotice(applicant.id, "专家认证", "您的专家身份认证失败，请尝试填写更正规的内容，有助于管理员辨别。","")
    except Exception:
        return 'database applyRefused error2'
    if res:
        if res2:
            return True
    return False

#用户升级为管理员
def upgradeAdmin(userId):
    try:
        usr = User.objects.with_id(userId)
        res = usr.update(set__identity = "admin")
    except Exception:
        return 'database upgradeAdmin error'
    if res:
        return True
    else:
        return False

#用户修改昵称
def editNick(userId,newNickname):
    try:
        
        usr = User.objects.with_id(userId)
        res = usr.update(set__nickname = newNickname)
    except Exception:
        return 'database editNick error'
    if res:
        return True
    else:
        return False

#用户修改简介
def editUserIntro(userId,newUserIntro):
    try:
        usr = User.objects.with_id(userId)
        res = usr.update(set__userIntro = newUserIntro)
    except Exception:
        return 'database editUserIntro error'
    if res:
        return True
    else:
        return False

#用户修改密码
def changePwd(userId,newPassword):
    try:
        usr = User.objects.with_id(userId)
        res = usr.update(set__password = newPassword)
    except Exception:
        return 'database changePwd error'
    if res:
        return True
    else:
        return False

#专家修改简介
def editExpertIntro(expertId,newExpertIntro):
    try:
        exp = Expert.objects.with_id(expertId)
        res = exp.update(set__achieveIntro = newExpertIntro)
    except Exception:
        return 'database editExpertIntro error'
    if res:
        return True
    else:
        return False

# 为专家添加论文
def addPaperForExpert(expertId,paperId):
    try:
        expert = Expert.objects.with_id(expertId)
        paper = Paper.objects.with_id(paperId) 
        if expert==None or paper==None:
            return 'database notFound error'
        expert.paperList.append(paper)
        expert.save()
    except Exception:
        return 'database addPaperForExpert error'
    return True

# 为专家添加专利
def addPatentForExpert(expertId,patentId):
    try:
        expert = Expert.objects.with_id(expertId)
        patent = Patent.objects.with_id(patentId) 
        expert.patentList.append(patent)
        expert.save()
    except Exception:
        return 'database addPatentForExpert error'
    return True

# 生成消息
def setNewNotice(userId, noticeType, noticeContent, noticePlusContent):
    try:
        user = User.objects.with_id(userId)
    except Exception:
        return 'database setNewNotice error in search user'
    try:
        message = Message(
            noticeBuildTime = datetime.datetime.now(),
            noticeType = noticeType,
            noticeContent = noticeContent,
            noticePlusContent = noticePlusContent,
            noticeRead = "not",
        )
        user.messages.append(message)
        user.save()
    except Exception:
        return 'database setNewNotice error'
    # user.messages.append(message)
    # user.save()
    return 'ok'

# 一条消息已读
def setOneNoticeRead(userId, offset):
    try:
        user = User.objects.with_id(userId)
    except Exception:
        return 'database setOneNoticeRead error int search user'
    try:
        message = user.messages[int(offset)]
        message.noticeRead = "yes"
        user.save()
    except Exception:
        return 'database setOneNoticeRead error'
    return 'ok'
    # message = user.messages[int(offset)]
    # message.noticeRead = "yes"
    # user.save()
    # return 'ok'


# 所有消息已读
def setAllNoticesRead(userId):
    try:
        user = User.objects.with_id(userId)
    except Exception:
        return 'database setAllNoticesRead error int search user'
    try:
        for message in user.messages:
            message.noticeRead = "yes"
        user.save()
    except Exception:
        return 'database setAllNoticesRead error'
    return 'ok'

#用户关注专家
def followExpert(userId,expertId):
    try:
        user = User.objects.with_id(userId)
        exp = Expert.objects.with_id(expertId)
        res=Watch.objects.create(expert=exp,user=user)
    except Exception:
        return 'database followExpert error'
    if res:
        return True
    else:
        return False

#用户取消关注专家
def cancelFollow(userId,expertId):
    try:
        user = User.objects.with_id(userId)
        exp = Expert.objects.with_id(expertId)
        watch=Watch.objects.filter(Q(user=user) & Q(expert=exp)).first()
        res=watch.update(unset__user=1,unset__expert=1)
    except Exception:
        return 'database cancelFollow error'
    return True
    if res:
        return True
    else:
        return False

#判断用户是否关注专家
def checkFollow(userId,expertId):
    try:
        user = User.objects.with_id(userId)
        exp = Expert.objects.with_id(expertId)
        res= Watch.objects.filter(Q(user=user) & Q(expert=exp)).first()
    except Exception:
        return 'database checkFollow error'
    if res:
        return True
    else:
        return False

# 获取用户专家认证状态
def getApplyState(userId):
    try:
        user = User.objects.with_id(userId)
    except Exception:
        return 'database getApplyState error1'
    try:
        applies = Apply.objects.filter(applicant = userId)
    except Exception:
        return 'database getApplyState error2'
    try:
        flag = 1
        for apply in applies:
            if apply.resultType == 'unhandled':
                flag = 0
    except Exception:
        return 'database getApplyState error3'
    return flag
    # user = User.objects.with_id(userId)
    # applies = Apply.objects.filter(applicant = userId)
    # flag = 1
    # for apply in applies:
    #     if apply.resultType == 'unhandled':
    #         flag = 0
    # return flag




#群发消息
def broadcastMessage(users,message):
    if users != None:
        for user in users:
            try:
                user.messages.append(message)
                user.save()
            except Exception:
                return 'database writeMessage error'
    return True

#单发消息
def sendAMessage(user,message):
    if user != None:
        try:
            user.messages.append(message)
            user.save()
        except Exception:
            return 'database writeMessage error'
    return True

#获取关注某专家的所有用户
def getAllFollower(expertId):
    res = []
    try:
        expert = Expert.objects.with_id(expertId)
        watches = list(Watch.objects.filter(Q(expert = expert)))
        for watch in watches:
            res.append(watch.user)
    except Exception:
        return 'database getAllFollower error'
    if res:
        return res
    else:
        return None

#向关注某专家的所有用户发送消息
def noticeFollowers(expertId,message):
    users = getAllFollower(expertId)
    if (users!='database getAllFollower error'):
        #True or 'database writeMessage error'
        return broadcastMessage(users,message)
    else:
        return 'database noticeFollowers error'

#向某个用户发送消息
def noticeUser(userId,message):
    try:
        user = User.objects.with_id(userId)
    except Exception:
        return 'database noticeUser error'
    #True or 'database writeMessage error'
    return sendAMessage(user,message)


