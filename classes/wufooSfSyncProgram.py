from . import *


class wufooSfSyncProgram: 

	def __init__(self):
		self.sf = sForce()
		self.wufoo = wufooApi()

	def startProgram(self):
		self.wufoo.createConnection()
		entryCount = int(self.wufoo.getEntryCount())
		newCount = str(entryCount - 5)
		print(newCount)
		data = self.wufoo.grabEntriesResponse(newCount)
		subList = self.wufoo.createSubObjects(data)
		print(len(subList))

		for sub in subList:
			try:
				self.sf.updateBookingRecord(sub.sfId, sub.mappings)
			except Exception as e:
				print(e)