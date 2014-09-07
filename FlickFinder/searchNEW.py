import urllib2
import re
import sys
from BeautifulSoup import BeautifulSoup
import time
import datetime


def search(movie,runtime):
	searchMovieLink = 'http://www.youtube.com/search_query=' + movie.replace(' ', '+')

	#https://www.youtube.com/results?search_query=

	response = urllib2.urlopen('https://www.youtube.com/results?search_query=' + movie.replace(' ', '+'))

	pageResults = response.read()

	checkForMovieInResults(pageResults,movie,runtime)
	


def checkForMovieInResults(pageResults,movie,runtime):
	soup = BeautifulSoup(pageResults)

	elements = soup.findAll('li', {'class':re.compile('yt-lockup clearfix yt-uix-tile result-item-padding yt-lockup-video yt-lockup-tile vve-check context-data-item')})

	#Empty list that will hold the runtimes of results found that are over an hour long
	queryRuntimes = []

	#Creating empty dictionary that will hold the link to the video along with the runtime of 
	#each video found in the query.
	results = {}

	#Printing movie
	#print movie

	for val in elements:

		if str(val.string == '>'):
			#print 'The ID is: ' + val['data-context-item-id']
			#print 'The runtime is: ' + val['data-context-item-time']

			try:
				dummyVal = val['data-context-item-time']
			except KeyError:
				#print 'Caught the KeyError at: ' + movie
				continue

			#Code here that will print just movies that are over an hour long.
			if isItOverAnHourLong(val['data-context-item-time']):
				#print 'https://www.youtube.com/watch?v=' + val['data-context-item-id'] + ' is over an hour long.'

				#This is sloppy, but what im doing here is grabbing the hour
				#and minute values from the times that are over an hour long
				#and creating a string that is in this format hh:mm and putting it in
				#a list
				hrMinFormatList = val['data-context-item-time'].split(':')
				#print hrMinFormatList
				hrMinFormat = hrMinFormatList[0] + ':' + hrMinFormatList[1]

				#Creating dictionary that will hold the time of each video from the query, along
				#with the link to each of them.
				movieLink = val['data-context-item-id']
				results[movieLink] = hrMinFormat


				#the bottom list is most likely not needed anymore
				queryRuntimes.append(hrMinFormat)
				#print queryRuntimes



	#Converting the time to hh:mm:ss
	nTime = str(datetime.timedelta(minutes=int(runtime)))
	movieRunTimes = newTimes(nTime)

	for k,v in results.items():
		for val in movieRunTimes:
			if val == v:
				print 'Possible match for: ' + movie + ' at ' + 'https://www.youtube.com/watch?v=' + k
	


	#Sleeping for 10 seconds
	time.sleep(10)


######################################################################
#The function below takes in a runtime of a movie, and returns a list 
#of runtimes that are plus and minus 5 minutes of the runtime.
######################################################################

def newTimes(time):

        finalTime = []

        ntime = time.split(':')

        for n in range(5):
                plusValue = int(ntime[1]) + n
                minusValue = int(ntime[1]) - n

                finalTime.append(time[0] + ':' + str(plusValue))
                finalTime.append(time[0] + ':' + str(minusValue))

	return list(set(finalTime))

#######################################################################
#
#
#######################################################################

def isItOverAnHourLong(vidLength):

        ntime = vidLength.split(':')

        if len(ntime) == 2:
                return False
        elif len(ntime) == 3:
                return True

#####################################################################
#
#
#####################################################################

def somethingFound(queryRuntimes,movieRunTimes):
	for val in queryRuntimes:
		for time in movieRunTimes:
			if val == time:
				return True



#Opening movie list for reading
f=open('h2000sMovies', 'r')

for val in f.readlines():
	splitMovie = val.split('*')
	search(splitMovie[0],splitMovie[1])

