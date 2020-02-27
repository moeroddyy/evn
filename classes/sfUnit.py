from . import *

class sfUnit:
	def __init__(self, sf, sfUnitId=None, unitRuId=None):
		self.sf = sf
		if sfUnitId != None and unitRuId == None:
			self.sfId = sfUnitId
			self.unitInfo = self.sf.Unit__c.get(self.sfId)
			self.ruId = self.unitInfo['RU_Property_ID__c'] #RU Property Id

		elif sfUnitId == None and unitRuId != None:
			self.ruId = unitRuId
			self.unitInfo = self.sf.Unit__c.get_by_custom_id('Name',self.ruId)
			self.sfId = self.unitInfo['Id']

		else:
			print("error in sfUnit object, check arguments passed.")
