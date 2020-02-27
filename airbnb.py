from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os 
import shutil
import glob
import datetime
import csv
from simple_salesforce import Salesforce
from collections import OrderedDict
import smtplib


class airbnbScraper:

	def __init__(self, page):
		self.sheet = None
		self.options = Options()
		self.options.binary_location = '/usr/bin/chromium-browser'
		self.options.headless = True
		self.options.add_argument('--user-data-dir=/home/moe/.config/chromium')
		self.downloadPath = "/home/moe/Desktop/airbnbSfSync/airbnbDownloads"
		self.emailPath1 = '//*[@id="site-content"]/div/div/div[2]/div/div/div[15]/div[1]/div[1]/div/div/div/span'
		self.emailPath2 = '//*[@id="site-content"]/div/div/div/div[2]/div[16]/div[1]/div[1]/div/div/div/span'
		self.prefs = {"download.default_directory" : self.downloadPath}
		self.options.add_experimental_option("prefs",self.prefs)
		self.driver = webdriver.Chrome('/home/moe/Desktop/airbnbSfSync/chromedriver', chrome_options=self.options)
		self.email = "customerservice@evonifyllc.com"
		self.password = "Moh*@Moh1995"
		self.allEmails = []
		self.enterLoginInfo()
		self.downloadReservations(page)
		self.changeFileName()
		self.sheet = csvFile()
		self.addAllEmails()
		self.exitBrowser()


	def enterLoginInfo(self):
		try:
			self.driver.get('https://www.airbnb.com/login/')
			username = self.driver.find_element_by_name("email")
			username.send_keys(self.email)
			time.sleep(1)
			password = self.driver.find_element_by_name("password")
			password.send_keys(self.password)
			time.sleep(1)
			self.driver.get_screenshot_as_file("capture.png")
			time.sleep(2)
			password.send_keys(Keys.RETURN);
			time.sleep(3)
			self.driver.get_screenshot_as_file("capture22.png")

		except Exception as e:
			print("couldn't enter username or password due to an error or page is already logged in")
			print(e)

	def downloadReservations(self, page):
		try:
			self.driver.get("https://www.airbnb.com/hosting/reservations/export.csv?sort_field=status&sort_order=asc&tab=upcoming&page=" + page)
			time.sleep(4)
			self.driver.get_screenshot_as_file("capture1.png")
			print("file has been downloaded")

		except Exception as e:
			print("file couldn't download due to an error")
			print(e)

	def changeFileName(self):
		try:
			list_of_files = glob.glob(self.downloadPath + "/*") # * means all if need specific format then *.csv
			latest_file = max(list_of_files, key=os.path.getctime)
			print (latest_file)
			newfile = "/home/moe/Desktop/airbnbSfSync/airbnbDownloads/" + datetime.date.today().strftime("%Y-%m-%d") + ".csv"
			os.rename(latest_file, newfile)
			print("file has been renamed")

		except Exception as e:
			print("file couldn't be renamed due to an error")
			print(e)

	def grabEmail(self, code):
		print(code)
		self.driver.get("https://www.airbnb.com/hosting/reservations/details/" + code)
		time.sleep(2)
		try:
			email = self.driver.driver.find_elements_by_class_name("_1jlnvra2");
			print("email has been retrieved")
			return email.text

		except Exception as e:
			print("email couldn't be retrieved")
			print(e)
			print("trying again")
			try:
				email = self.driver.find_element_by_xpath(self.emailPath2)
				print("email has been retrieved")
				return email.text
			except Exception as f:
				print("second try to retrieve email didn't work")
				print(f)

	def findEmail(self, code):
		#self.driver.get("https://www.airbnb.com/hosting/reservations/details/" + code)
		self.driver.get("https://www.airbnb.com/messaging/qt_for_reservation/" + code)
		time.sleep(5)
		print(code)
		try:
			temp = self.driver.find_element_by_css_selector('span._1jlnvra2')
			#print("element found")
			print(temp.text)
			return temp.text
		except Exception as e:
			print(e)
			try:
				print("trying again")
				temp = self.driver.find_element_by_xpath(self.emailPath1)
				print(temp.text)
				return temp.text
			except Exception as e:
				print("second try failed")
				print(e)

	def addAllEmails(self):
		try:
			for reservation in self.sheet.reservationsDict:
				email = ""
				email = self.findEmail(reservation['Confirmation code'])
				reservation.update({'Email':email})
				#print(self.sheet.reservationsDict[i])

			print("ALL EMAILS RETRIEVED")

		except Exception as e:
			print("couldn't retrieve emails due to an error")
			print(e)

	def exitBrowser(self):
		self.driver.quit()


class csvFile: 

	def __init__(self):
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
		self.reservations = []
		self.reservationsDict = {}
		self.pathToFile = "/home/moe/Desktop/airbnbSfSync/airbnbDownloads/" + datetime.date.today().strftime("%Y-%m-%d") + ".csv"
		#self.pathToFile = "/Users/moeroddy/desktop/programs/ruSync/airbnbdownloads/MissingReservationsAugust.csv"
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

	def getReservations(self):
		for reservation in self.reservationsDict:
			self.reservations.append(reservation['Confirmation code'])


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


class sfConnection:

	def __init__(self, scraper):
		self.msg = ""
		self.mappings = {}
		self.sf = Salesforce(username='petraluxuryrentals-cxv1@force.com', password='Evonify@@Evonify2020', security_token='Akkdxr4TF0sdRtDR9gEHiYEU')
		self.scraper = scraper
		self.fixMappingAll()
		self.loopToPush()

	def sendEmail(self,subject,msg):
		try:
			server = smtplib.SMTP('smtp.gmail.com: 587')
			server.ehlo()
			server.starttls()
			server.login("moe@evonifyllc.com", "Mohammed@Elkhatib1995")
			message = 'Subject: {}\n\n{}'.format(subject, msg)
			server.sendmail('moe@evonifyllc.com','moe@evonifyllc.com',message)
			print("email has been sent")
			server.quit()
		except Exception as e:
			print("email couldn't be send due to an error")
			print(e)


	def recordExists(self, reservationID):
		try:
			log = self.sf.Booking__c.get_by_custom_id('Name', reservationID)
			return log['Id']
		except Exception as e:
			print(e)
			return False

	def grabUnitSfId(self, reservation):
		unitSfId = self.sf.Unit__c.get_by_custom_id('Name',reservation['Unit__c'])["Id"]
		reservation['Unit__c'] = unitSfId

	def pushToSalesForce(self, reservation):
		sfID = self.recordExists(reservation['Name'])
		subject = "result of extracting airbnb reservations"
		if sfID != False:
			print("recrod already exists...will update record", reservation['Name'])
			del reservation['Unit__c']
			try:
				self.sf.Booking__c.update(sfID,dict(reservation))
				print("reservation has been updated ", reservation['Name'])
				self.msg = self.msg + "reservation has been updated " + reservation['Name'] + "\n"
			except Exception as e:
				self.msg = self.msg + "reservation couldn't update due to an error" + reservation['Name'] + str(e) +"\n"
				print(e)
		else:
			print("record doesn't exist... will create ")
			try:
				self.sf.Booking__c.create(dict(reservation))
				print("reservation has been created", reservation['Name'])
				self.msg = self.msg + "reservation has been created " + reservation['Name'] + "\n"
			except Exception as e:
				self.msg = self.msg + "reservation couldn't be created due to an error" + reservation['Name'] + str(e) +"\n"
				print(e)


	def loopToPush(self):
		for reservation in self.scraper.sheet.reservationsDict:
			self.grabUnitSfId(reservation)
			self.pushToSalesForce(reservation)

		self.sendEmail("result of airbnb extraxction program", self.msg)
		time.sleep(1)
		

	def fixMappingAll(self):
		for reservation in self.scraper.sheet.reservationsDict:
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
			'guest_Email__c':temp['Email'],
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
		del temp['Email']
		del temp['First Name']
		del temp['Last Name']



	def printAllRes(self):
		for reservation in self.scraper.sheet.reservationsDict:
			print(reservation)






scraper1 = airbnbScraper("1")
addData = sfConnection(scraper1)
print("****************************************")
scraper2 = airbnbScraper("2")
addData2 = sfConnection(scraper2)
print("****************************************")
scraper3 = airbnbScraper("3")
addData3 = sfConnection(scraper3)
print("****************************************")
