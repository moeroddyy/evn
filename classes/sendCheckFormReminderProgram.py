from . import *


class sendCheckFormReminderProgram:

	def __init__(self):
		self.sf = sForce()
		self.today = datetime.datetime.now()

	def sendCheckinFormReminder(self):
		updateDict = {'Was_Check_in_form_reminder_sent__c': 0, 'Send_Check_in_form_reminder__c': 1}
		queryConditions = "SELECT Id FROM Booking__c WHERE Reservation_Status__c = '1' and 	Was_check_in_form_filled__c = False and was_check_in_form_sent__c = True and start_date__c > " + self.today.strftime("%Y-%m-%d")
		for sfId in self.sf.importRecords(queryConditions):
			res = sfReservation(sfId, self.sf.sf)
			print(res.sfId)
			self.sf.updateBookingRecord(res.sfId,updateDict)