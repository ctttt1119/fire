from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from fire import views
from fire import user
from fire import paper
from fire import patent
from fire import search
from fire import expert
from fire import apply

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.testNotice),
    
    path('api/apply/getAllApplyInfo',apply.getAllApplyInfo),
    path('api/apply/applyPassed',apply.applyPassed),
    path('api/apply/applyRefused',apply.applyRefused),
    path('api/apply/getApplyState',apply.getApplyState),
    
    path('api/expert/getExpertInfo',expert.getExpertInfo),
    path('api/expert/uploadApplyInfo',expert.uploadApplyInfo),
    path('api/expert/uploadImage',expert.uploadImage),
    path('api/expert/editExpertIntro',expert.editExpertIntro),
    path('api/expert/getExpertByExpertName',expert.getExpertByExpertName),
    path('api/expert/addPaper',expert.addPaper),
    path('api/expert/addPatent',expert.addPatent),

    path('api/paper/uploadPaper',paper.uploadPaper),
    path('api/paper/addPaperReading',paper.addPaperReading),
    path('api/paper/addPaperStar',paper.addPaperStar),
    path('api/paper/addPaperQuote',paper.addPaperQuote),
    path('api/paper/getPaperInfo',paper.getPaperInfo),
    path('api/paper/getRelatedPaper',paper.getRelatedPaper),
    path('api/paper/getAllPaperByExpertId',paper.getAllPaperByExpertId),

    path('api/patent/uploadPatent',patent.uploadPatent),
    path('api/patent/addPatentReading',patent.addPatentReading),    
    path('api/patent/addPatentStar',patent.addPatentStar),
    path('api/patent/getPatentInfo',patent.getPatentInfo),
    path('api/patent/getAllPatentByExpertId',patent.getAllPatentByExpertId),

    path('api/search/searchPaperByExpertName',search.searchPaperByExpertName),
    path('api/search/searchPatentByExpertName',search.searchPatentByExpertName),
    path('api/search/searchByKeyword',search.searchByKeyword),

    path('api/user/login',user.login),
    path('api/user/register',user.register),
    path('api/user/getUserInfo',user.getUserInfo),
    path('api/user/upgradeAdmin',user.upgradeAdmin),
    path('api/user/editNick',user.editNick),
    path('api/user/editUserIntro',user.editUserIntro),
    path('api/user/changePwd',user.changePwd),
    path('api/user/setNewNotice',user.setNewNotice),
    path('api/user/setOneNoticeRead', user.setOneNoticeRead),
    path('api/user/setAllNoticesRead', user.setAllNoticesRead),
    path('api/user/followExpert', user.followExpert),
    path('api/user/cancelFollow', user.cancelFollow),
    path('api/user/checkFollow', user.checkFollow),

    path('api/expert/addPaper',expert.addPaper),
    path('api/expert/addPatent',expert.addPatent),
    path('api/paper/claimPaper',paper.claimPaper),
    path('api/paper/passClaim',paper.passClaim),
    path('api/paper/refuseClaim',paper.refuseClaim)
]
