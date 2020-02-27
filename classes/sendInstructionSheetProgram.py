from . import *


class sendInstructionSheetProgram:

	def __init__(self):
		self.sf = sForce()
		self.today = datetime.datetime.now()
		self.afterThreeDays = self.today + datetime.timedelta(days=3)
		self.msg = "send sendInstructionSheetProgram" + "\n"
		print(self.today, self.afterThreeDays)

	def importRecords(self):
		queryConditions = "SELECT Id FROM Booking__c WHERE Reservation_Status__c = '1' and was_instruction_sheet_sent__c = False and Was_check_in_form_filled__c = True and IsPaid__c = True and start_date__c >= " + self.today.strftime("%Y-%m-%d") + " and start_date__c <= " + self.afterThreeDays.strftime("%Y-%m-%d")
		return self.sf.importRecords(queryConditions)

	def case1(self, res, unit):
		case1 = ["SELECT Id from Booking__c WHERE Reservation_Status__c = '1' and start_date__c <= ", res.startDate, " and End_Date__c > ", res.startDate ," and Unit__c = ", "'", unit.sfId, "'", " and Id != ", "'" , res.sfId, "'"]
		return self.sf.importRecords("".join(case1))

	def case2(self, res, unit):
		case2 = ["SELECT Id from Booking__c WHERE Reservation_Status__c = '1' and start_date__c < ", res.endDate, " and End_Date__c >= ", res.endDate ," and Unit__c = ", "'", unit.sfId, "'", " and Id != ", "'" , res.sfId, "'"]
		return self.sf.importRecords("".join(case2))

	def case3(self, res, unit):
		case3 = ["SELECT Id from Booking__c WHERE Reservation_Status__c = '1' and start_date__c >= ", res.startDate, " and End_Date__c <= ", res.endDate ," and Unit__c = ", "'", unit.sfId, "'", " and Id != ", "'" , res.sfId, "'"]
		return self.sf.importRecords("".join(case3))

	def updateBookingRecord(self, sfId):
		updateDict = {'Send_Check_in_Instructions__c': 1}
		self.sf.updateBookingRecord(sfId, updateDict)

	def sendEmail(self,msg):
		#sending an email 
		email  = Email()
		email.sendEmail("results of sendInstructionSheetProgram ", self.msg)

	def msgContent(self, sfId, i):
		# i = 1 -> pass alert
		# i = 2 -> double booking alert
		if i == 1:
			self.msg = self.msg + " Sending the instruction sheet for Reservation: " + sfId + "\n"
		if i == 2:
			self.msg = self.msg + " DOUBLE BOOKING ALERT FOR Reservation: " + sfId + "\n"




	def startProgram(self):
		for sfId in self.importRecords():
			res = sfReservation(sfId, self.sf.sf)
			unit = sfUnit(self.sf.sf, sfUnitId=res.unitSfId, )
			
			print("*************")
			print("unitRuID: ", unit.ruId)

			print("case1: ")
			if len(self.case1(res, unit)) == 0:
				print("case1 passed")
				print("case2: ")
				if len(self.case2(res, unit)) == 0:
					print("case2 passed")
					print("case3: ")
					if len(self.case3(res, unit)) == 0:
						print("case3 passed")
						self.updateBookingRecord(res.sfId)
						self.msgContent(res.sfId, 1)
					else:
						self.msgContent(res.sfId, 2)
						continue
				else:
					self.msgContent(res.sfId, 2)
					continue
			else:
				self.msgContent(res.sfId, 2)
				continue

		self.sendEmail(self.msg)





