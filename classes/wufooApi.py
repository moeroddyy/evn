from . import *


class wufooApi:
	

	def __init__(self):
		self.params = {}
		self.subList = []
		self.baseUrl = 'https://evon.wufoo.com/api/v3/'
		self.checkinFormIdent = 'm6ipjmm1mdo3h9'
		self.username = 'TEEH-3DFC-NSDD-P45Z'
		self.password = 'Bol@@Bol1995'
		#self.createConnection()
		#self.subList = self.createSubObjects()
		
		#self.printSubObjectList()

	def createConnection(self):
		password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_manager.add_password(None, self.baseUrl, self.username, self.password)
		handler = urllib2.HTTPBasicAuthHandler(password_manager)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)
		#return urllib2

	def grabEntriesResponse(self, entryCount):
		requestLink = '/forms/{}/entries.json?system=True&pageStart={}&pageSize=100&sort=EntryId&sortDirection=DESC?'.format(self.checkinFormIdent, entryCount)
		response = urllib2.urlopen(self.baseUrl+requestLink)
		data = json.load(response)
		data = data.items()
		return data

	def createSubObjects(self, data):
		subList = []
		for sub in list(data)[0][1]:
			subObject = submission(sub)
			subList.append(subObject)
		return subList

	def getEntryCount(self):
		requestLink = 'forms/{}/entries/count.json'.format(self.checkinFormIdent)
		response = urllib2.urlopen(self.baseUrl+requestLink)
		data = json.load(response)
		return data['EntryCount']

	def printSubObjectList(self):
		for sub in self.subList:
			sub.printVariables()
