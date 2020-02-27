from . import *


class sfReservation:

	def __init__(self, sfId, sfConnection):
		self.sf = sfConnection
		self.sfId = sfId
		self.reservationInfo = self.sf.Booking__c.get(self.sfId)
		self.startDate = self.reservationInfo['start_date__c']
		self.endDate = self.reservationInfo['End_Date__c']
		self.calendarEndDate = self.reservationInfo['CalendarEndDate__c']
		self.unitId = self.reservationInfo['Unit_RU_property_ID__c']
		self.unitSfId = self.reservationInfo['Unit__c']