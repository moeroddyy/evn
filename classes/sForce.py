from . import *

class sForce:

	def __init__(self):
		self.sf = Salesforce(username='petraluxuryrentals-cxv1@force.com', password='Evonify@@Evonify2020', security_token='Akkdxr4TF0sdRtDR9gEHiYEU')
		self.end = datetime.datetime.now(pytz.UTC)
		self.today = datetime.datetime.now()

	def importRecords(self, queryConditions):
		allRecords = []
		records = self.sf.query(queryConditions)
		for i in records['records']:
			allRecords.append(i['Id'])
		#print(allRecords)
		return allRecords


	def grabAllBookingsPerUnit(self, unitId, numOfDays):
		daysAgo = self.today - datetime.timedelta(days=numOfDays)
		daysAgo = daysAgo.strftime("%Y-%m-%d")
		queryConditions = "SELECT Id FROM Booking__c WHERE Reservation_Status__c = '1' and Don_t_Block_RU_Calendar__c = False and Unit_RU_property_ID__c = " + unitId + " and CalendarEndDate__c > " + daysAgo
		return self.importRecords(queryConditions)

	def grabAllActiveMainUnits(self):
		queryConditions = "SELECT Id FROM Unit__c WHERE Active__c = True and Main_Unit__c = True"
		return self.importRecords(queryConditions)

	def updateBookingRecord(self, sfId, updateDict):
		try:
			self.sf.Booking__c.update(sfId,updateDict)
			print("booking record: ", sfId, " Has been updated")
		except Exception as e:
			print("booking record couldn't update due to an error: ")
			print (e)

