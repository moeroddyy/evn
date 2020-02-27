from classes import airbnbSfSync, airbnbScraper, sForce


scraper1 = airbnbScraper()
scraper1.setupDriver(0)
reservationsDict = scraper1.startScraping('1') #0 for scrape on mac #1 for scrape on server
sforce = sForce()
addData = airbnbSfSync(scraper1, sforce, reservationsDict)
print("************")
scraper2 = airbnbScraper()
scraper2.setupDriver(0)
reservationsDict = scraper2.startScraping('2') #0 for scrape on mac #1 for scrape on server
sforce = sForce()
addData = airbnbSfSync(scraper2, sforce, reservationsDict)
print("************")
scraper3 = airbnbScraper()
scraper3.setupDriver(0)
reservationsDict = scraper3.startScraping('3') #0 for scrape on mac #1 for scrape on server
sforce = sForce()
addData = airbnbSfSync(scraper3, sforce, reservationsDict)
