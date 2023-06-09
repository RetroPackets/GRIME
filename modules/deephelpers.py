from subprocess import PIPE, run
import os, csv, re, sys, json, subprocess, socks, httplib2
import urllib.request as request

cyan = "\033[1;36;40m"
green = "\033[1;32;40m"
red = "\033[1;31;40m"
Y = '\033[1;33;40m'

def onionStatus(url):
	try:
	        proxy = httplib2.ProxyInfo(proxy_type=socks.PROXY_TYPE_SOCKS5, proxy_host='localhost', proxy_port=9050)
	        http = httplib2.Http(proxy_info=proxy, timeout=30)
	        resp = http.request(url, headers={'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})[0]
	        return resp.status
	except:
		return 404


def onionHTML(url):
	try:
		proxy = httplib2.ProxyInfo(proxy_type=socks.PROXY_TYPE_SOCKS5, proxy_host='localhost', proxy_port=9050)
		http = httplib2.Http(proxy_info=proxy, timeout=30)
		content = http.request(url, headers={'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})[1]
		return (
			str(content, 'utf-8')
			.replace('\t', ' ')
			.replace('\n', ' ')
			.replace('\r', ' ')
			.replace('\"', '')
		)
	except:
		return "None"

def onionExtractor(html,inputUrl):
        results,onions = [],[]
        regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.onion\/?[-a-zA-Z0-9@:%._\/+~#=]{1,256}"
        inputRegex = r"\"" + inputUrl + "?[-a-zA-Z0-9@:%._\/+~#=]{1,256}"
        inputMatches = re.finditer(inputRegex, html, re.MULTILINE)
        matches = re.finditer(regex, html, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
                url = (match.group())
                results.append(url)
                onions = list(set(results))
        for matchNum, match in enumerate(inputMatches,start=1):
                url = (match.group())
                results.append(url)
                onions = list(set(results))
        return onions

def ahmia():
	results = []
	regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.onion\/?[-a-zA-Z0-9@:%._\/+~#=]{1,256}"
	url = "https://ahmia.fi/address/"
	req = request.Request(url, data=None, headers={'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})

	with request.urlopen(req) as response:
		source = response.read()
	dataString = str(source)
	matches = re.finditer(regex, dataString, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		url = (match.group())
		results.append(url)
	return list(set(results))

def redditOnions():
	url = "https://www.reddit.com/r/onions/new.json?limit=10000000000000000000000000000000"
	req = request.Request(url, data=None, headers={'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})

	with request.urlopen(req) as response:
		source = response.read()
		data = json.loads(source)
	dataString = json.dumps(data)
	if "Traceback (most recent call last):" in dataString:
		redditOnions()
	else:
		regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.onion\/?[-a-zA-Z0-9@:%._\/+~#=]{1,256}"
		matches = re.finditer(regex, dataString, re.MULTILINE)
		results = []
		for matchNum, match in enumerate(matches, start=1):
			url = (match.group())
			results.append(url)
		return list(set(results))

def torstatus():
	torstatus = subprocess.getoutput("Service Tor Status | grep Active")
	torstatus = str(torstatus.split()[1])
	if torstatus == "inactive":
		os.system('systemctl tor restart')
	return torstatus

def rootcheck():
	check = subprocess.run(['whoami'],stdout=subprocess.PIPE)
	check = str(check.stdout.decode("utf-8").replace('\n','').strip())
	if check != "root":
		exit()
	return check

def urlSplitter(url):
	if ".onion" in url:
		directory = str(url.split(".onion")[1])
		url = str(url.split(".onion")[0]) + ".onion"
	elif ".com" in url:
		directory = str(url.split(".com")[1])
		url = str(url.split(".com")[0]) + ".com"
	elif ".org" in url:
		directory = str(url.split(".org")[1])
		url = str(url.split(".org")[0]) + ".org"
	else:
		print(f"{Y}Unknown URL {str(url)}")
		exit()
	if directory == "":
		directory = "/"
	if directory[0] == ":":
		split = directory.split("/")
		url = url+split[0]
		directory = split[1]
	return url,directory


def removeDuplicates(listOne, listTwo):
	return listOne + list(set(listTwo) - set(listOne))

def aTag(inputURL,html):
	if inputURL[-1] == "/":
		inputURL= inputURL[:-1]
	temp,temp2,results,onions = [],[],[],[]
	regex = r'<a href=?[-a-zA-Z0-9@:%._\+~#=/]{1,256}>'
	matches = re.finditer(regex, html, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		url = (match.group())
		results.append(url)
	onions = list(set(results))
	temp.extend(i.replace("<a href=","").replace(">","") for i in onions)
	for i in temp:
		if "http" in i:
			if ".onion" in i:
				temp2.append(i)
		elif "mailto:" in i:
			pass
		elif i.startswith("../"):
			i = i.replace("../", f"{inputURL}/")
			temp2.append(i)
		elif i.startswith("/"):
			temp2.append(inputURL+i)
		else:
			temp2.append(f"{inputURL}/{i}")
	return list(set(temp2))

def inputAdder(newInput, input):
        for i in input:
                if i not in newInput:
                        newInput.append(i)
        return newInput

def inputList():
	ahmiaLinks = ahmia()
	inputList = ['https://thehiddenwiki.com/','https://hiddenwiki.com','https://thehiddenwiki.org']
	reddit = redditOnions()
	results = removeDuplicates(inputList,ahmiaLinks)
	results = removeDuplicates(inputList,reddit)
	return results

def titlePrinter():
	os.system('clear')

	print(cyan +'''


████████████████████████████████████████████████████████████████████████████████████
█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░███░░░░░░░░░░█░░░░░░██████████░░░░░░█░░░░░░░░░░░░░░█
█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀░░█░░▄▀░░░░░░░░░░░░░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█
█░░▄▀░░░░░░░░░░█░░▄▀░░░░░░░░▄▀░░███░░░░▄▀░░░░█░░▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░░░░░░░░░█
█░░▄▀░░█████████░░▄▀░░████░░▄▀░░█████░░▄▀░░███░░▄▀░░░░░░▄▀░░░░░░▄▀░░█░░▄▀░░█████████
█░░▄▀░░█████████░░▄▀░░░░░░░░▄▀░░█████░░▄▀░░███░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█
█░░▄▀░░██░░░░░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░█████░░▄▀░░███░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█
█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░░░█████░░▄▀░░███░░▄▀░░██░░░░░░██░░▄▀░░█░░▄▀░░░░░░░░░░█
█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░███████░░▄▀░░███░░▄▀░░██████████░░▄▀░░█░░▄▀░░█████████
█░░▄▀░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░░░░░█░░░░▄▀░░░░█░░▄▀░░██████████░░▄▀░░█░░▄▀░░░░░░░░░░█
█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀▄▀▄▀░░█░░▄▀▄▀▄▀░░█░░▄▀░░██████████░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█
█░░░░░░░░░░░░░░█░░░░░░██░░░░░░░░░░█░░░░░░░░░░█░░░░░░██████████░░░░░░█░░░░░░░░░░░░░░█
████████████████████████████████████████████████████████████████████████████████████''')
	print(Y +'''
-----------------------------------------------------------------------------------------
|---------------------------------------------------------------------------------------|
|  HOW TO RUN : python3 grime.py			            		        |
|---------------------------------------------------------------------------------------|
| MODIFIED BY : RetroPackets                                                            |
|      GITHUB : https://gtihub.com/RetroPackets                                         |
|---------------------------------------------------------------------------------------|
|     TOOL BY : Conso1eCowb0y
-----------------------------------------------------------------------------------------''')
	print(red + """YOU MUST RUN THIS TOOL AS ROOT [sudo python3 grime.py]
""")


def deepSearchTitle():
	os.system('clear')

