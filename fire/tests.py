from django.test import TestCase
import requests
import datetime
# Create your tests here.



# res = {
# "_id": "5df0c8c5b4ef5d232026c857",
# "expert": "5df48bc4c2df6a4bf5e94681",
# "password": "password2",
# "username": "user2",
# "nickname": "nick2",
# "userEmail": "user2@gmail.com"
# }
# res2 = {}
# for key, value in res.items():
#     if key != 'password':
#         res2[key] = value;
# print(res2)

res = requests.post('http://127.0.0.1:8000/api/user/register', 
                    data={"username":"qwe1234567", "nickname":"qwe1234567", "password":"qwe1234567", "userEmail":"qwe@1234567.com"})
print(res.text)
print(res.url)
res = requests.post('http://127.0.0.1:8000/api/user/register', 
                    data={})
print(res.text)
print(res.url)

# res = requests.post('http://127.0.0.1:8000/api/user/login', data={"username":"user2", "password":"password2"})
# print(res.text)
# print(res.url)
# res = requests.post('http://127.0.0.1:8000/api/user/login', data={"username":"user1", "password":"password1"})
# print(res.text)
# print(res.url)
# res = requests.post('http://127.0.0.1:8000/api/user/login', data={})
# print(res.text)
# print(res.url)
# res = requests.get('http://127.0.0.1:8000/api/user/login', params="{"username":"user1", "password":"password1"}")
# print(res.text)
# print(res.url)
# res = requests.post('http://127.0.0.1:8000/api/user/login', data={"username":"", "password":""})
# print(res.text)
# print(res.url)
# res = requests.get('http://127.0.0.1:8000/api/user/login', params={"ya si la", "liang fei fan"})
# print(res.text)
# print(res.url)

# res = requests.get('http://127.0.0.1:8000/api/user/getUserInfo', params={"userId":"5df0c8c5b4ef5d232026c857"})
# print(res.text)
# print(res.url)

def convert(dic_data):
    for key, value in dic_data.items():
        if key == 'messages':
            # print(1)
            for message in value:
                # print(2)
                # print(message)
                message['noticeBuildTime'] = str(message['noticeBuildTime'])
    return dic_data

def convert2(dic_data):
    # from bson import ObjectId
    for key, value in dic_data.items():
        # if isinstance(value, ObjectId):
        #     dic_data[key] = str(value)
        if key == 'messasges':
            for message in value:
                message['noticeBuildTime'] = str(message['noticeBuildTime'])
    return dic_data

print(convert({'_id': '5dfaf7c4d9b4df08623b9306',
 'identity': 'user',
 'messages': [{'noticeBuildTime': datetime.datetime(2019, 12, 19, 4, 22, 31, 976000),
               'noticeContent': 'content1',
               'noticePlusContent': 'pluscontent1',
               'noticeRead': 'not',
               'noticeType': 'type'}],
 'nickname': 'nickname1001',
 'password': 'password1001',
 'userEmail': 'user1001@gmail.com',
 'username': 'user1001'}))

try:
    user = User.objects.filter(username='wyx')
except Exception:
    return 'database getApplyState error1'
try:
    apply = Apply.objects.filter(applecant = user)
except Exception:
    return 'database getApplyState error2'
try:
    state = apply.resultType
except Exception:
    return 'database getApplyState error13'
print(state)
print(type(state))
