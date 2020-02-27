from . import *


class rentalsunited:

	def __init__(self):
		self.username = 'petraluxuryrentals@gmail.com'
		self.password = 'Bol@Bol1995'
		self.url = url = "http://rm.rentalsunited.com/api/Handler.ashx"
		self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}


	def blockCalendar(self, pid, startDate, endDate, status):
		#when status is false, calendar will be blocked 
		payload = "\n<Push_PutAvb_RQ>\n <Authentication>\n <UserName>{}</UserName>\n <Password>{}</Password>\n </Authentication>\n <Calendar PropertyID=\"{}\">\n <Availability DateFrom=\"{}\" DateTo=\"{}\">{}</Availability>\n </Calendar>\n</Push_PutAvb_RQ>"
		payload = payload.format(self.username, self.password, pid, startDate, endDate, status)
		response = requests.request("GET", self.url, headers=self.headers, data = payload)
		tree = ET.fromstring(response.text)
		responseStatus = tree[0].get("ID")
		print(startDate, " ", endDate)
		print(responseStatus)
		print(response.text)
		return responseStatus

	def putMinStay(self, pid, startDate, endDate, minStay):
		payload = "<Push_PutMinstay_RQ>\n<Authentication>\n <UserName>{}</UserName>\n <Password>{}</Password>\n </Authentication>\n  <PropertyMinStay PropertyID=\"{}\">\n  \t<MinStay DateFrom=\"{}\" DateTo=\"{}\">{}</MinStay>\n  \t </PropertyMinStay>\n</Push_PutMinstay_RQ>"
		payload = payload.format(self.username, self.password, pid, startDate, endDate, minStay)
		response = requests.request("GET", self.url, headers=self.headers, data = payload)
		tree = ET.fromstring(response.text)
		responseStatus = tree[0].get("ID")
		print(startDate, " ", endDate)
		print(responseStatus)
		print(response.text)
		return responseStatus

	def tryPutMinStay(self, pid, startDate, endDate, minStay):
		try:
			self.putMinStay(pid, startDate, endDate, minStay)
			print("minimum stay has been successfully added to the property: ", pid)
		except Exception as e:
			print(e)