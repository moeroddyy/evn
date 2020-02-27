from . import *


class submission:

	def __init__(self, sub):
		self.wasCheckInFormFilled = True
		self.entryId = sub['EntryId']
		self.entryIP = sub['IP']
		self.sfId = sub['Field241']
		self.bookingChannel = sub['Field18']
		self.enteredConfirmationCode = sub['Field30']
		self.numberOfGuests = sub['Field32']
		self.earlyCheckIn = sub['Field139']
		self.lateCheckOut = sub['Field140']
		self.babyCrib = sub['Field141']
		self.approxCheckIn = sub['Field35']
		self.approxCheckOut = sub['Field242']
		self.firstName =  sub['Field3']
		self.lastName = sub['Field4']
		self.phoneNumber = sub['Field11']
		self.comments = sub['Field244'] 
		self.email = sub['Field12']
		self.stAddress = sub['Field5']
		self.stAdress2 = sub['Field6']
		self.city = sub['Field7']
		self.state = sub['Field8']
		self.zipCode = sub['Field9']
		self.country = sub['Field10']
		self.frontId = sub['Field22']
		self.backId = sub['Field23']
		self.dateCreated = sub['DateCreated']
		self.createdBy = sub['CreatedBy']
		self.dateUpdated = sub['DateUpdated']
		self.updatedBy = sub['UpdatedBy']
		self.fixFields()
		self.mappings = self.creatMappings()
		
		
	def printVariables(self):
		print(ppretty(self,seq_length=50))

	def fixFields(self):
		if self.sfId == "":
			print("wtf")
			self.sfId = 'No SF ID has been provided to the form'
		else:
			pass
			#print(self.sfId)

		if self.babyCrib == "Baby Crib - 35$ ":
			self.babyCrib = 1
		else:
			self.babyCrib = 0

		if self.earlyCheckIn == "Early Check-In 2:00pm-4:00pm --35$":
			self.earlyCheckIn = 1
		else:
			self.earlyCheckIn = 0

		if self.lateCheckOut == "Late Check-out 11:30am - 2:00pm --35$":
			self.lateCheckOut = 1
		else:
			self.lateCheckOut = 0

		self.dateCreated = self.dateCreated[:10]
		self.dateUpdated = self.dateUpdated[:10]
		#print("checkin")
		#print(self.approxCheckIn)
		#print("checkout")
		#print(self.approxCheckOut)

		if self.approxCheckIn == '':
			self.approxCheckIn = '00:00:00'
			self.approxCheckIn = datetime.datetime.strptime(self.approxCheckIn, "%H:%M:%S")
			self.approxCheckIn = datetime.datetime.strftime(self.approxCheckIn, "%H:%M:%S")
		else:
			self.approxCheckIn = datetime.datetime.strptime(self.approxCheckIn, "%H:%M:%S")
			self.approxCheckIn = self.approxCheckIn - datetime.timedelta(hours=5)
			self.approxCheckIn = self.approxCheckIn + datetime.timedelta(days=3650)
			self.approxCheckIn = datetime.datetime.strftime(self.approxCheckIn, "%H:%M:%S")

		if self.approxCheckOut == '':
			self.approxCheckOut = '00:00:00'
			self.approxCheckOut = datetime.datetime.strptime(self.approxCheckOut, "%H:%M:%S")
			self.approxCheckOut = datetime.datetime.strftime(self.approxCheckOut, "%H:%M:%S")
		else:
			self.approxCheckOut = datetime.datetime.strptime(self.approxCheckOut, "%H:%M:%S")
			self.approxCheckOut = self.approxCheckOut - datetime.timedelta(hours=5)
			self.approxCheckOut = self.approxCheckOut + datetime.timedelta(days=3650)
			self.approxCheckOut = datetime.datetime.strftime(self.approxCheckOut, "%H:%M:%S")


	def creatMappings(self):
		mappings = {
		'Wufoo_Address_1__c': self.stAddress,
		'Wufoo_Address_2__c': self.stAdress2,
		'Wufoo_Approx_Check_in__c': self.approxCheckIn,
		'Wufoo_Approx_Check_out__c': self.approxCheckOut,
		'Wufoo_Baby_Crib__c': self.babyCrib,
		'Wufoo_Back_Id__c': self.backId,
		'Wufoo_Booking_Channel__c': self.bookingChannel,
		'Wufoo_City__c': self.city,
		'Wufoo_Confirmation_Code__c': self.enteredConfirmationCode,
		'Wufoo_Country__c': self.country,
		'Wufoo_Created_By__c': self.createdBy,
		'Wufoo_Date_Updated__c': self.dateUpdated,
		'Wufoo_Early_Check_in__c': self.earlyCheckIn,
		'Wufoo_Email__c': self.email,
		'Wufoo_Entry_Id__c': self.entryId,
		'Wufoo_Entry_Ip__c': self.entryIP,
		'Wufoo_First_Name__c': self.firstName,
		'Wufoo_Form_Creation_Time__c': self.dateCreated,
		'Wufoo_Front_ID__c': self.frontId,
		'Wufoo_Last_Name__c': self.lastName,
		'Wufoo_Late_Check_out__c': self.lateCheckOut,
		'Wufoo_Number_of_Guests__c': self.numberOfGuests,
		'Wufoo_Phone_Number__c': self.phoneNumber,
		'Wufoo_State__c': self.state,
		'Wufoo_Updated_By__c': self.updatedBy,
		'Wufoo_ZipCode__c': self.zipCode,
		'Wufoo_Comments__c': self.comments,
		'Was_check_in_form_filled__c': self.wasCheckInFormFilled,
		}
		return mappings
		
