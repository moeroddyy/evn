from . import *


class sfRuCalendarBlockProgram:

	def __init__(self):
		self.sf = sForce()
		self.rentalsunited = rentalsunited()
		self.msg = ""

	def grabBookingsPerUnit(self, unitId, numOfDays):
		bookingsPerUnit = self.sf.grabAllBookingsPerUnit(unitId, numOfDays)
		return bookingsPerUnit
	
	def getReservationObject(self, sfId):
		#return the reservation object
		booking = sfReservation(sfId, self.sf.sf)
		return booking

	def blockRuCalendar(self, unitId):
		quotes = "'" #must add quotes to the unitID string for the query call 
		unitId = quotes + unitId + quotes
		for sfId in self.grabBookingsPerUnit(unitId, 14): #one sf api call
			booking = self.getReservationObject(sfId) # one sf api call
			print("sfId: ", booking.sfId,"unitId: ", booking.unitId)
			responseStatus = self.rentalsunited.blockCalendar(booking.unitId, booking.startDate, booking.calendarEndDate, 'false')
			if responseStatus != '0':
				self.msg = self.msg + "the reservation: " + str(sfId) + " couldn't block the calendar on RU for the unit: " + str(unitId) + " check-in: " + booking.startDate + " check-out: " + booking.endDate + "\n"

	def freeAllCalendar(self, unitId):
		#free all the calendar in case any cancellation is present # this function should be included twice a day as it's very slow
		today = datetime.datetime.now()
		for x in range(90):
			self.rentalsunited.blockCalendar(unitId, today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"), 'true')
			today = today + datetime.timedelta(days=1)

	def fixCalendarForOneUnit(self, unitId):
		print("Fixing the calendar for unit: ", unitId)
		print("***********************************")
		self.blockRuCalendar(unitId)
		print("\n")

	def sendEmail(self,msg):
		#sending an email 
		email  = Email()
		email.sendEmail("results of blocking the calendar for all units unit", self.msg)

	def getUnitPropertyId(self, unitSfId):
		ruPropertyId = sfUnit(self.sf.sf, sfUnitId=unitSfId).ruId
		return ruPropertyId

	def startProgram(self):
		print("starting the program for blocking and freeing the calendars")
		units = self.sf.grabAllActiveMainUnits() # one SF API CALL
		for unitSfId in units:
			ruPropertyId = self.getUnitPropertyId(unitSfId) # one API call x units.len()
			print(ruPropertyId)
			#self.freeAllCalendar(ruPropertyId) 
			self.fixCalendarForOneUnit(ruPropertyId)
