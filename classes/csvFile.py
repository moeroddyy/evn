from . import *


class csvFile: 

	def __init__(self, pathToFile):
		self.propertyID = {
		  "Evon | Back Bay Convention CTR | Cozy Studio S9": "2500628", #B9
		  "Evon | Back Bay Convention CTR | Beautiful 1BR S4": "2500624", #B4
		  "Evon | Back Bay Convention CTR | Beautiful 1BR S1": "2498382", #B1
		  "Evon | Back Bay Convention CTR | Modern 1BR S52": "2500627", #1.B5
		  "Evon | Back Bay Convention CTR | Gorgeous 1BR S5" : "2500627", #2.B5
		  "Evon | Back Bay Convention CTR | Beautiful 1BR S14" : "2551193", #6blackwood-314
		  "Evon | Back Bay | Lux Penthouse + City View S06": "2500629", #406
		  "Evon | Back Bay | Lux Penthouse + City View S08": "2500630", #408
		  "Beautiful Penthouse with a Stunning City View": "2500630", #2.408
		  "Evon | Boston Commons | Stunning Huge Studio b14": "2096645", #114
		  "Evon | Downtown Boston | Beautiful Huge Studio b24": "2096645", #114
		  "Evon | Boston Commons | Gorgeous 2BR + Subway b15": "2426037", #215
		  "Gorgeous 2BD/1BA in Boston Theatre District": "2426037", #215
		  "Gorgeous 4BD/3BA Reunion Resort Near DisneyLand": "2096871", #orlando
		  "Gorgeous 3BD/2BA Vacation House in the Vineyard": "2096872", #vineyard
		  "Stunning 3BD/2BA Vacation House in the Vineyard": "2096872", #vineyard
		  "Stunning 3BD/2BA Vacation House in the Vineyard": "2096872", #vineyard
		  "Stunning 3BD/3BA in Jamaica Plain": "2256451", #43Mozart 
		  "Stunning 3BD/3BA in Jamaica Plain": "2256451", #43Mozart
		  "Evon | Boston Commons | Gorgeous 1BR + Subway b81": "2360649", #814
		  "Evon | Boston Commons | Gorgeous 1BR + Subway b81": "2360649", #814
		  "Massive Stunning 1BD/1BA in Fenway Area": "2332905", #875Beacon
		  "Luxury 1BD/1BA in the W ICON FREE SPA/GYM/POOL":"2520100", #485-3106
		  "Evon | SouthEnd | Luxury Apt | Boston Medical" : "2531480", #1661Washington st 
		  "Evon | Downtown | SoWa | Luxury 2BR/2BA + Art F3" : "2557518", #460-330
		  "Evon | Fenway Park | Luxury Apt | BU & NEU" : "2218105", #The viridian
		  "Evon - Downtown Boston - Stunning Apt Near Subway" : "2596267", #62boylston-316
		  "Evon - Boston Common - Gorgeous Apt Near Subway" : "2596268", #62boylston-326
		  "Evon - Boston Common - Beautiful Apt Near Subway" : "2596269", #62boylston-210
		  "Evon - Downtown - Gorgeous 2BD/2BA Apt Near Subway" : "2597799", #40Boylston-506
		  "Evon - Downtown - Stunning 2BD/1BA Apt Near Subway" : "2602269"	#40Boylston-605

		}
		self.reservationsDict = {}
		self.pathToFile = pathToFile
		self.openFile()
		self.fixSheet()


	def openFile(self):
		try:
			with open(self.pathToFile) as csv_file:
				reader = csv.DictReader(csv_file)
				self.reservationsDict = list(reader)
				csv_file.close()

		except Exception as e:
			print("error in processing the csv file to take the reservation codes")
			print(e)


	def fixPhoneNumber(self):
		for reservation in self.reservationsDict:
			reservation['Contact'] = reservation['Contact'][1:]
			#print(reservation['Contact'])

	def fixPrice(self):
		for reservation in self.reservationsDict:
			reservation['Earnings'] = reservation['Earnings'][1:]
			reservation['Earnings'] = reservation['Earnings'].replace(",", "")
			#print(reservation['Earnings'])

	def fixName(self):
		for reservation in self.reservationsDict:
			temp = reservation['Guest name'].split()
			reservation.update({'First Name':temp[0], 'Last Name':temp[1]})
			del reservation['Guest name']

	def fixUnitName(self):
		for reservation in self.reservationsDict:
			if reservation['Listing'] in self.propertyID:
				reservation['Listing'] = self.propertyID.get(reservation['Listing'])

	def fixStatus(self):
		for reservation in self.reservationsDict:
			if reservation['Status'] == 'Confirmed':
				reservation['Status'] = '1'
			elif reservation['Status'] == 'Canceled':
				reservation['Status'] = '2'

	def fixSheet(self):
		self.fixPhoneNumber()
		self.fixPrice()
		self.fixName()
		self.fixUnitName()
		self.fixStatus()