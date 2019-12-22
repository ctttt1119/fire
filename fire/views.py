from django.shortcuts import render,HttpResponse
from .models import *
from .database import *
from datetime import datetime
from . import database

def hello(request):
    
    

    # value = "2019-12-16T00:00:00Z"
    # date = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    # paper = Paper.objects(paperTitle = "testPaper").first()
    # paper.paperTime = date
    # paper.save()
    
    
    # 获取一个用户
    # user = User.objects(username = 'user100').first()
    # # 新建一个message对象
    # message = Message(
    #     noticeBuildTime = datetime.now(),
    #     noticeType = "type",
    #     noticeContent = "test",
    #     noticePlusContent = "www.baidu.com",
    #     noticeRead = "not",
    # )
    # #在用户的messages中添加这个对象
    # user.messages.append(message)
    # user.save()

    # # # 可以通过描述一个message找到拥有这个message的user
    # message = Message(
    #     noticeBuildTime = datetime.strptime("2019-12-18T07:11:42.137Z", '%Y-%m-%dT%H:%M:%S.%fZ'),
    #     noticeType = "type",
    #     noticeContent = "test",
    #     noticePlusContent = "www.baidu.com",
    #     noticeRead = "not",
    # )
    # user = User.objects(messages = message).first()

    # # 也可以修改一个message
    # # 但是需要知道这个message是messages数组的第几项
    # # 注意，最后需要保存的是user，而非message
    # message = user.messages[1]
    # message.noticeRead = 'yes'
    # user.save()


    # # expert = user.expert
    # # aim = expert.id
    # apply = Apply(
    #     applicant = user,
    #     applicantImage = "testImage",
    #     applicantWorkplace = "workplace1",
    #     applicantTitle = "title1",
    #     applicantName = "expert1",
    #     applicantEmail = "expert1@gmail.com",
    # )
    # apply.save()
    
    # patent = Patent(
    #     patentName = "test patent",
    #     patentNo = 0,
    #     patentTime = datetime.strptime("20191213","%Y%m%d"),
    #     patentAuthors = ["author1"],
    # )
    # patent.save()
    
    # 获取一个对象的id
    # tid = User.objects(username = '111').first().id

    # # 使用一个objectID查找对象
    # user = User.objects.with_id(tid)

    # return HttpResponse(register('111', 'testuser', '111', '111@qq.com'))
    
    # 插入数据
    
    


    # # 查询（注意：查询结果是一个列表），有则返回QuerySet，无则返回None
    # user = User.objects(username = "user2").first()

    # 使用外键插入新数据
    # expert = Expert(
    #     user = user,
    #     expertEmail = 'expert1@qq.com',
    #     identityImage = 'test1',
    #     workplace = 'test1',
    #     expertName = 'test1',
    # )
    # expert.save()

    # # # 更新一个字段的值 set__
    # # user.update(set__expert = expert)
    # 或者
    # user.expert = expert
    # user.save()

    # # List使用：[]
    # paper = Paper(
    #     uploadExpert = expert,
    #     paperTags = ['tag1','tag2','tag3'],
    #     DOI = '9901-sd28',
    #     paperTitle = 'testPaper',
    #     paperTime = '2019-12-4',
    #     paperUrl = 'www.baidu.com',
    #     paperAbstract = 'very good',
    #     quoteNum = 2,
    #     readNum = 3,
    #     starNum = 4,
    #     author = ['author1','author2']
    # )
    # paper.save()

    # upload_patent(
    #     1,
    #     111,
    #     ['cs'],
    #     '111',
    #     111,
    #     '2019-12-08',
    #     '111',
    #     111,
    #     111,
    #     ['author1','author2'])


    
    return HttpResponse("hello")

def testNotice(requset):
    # message = Message(
    #     noticeBuildTime = datetime.strptime("2019-12-18T07:11:42.137Z", '%Y-%m-%dT%H:%M:%S.%fZ'),
    #     noticeType = "fff",
    #     noticeContent = "fff",
    #     noticePlusContent = "fff",
    #     noticeRead = "not",
    # )
    # expertId = '5dfb710af91085db2d0bfbe4'
    # userId = '5dfb6c7e617dffa09d93ca42'
    # #database.noticeFollowers(expertId,message)
    # hello = database.noticeUser(userId,message)
    # expert = Expert.objects.with_id("5dfb710af91085db2d0bfbe4")
    # paper = Paper(
    #     uploadExpert = expert,
    #     paperTags = ['tag1','tag2','tag3'],
    #     DOI = '9901-109827372153',
    #     paperTitle = 'testPaper111',
    #     paperTime = '2019-12-4',
    #     paperUrl = 'www.baidu.com',
    #     paperAbstract = 'very good',
    #     quoteNum = 2,
    #     readNum = 3,
    #     starNum = 4,
    #     author = ['author1','author2']
    # )
    # paper.save()
    # database.noticeUser("5dfb8f37423d8402b2a368a9",message)

    # expert = Expert.objects.with_id("5dfb84fa01708a50d0d26aec")
    # paperList = expert.paperList
    # paper = Paper.objects.with_id("5dfbb32c59eecd624e4f6d47")
    # paperList.append(paper)
    # patent = Paper.objects.with_id("5dfbb32c59eecd624e4f6d48")
    # paperList.append(paper)
    # expert.save()

    # user = User(
    #     password = "fire",
    #     userIntro = "用于管理未在本平台注册的专家",
    #     username = "ExpertAdministration",
    #     nickname = "ExpertAdministration",
    #     userEmail = "5477814599@qq.com",
    # ) 
    # user.save()
    # user = User.objects.with_id("5dfdc390a89000267f4a1b3a")
    # expert = Expert(
    #     user = user,
    #     expertEmail = 'gate@gmail.com',
    #     identityImage = 'test',
    #     workplace = "International Conference on Document Analysis and Recognition",
    #     expertName = "B.Gatos",
    # )
    expert = Expert.objects.with_id("5dfe0e66fc3acce38d80be12")
    #expert.expertTitle = "Senior Researcher"
    # paper = Paper.objects.with_id("5dfbb32c59eecd624e4f6d56")
    # expert.paperList.append(paper)
    # paper = Paper.objects.with_id("5dfbb51bfc30ef1828e8bd29")
    # expert.paperList.append(paper)
    # paper = Paper.objects.with_id("5dfbb51cfc30ef1828e8c0a8")
    # expert.paperList.append(paper)
    # expert.paperNum = 3
    #expert.expertTags.append("algorithm")
    expert.identityImage = "none"
    expert.save()
    # user.expert = expert
    # user.save()

    return HttpResponse('hello')