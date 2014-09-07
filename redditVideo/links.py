from pprint import pprint
import requests
import json
import time
import sys

#Grabbing links off of page
r = requests.get(r'http://www.reddit.com/r/fullmoviesonyoutube.json?limit=500')

#turning the response into keys
data = r.json()

#For loop to pull the title of the movie and the link to the movie.
for child in data['data']['children']:
	#Grabbing the title of the movie
	title = child['data']['title']
	
	#Grabbing the url of the movie
	url = child['data']['url']

	#Getting rid of https in all links
	url = url.replace('https','http')	

	#print 'Title: ' + title + '  Link: ' + url

	r = requests.get(url)

	#Check each line in youtube page for an unavailble message
	for line in r.text.split('\n'):
		if 'sorry' in line:
			print 'The following link is down: ' + url
			break
		else:
			print 'This movie is up: ' + title + ' URL is: ' + url	
			break

	#Sleeping for 10 seconds
	time.sleep(10)
