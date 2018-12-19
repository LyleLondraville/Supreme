import requests, json, time 
from threading import Thread 

class AntiCaptcha:

	
	def __init__(self, clientKey, siteKey, url ):
		self.antiKey = clientKey
		self.siteKey = siteKey
		self.url = url
		self.captchaList = []

	def makeCaptcha(self):
		
		data = json.dumps({
		    "clientKey": self.antiKey,
		    "task":
		        {
		            "type":"NoCaptchaTaskProxyless",
		            "websiteURL":self.url,
		            "websiteKey":self.siteKey
		        }
		})

		r = requests.post('http://api.anti-captcha.com/createTask', data = data)

		taskID = json.loads(r.text)['taskId']
		
		data2 = json.dumps({
			"clientKey": self.antiKey,
			"taskId" : taskID})

		while True :
			r = requests.post('https://api.anti-captcha.com/getTaskResult', data = data2)
			j = json.loads(r.text)
			#print j['status']
			if j['status'] != 'processing':
				statusJson = json.loads(json.dumps(j))
				solution = json.loads(json.dumps(statusJson['solution']))['gRecaptchaResponse']
				break 
			else :
				pass 

			time.sleep(.5)

		self.captchaList.append(solution)

	def genCaptcha(self, number):
		for i in range(0, number):
			Thread(target = self.makeCaptcha, args = ()).start()

	def getGenList(self):
		return self.captchaList




i = AntiCaptcha("", "", "")

i.genCaptcha(3)

#i.makeCaptcha()

while len(i.getGenList()) != 3 :
	print (i.getGenList())
	time.sleep(.5)


print (i.getGenList())










