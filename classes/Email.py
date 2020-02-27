from . import *


class Email:

	def __init__(self):
		self.server = smtplib.SMTP('smtp.gmail.com: 587')
		self.server.ehlo()
		self.server.starttls()
		self.server.login("server@evonifyllc.com", "Bol@Bol1995")

	def sendEmail(self,subject,msg):
		try:
			message = 'Subject: {}\n\n{}'.format(subject, msg)
			self.server.sendmail('server@evonifyllc.com','server@evonifyllc.com',message)
			print("email has been sent")
			self.server.quit()
		except Exception as e:
			print("email couldn't be send due to an error")
			print(e)

