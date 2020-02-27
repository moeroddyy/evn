from . import *

class minStayProgram:

	def __init__(self, numOfDays, minStay):
		self.ru = rentalsunited()
		self.sf = sForce()
		self.today = datetime.datetime.now()
		self.nextDate = self.today + datetime.timedelta(days=numOfDays)
		self.minStay = minStay

	def getActiveMainUnits(self):
		return self.sf.grabAllActiveMainUnits()

	def createUnitObjects(self, unitLists):
		unitObjectList = []
		for unit in unitLists:
			unitObjectList.append(sfUnit(self.sf.sf, sfUnitId=unit))

		return unitObjectList

	def startProgram(self):
		unitList = self.getActiveMainUnits()
		unitObjectList = self.createUnitObjects(unitList)
		for unit in unitObjectList:
			self.ru.tryPutMinStay(unit.ruId, self.today.strftime("%Y-%m-%d"), self.nextDate.strftime("%Y-%m-%d"), self.minStay)



