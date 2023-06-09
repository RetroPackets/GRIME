from modules.deephelpers import *
from modules.deepsqlite import *
import os
import random

cyan = "\033[1;36;40m"
green = "\033[1;32;40m"
red = "\033[1;31;40m"
Y = '\033[1;33;40m'

inputList = inputList()
titlePrinter()
check = rootcheck()
masterList = []
blacklist = ('http://76qugh5bey5gum7l.onion')
while len(inputList) > 0:
	if not os.path.exists("../output/deepminer.db"):
		deepminerDB = createDB()
	deepminerCon = connectDB()
	tables = createTables(deepminerCon)
	connectedOnions = []
	url = random.choice(inputList)
	torstatus()
	extensions = ('.jpg', 'jpeg', '.mp4', '.png', '.gif')
	if url not in masterList and not url.endswith(extensions) and not url.startswith(blacklist):
		print(Y +"""
[GRIME] New Iteration:""")
		print(green +"""
[GRIME] Currently Scanning """ + url)
		status = onionStatus(url)
		print(status)
		if status != 404:
			html = onionHTML(url)
			if html == "None":
				inputList.remove(url)
				print(red +"""
Returned TraceError. Moving to next URL
""")
			else:
				res = []
				onions = onionExtractor(html,url)
				atag = aTag(url,html)
				allonions = onions + atag
				onionResults = list(set(allonions))
				for site in onionResults:
					if site not in res:
						res.append(site)
				newList = inputAdder(onions,inputList)
				masterList.append(url)
				if url in newList:
					newList.remove(url)
				inputList = newList
				print(green +"""
[GRIME]Found Sites """ + str(len(res)))
				print(res)
				url,urlDir = urlSplitter(url)
				if urlDir == "":
					urlDir = "/"
				data = addDeepData(url,urlDir,html,deepminerCon)
				for connection in res:
					site,siteDir = urlSplitter(connection)
					if siteDir == "":
						siteDir = "/"
					connections = addDeepConnections(url,urlDir,site,siteDir,deepminerCon)
		else:
			inputList.remove(url)
			print(red +"""
URL gave bad response...not scanning
""")
	elif url in masterList:
		inputList.remove(url)
		print(url)
		print(Y +"""
URL already scanned
""")
	elif url.startswith(blacklist):
		inputList.remove(url)
		print(url)
		print(Y +"""
URL in blacklist
""")
	elif url.endswith(extensions):
		inputList.remove(url)
		print(url)
		print(red +"""
URL ends with extension not compatible
""")
