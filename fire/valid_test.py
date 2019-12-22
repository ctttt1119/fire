import re
from . import database

def repeat_doi(DOI):

    res = database.findPaperDoi(DOI)
    if res:
        return "已有该DOI号的论文存在，上传失败"
    else:
        return "ok"

def repeat_patentNo(patentNo):
    res = database.findPatentNo(patentNo)
    if res:
        return "已有该专利号的专利存在，上传失败"
    else:
        return "ok"

def login(username, password):
    if (not username.isalnum()):
        return 'illegalUsername'
    else:
        if (not password.isalnum()):
            return 'illegalPassword'
        else:
            return 'ok'

def register(username, nickname, password, userEmail):
    if(not username.isalnum()):
        return 'illegalUsername'
    else:
        if(not nickname.isalnum()):
            return 'illegalNickname'
        else:
            if (not password.isalnum()) or (password.isalpha() or password.isdigit() or len(password) < 6):
                return 'illegalPassword'
            else:
                if(not re.match('^[0-9a-zA-Z\_\-\.]+@[0-9a-zA-Z]+(\.[0-9a-zA-Z]+){1,}$', userEmail)):
                    return 'illegalUserEmail'
                else:
                    return 'ok'
