
from . import *


class airbnbSfSync:

	def __init__(self, scraper, sForce, reservationsDict):
		self.msg = ""
		self.mappings = {}
		self.sf = sForce.sf
		self.scraper = scraper
		self.reservationsDict = reservationsDict
		self.fixMappingAll()
		self.loopToPush()

	def recordExists(self, reservationID):
		try:
			log = self.sf.Booking__c.get_by_custom_id('Name', reservationID)
			return log['Id']
		except Exception as e:
			print(e)
			return False

	def grabUnitSfId(self, reservation):
		unit = sfUnit(self.sf, unitRuId=reservation['Unit__c'])
		return unit.sfId

	def pushToSalesForce(self, reservation):
		sfID = self.recordExists(reservation['Name'])
		subject = "result of extracting airbnb reservations"
		if sfID != False:
			self.msg = self.msg + "reservation has been skipped as it exists already " + reservation['Name'] + "\n"
			print("recrod already exists...will skip record for now", reservation['Name'])

		else:
			print("record doesn't exist... will create ")
			try:
				airbnbEmail = self.grabAirbnbEmail(reservation['Name'])
				self.addAirbnbEmail(reservation, airbnbEmail)
				self.sf.Booking__c.create(dict(reservation))
				print("reservation has been created", reservation['Name'])
				self.msg = self.msg + "reservation has been created " + reservation['Name'] + "\n"
			except Exception as e:
				self.msg = self.msg + "reservation couldn't be created due to an error" + reservation['Name'] + str(e) +"\n"
				print(e)

	def sendEmail(self, subject, msg):
		email = Email()
		email.sendEmail(subject, msg)


	def loopToPush(self):
		for reservation in self.reservationsDict:
			reservation['Unit__c'] = self.grabUnitSfId(reservation)
			self.pushToSalesForce(reservation)

		self.sendEmail("result of airbnb extraxction program", self.msg)
		self.scraper.endScraping()
		time.sleep(1)

	def grabAirbnbEmail(self, airbnbReservationCode):
		email = self.scraper.findEmail(airbnbReservationCode)
		print('email has been retrieved: ', email)
		return email

	def addAirbnbEmail(self, reservation, airbnbEmail):
		reservation.update({'guest_Email__c':airbnbEmail})
		print("email has been added")

		

	def fixMappingAll(self):
		for reservation in self.reservationsDict:
			self.fixMapping(reservation)

	def fixMapping(self, temp):

		temp.update({'Name':temp['Confirmation code'],
			'Reservation_Status__c':temp['Status'],
			'Guest_Phone_Number__c':temp['Contact'],
			'of_adults__c':temp['# of adults'],
			'of_children__c':temp['# of children'],
			'of_infants__c':temp['# of infants'],
			'start_date__c':temp['Start date'],
			'End_Date__c':temp['End date'],
			'of_nights__c':temp['# of nights'],
			'day_of_booking__c':temp['Booked'],
			'Unit__c':temp['Listing'],
			'Already_Paid__c':temp['Earnings'],
			'Currency__c':temp['Earnings'],
			'creator__c':'airbnb@rentalsunited.com',
			'Guest_FirstName__c':temp['First Name'],
			'Guest_LastName__c':temp['Last Name']})

		del temp['Confirmation code']
		del temp['Status']
		del temp['Contact']
		del temp['# of adults']
		del temp['# of children']
		del temp['# of infants']
		del temp['Start date']
		del temp['End date']
		del temp['# of nights']
		del temp['Booked']
		del temp['Listing']
		del temp['Earnings']
		del temp['First Name']
		del temp['Last Name']



	def printAllRes(self):
		for reservation in self.reservationsDict:
			print(reservation)


