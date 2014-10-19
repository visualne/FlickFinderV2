import requests
from bs4 import BeautifulSoup

#Adding user-agent headers
headers = {
    'User-Agent': 'Mozilla/5.0',
    'From': 'god@heaven.com'
}

#Get page
r = requests.get('http://www.fixedorbit.com/cgi-bin/cgirange.exe?ASN=14618',headers=headers)

soup = BeautifulSoup(r.text)

table = soup.find("table", { "width" : "100%" })




#This runs through each row in the table and pulls specific data
#from td tags in that table.
for row in table.findAll("tr"):
	cells = row.findAll("td")
	if len(cells) == 6:
		prefixLength = cells[1].find(text=True)
		networkAddress = cells[4].find(text=True)
		
		if prefixLength != 'Type':
			print networkAddress + prefixLength
