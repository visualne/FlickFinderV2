import requests
import json
import datetime
import time

def compareRuntimes(IDAndTitleAndLength, movieTitle, movieRuntime):
	#Checking to see if runtimes match
	for val in IDAndTitleAndLength.values():
		#Grabbing the runtime only
		runtime = val.split('*')[1][2:]
		#Need a way to store the below time in the format HH:MM:SS
		print runtime



#Insert your API key below
apiKey = ''

#A opening up our list of movies and runtimes for each movie.
f = open('2000_MovieList','r')

for val in f.readlines():
	#Splitting the line read in from in the input file into a list.
	TitleRuntimeYear = val.split('*')

	#Storing the title of the movie read in from the input file in its own variable called movieTitle
	movieTitle = TitleRuntimeYear[0]

	#Storing the runtime of the movies read in from the input file in its own variable called movieRuntime
	movieRuntime = TitleRuntimeYear[1]
	#print movieTitle + ' Runtime: ' + movieRuntime

    #Grabbing links off of page
	r = requests.get(r'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q='+movieTitle+'&type=video&videoDuration=long&key=' + apiKey)

    #turning the response json key value pairs
	data = r.json()

    #Creating empty dictionary that holds the title of the video along with the id of
    #the video
	IDAndTitleAndLength={}

    #Second API for determining the length of each of the videos
	videoLengthsLink = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id='

    #The loop below determines the title and id of the video from the above api first api that was queried with requests
	for val in data['items']:
		title = val['snippet']['title']
		videoId = val['id']['videoId']

		#Filling dictionary with id:title pairs ex) sf@a234asdf:'Happy Gilmore'
		IDAndTitleAndLength[videoId] = title

	#Adding list of IDs to api url
	for key in IDAndTitleAndLength.keys():
		videoLengthsLink =  videoLengthsLink + key + '%2C'

	#Creating rest of the videoLengthsLink
	videoLengthsLink = videoLengthsLink + '&fields=items&key=' + apiKey


	#Doing second search. This search will tell me the length of each of the videos in my IDAndTitleLength dictionary.
	#I called the variable IDAndTitleLength because after the below for loop is finished the dictionary will look like this
	#ex) sf@a234asdf:'Happy Gilmore*PT59M56S' I now have a dictionary that contains the video id of the movie found, the title of the movie
	#and the runtime of the movie
	r = requests.get(videoLengthsLink)

	#turning the response json key value pairs
	data = r.json()

	#the for loop below adds the runtime of the video to the IDAndTitleAndLength dictionary
	for val in data['items']:
		IDAndTitleAndLength[val['id']] = IDAndTitleAndLength[val['id']] + '*' + val['contentDetails']['duration']


	#The below data structure can now be checked against the line read in from the movie list file to see if the runtimes
	#are close to eachother. If they are within 5 minutes of eachother print the potential match for further checking.
	#print IDAndTitleAndLength.items()

	#Send the above dictionary and the title and runtime of the movie read in from the input file into a function to check
	#to see if the runtimes are close to eachother
	compareRuntimes(IDAndTitleAndLength, movieTitle, movieRuntime)

	#sleeping for 5 seconds
	time.sleep(5)



