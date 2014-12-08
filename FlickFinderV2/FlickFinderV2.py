import requests
import json
import datetime


#Insert your API key below
apiKey = ''

#A single movie title will be added for now, but later an entire list of movies and runtimes will be used.
movieTitle = 'The Rock'

#Grabbing links off of page
#r = requests.get(r'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q=The+Rock&type=video&videoDuration=long&key=' + apiKey)
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



#Doing second search. This search will tell me the length of each of the videos in my IDAndTitle dictionary
#https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id=Pv1nRwONwK8%2CWbs0OsZWEAc&fields=items%2FcontentDetails&key={YOUR_API_KEY}
r = requests.get(videoLengthsLink)

#turning the response json key value pairs
data = r.json()

#the for loop below adds the runtime of the video to the IDAndTitleAndLength dictionary
for val in data['items']:
		IDAndTitleAndLength[val['id']] = IDAndTitleAndLength[val['id']] + ',' + val['contentDetails']['duration']

#The below data structure can now be checked against the list of movies you read into the script
print IDAndTitleAndLength.items()

##
#Some code here to check the 2000_MovieList file against the IDAndTitleAndLength dictionary and check to see if
#runtime are close to eachother 
##


