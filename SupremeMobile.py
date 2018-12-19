import requests, json, time
from enum import Enum


## Recomended timeout is 3.2 sec

class options(Enum):
	
	BAGS = 'Bags'
	JACKETS = 'Jackets'
	SHIRTS = 'Shirts'
	TOPS_SWEATSHIRTS = 'Tops/Sweaters'
	SWEATSHIRTS = 'Sweatshirts'
	PANTS = 'Pants'
	HATS = 'Hats'
	ACCESSORIES = 'Accessories'
	SKATE = 'Skate'

	SMALL = 'Small'
	MEDIUM = 'Medium'
	LARGE = 'Large'
	XLARGE = 'XLarge'
	OS = 'N/A'

	WHITE = 'White'
	YELLOW = 'Yellow'
	PINK = 'Pink'
	BLUE = 'Blue'
	RED = 'Red'
	BLACK = 'Black'
	PURPLE = 'Purple'
	GREY = 'Grey'
	GREEN = 'Green'
	PEACH = 'Peach'
	NAVY = 'Navy'

	CHECKOUT1 = {
	'name':' ',
	'email':'',
	'tel':'',
	'addy1':'',
	'addy2':'',
	'zip':'',
	'city':'',
	'stateInitals':'',
	'cardType':'',
	'cardNumber':'',
	'cardExpMonth':'',
	'cardExpYear':'',
	'cardCVV':''}



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

class SupremeShredder :

	def __init__(self):

		self.superMasterDict = {}
		
		self.MobilHeaders = {
			'Host':'www.supremenewyork.com',                                                                   
			'Accept-Encoding':'gzip, deflate',                                                                            
			'Connection':'keep-alive',                                                                  
			'Proxy-Connection':'keep-alive',                                                                               
			'Accept':'application/json',                                                                         
			'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML,like Gecko) Mobile/14B100',                                                    
			'Accept-Language':'en-us',                                                                                    
			'X-Requested-With':'XMLHttpRequest'}


	def jLoad(self, j):
		return json.loads(json.dumps(j))

	def t(self):
		return time.strftime('%H:%M:%S',time.localtime())


	def stocky(self, proxyList, timeout):

		headers = self.MobilHeaders
		self.update = False 
		n = 0
		
		inital = requests.get('http://www.supremenewyork.com/mobile_stock.json', headers = headers)  

		while self.update == False :

			time.sleep(timeout)
			
			final = requests.get('http://www.supremenewyork.com/mobile_stock.json', headers = headers, proxies = proxyList[n])

			if final.status_code == 200 :

				if final.text == inital.text:
					print (('{} - No changes found, continuing to refresh under proxy {}').format(self.t(), proxyList[n].values()[0] ))
				
				else :
					print (('[{}] - Online shop update!').format(self.t()))
					self.update = True
			
			else :
				print (('[{}] - 403 error with proxy {}').format(self.t(),  proxyList[n].values()[0] )) 
				n = (0 if n == len(proxyList) - 1 else n + 1)
				print (('[{}] : retrying with proxy {}').format( self.t(), proxyList[n].values()[0] ))
		
		return json.loads(final.text)['products_and_categories']


	def parsey(self, jObject, keyword, category, listOfList, name): 

		print ( ('[{}] : searching for id with keywords {}, in {}').format(self.t(), keyword, category) )

		parentPid = ''
		masterDictonary = {}
		headers = self.MobilHeaders
		jLoad = self.jLoad


		categoryJson = jLoad(jObject[category])   

		for item in categoryJson:
			j = jLoad(item)
			
			#if j['new_item'] == True :
			
			if all(kw in j['name'].lower() for kw in keyword):
				parentPid = str(j['id'])
				print ( ('[{}] : Found id {} with keywords {} in category {}!').format(self.t(), parentPid, keyword, category) )
				break 
				
			#	else :
			#		pass 
			
			#else :
			#	pass 

		
		if parentPid == '':
			print ( ('[{}] : Could not find a product with the keyword {} in the category {}').format( self.t(), keyword, category ) )
			return ''
		
		else :
			print ( ('[{}] : Loading json for id {}').format(self.t(), parentPid) )
			
			product = requests.get('http://www.supremenewyork.com/shop/%s.json' % parentPid, headers = headers)
			productjson = json.loads(product.text)

			for c in productjson['styles']:
				
				miniDictonary = {}
				colorDictonary = {}
				
				j = jLoad(c)

				color = str(j['name'])
				childPid = str(j['id'])


				for s in jLoad(j['sizes']):
					j = jLoad(s)
					
					name = str(j['name'])
					sID = str(j['id'])

					miniDictonary.update({ name : sID })
				
				masterDictonary.update({ color : { childPid : miniDictonary } })
				

			print ( ('[{}] : Created dicotnary for id {}').format(self.t(), parentPid) )
			

		for c in listOfList:
			Thread(target = self.boty, args = (c[0], c[1], c[2], c[3], captcha, masterDictonary, c[4]))



	def boty(self, name, timeout, color, size, captcha, masterDictonary, checkoutPreset):

		t1 = time.time()

		sesh = requests.Session()
		headers = self.MobilHeaders

		checkoutData = {
			'store_credit_id':'',          
			'from_mobile':'1',
			'same_as_billing_address':'1',
			'order[billing_name]': checkoutPreset['name'] ,
			'order[email]':checkoutPreset['email'],
			'order[tel]':checkoutPreset['tel'],
			'order[billing_address]':checkoutPreset['addy1'],
			'order[billing_address_2]': checkoutPreset['addy2'],
			'order[billing_zip]':checkoutPreset['zip'],
			'order[billing_city]':checkoutPreset['city'],
			'order[billing_state]':checkoutPreset['stateInitals'],
			'order[billing_country]':'USA',
			'store_address':'1',
			'credit_card[type]':checkoutPreset['cardType'],
			'credit_card[cnb]':checkoutPreset['cardNumber'],
			'credit_card[month]':checkoutPreset['cardExpMonth'],
			'credit_card[year]':checkoutPreset['cardExpYear'],
			'credit_card[vval]':checkoutPreset['cardCVV'],
			'order[terms]':'0',
			'g-recaptcha-response' : captcha}
			#'order[terms]':'1',
			#'hpcvv':'',
			#'commit':'process payment'}
		
		parentPid = masterDictonary.keys()[0]

		print ( ('[{}] : {} - Selecting size/color ID').format(self.t(), name) )
		
		for c, d in (masterDictonary.values()[0]).iteritems():
			if c == color :
				colorPid = d.keys()[0]
				for s, sid in (d.values()[0]).iteritems():
					if s == size :
						sizePid = sid
						break 

		print ( ('[{}] : {} - adding to cart with size ID {} and color ID {}').format(self.t(), name, sizePid, colorPid) )

		data = {
			'size' : sizePid,
			'style' : colorPid,
			'qty' : '1'
		}


		add = sesh.post( (('http://www.supremenewyork.com/shop/{}/add.json').format(parentPid)) , headers = headers, data = data)

		print ( ('[{}] : {} - Added to cart!').format(self.t(), name) )

		if add.text != []:
			addJson = json.loads(add.text)
			
			if addJson[0]['in_stock'] == True:
				
				timeout = (timeout - (time.time() - t1))

				time.sleep(timeout)

				checkout = sesh.post('https://www.supremenewyork.com/checkout.json', data = checkoutData, headers = headers)

				t2 = time.time()

				checkoutJSON = json.loads(checkout.text)

				info = self.jLoad(checkoutJSON)['info']
				rawPrice = str(info['item_total'] + info['shipping_total'])
				price = ('${}.00').format(rawPrice[0:len(rawPrice)-2])

				purchases = self.jLoad(self.jLoad(info)['purchases'][0])

				pName = purchases['product_name']
				color = purchases['style_name']
				sizeName = purchases['size_name']

				productDesk = (('{} {} {}').format(sizeName, color, pName))


				if checkoutJSON['status'] == 'paid':
					print (('[{}] : {} - Checkout complete, Checkout time : {} - Delay : {} - Product title : "{}" - Retail price : {}').format(self.t(), name, t2-t1, timeout, productDesk, price))
				
				else :
					print (('[{}] : {} - Failed to complete checkout, Checkout time : {} - Delay : {} - Product title : "{}" - Retail price : {}').format(self.t(), name, t2-t1, timeout, productDesk, price))
	

			else :
				print (('[{}] : {} - item OOS!').format(self.t(), name))
		else :
			print ('[{}] : {} - ID error!').format(self.t(), name)


o = options()
c = AntiCaptcha("", "", "")
s = SupremeShredder()

c.genCaptcha(3)

while len(c.getGenList()) != 3 :
	print "Checking for captchas...."

captcha = c.getGenList()

d1 = {
	'name':'Task1',
	'timeout':.25,
	'color' : o.WHITE,
	'size' : o.MEDIUM,
	'captcha' : captcha[0],
	'checkoutPreset' : o.CHECKOUT1}


mobileStock = s.stocky(['kw here'], .1)

Thread(s.parsey, args = (mobileStock, ['comme', 'des', 'garsons'], o.SHIRTS, 'CDG')).start()






inst = SupremeShredder()




































