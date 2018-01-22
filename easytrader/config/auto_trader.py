import requests
import random
'''
	交易

'''

'''
   API
'''
# tradeUrl = 'https://tradeh5.eastmoney.com/Trade/SubmitTrade'
# assetUrl = 'https://tradeh5.eastmoney.com/Assets/GetMyAssests'
api_asset='https://tradeh5.eastmoney.com/Assets/GetMyAssests'
api_login='https://tradeh5.eastmoney.com/Login/Authentication'
url_verify ='https://tradeh5.eastmoney.com/LogIn/YZM?randNum=%s'
url_get_uuid= 'https://tradeh5.eastmoney.com/LogIn/IsNeedValidCode'


# params = {
# 	'stockCode':'512000',
# 	'price':'1.000',
# 	'amout':'200',
# 	'tadeType':'B'
# }

sess = requests.Session()
r1 = sess.post(url_get_uuid)

if r1.text != 1:
	exit()
	
randNm = random.random()

r2 = sess.post(url_verify % randNm)

f = open('test.png','wb')
f.write(r2.content)
f.close()

code = input("输入验证码")

loginParms={
	'userId': '',
	'password': '',
	'identifyCode':code,
	'randNumber':randNm,
	'type':'Z', 			
	'holdOnlineIdx':'1'}

r3 = sess.post(api_login,data=loginParms)

r4 = sess.post(api_asset)

print(r4.content)



# cookies = {
	# 'Uuid':'ab534bc66752495dace6769e9aca3c80'
# }

# ret = requests.post(url,data=params,cookies=cookies)

# if ret.text['Status'] == 0:
	# print('Success')

'''
	登录状态
'''