import requests
import json
import datetime
import time
import isodate

class FlickFinderV2:

    def __init__(self, apiKey, movieList):
        """This constructor creates the FlickFinderV2 object 

        Args:
            apiKey (str) The first parameter. This will be your public google api key.
            movieList (str) The second parameter. This will be the filename of a movie list that you have created.
        """
        self.apiKey = apiKey
        self.movieList = movieList

    def searchMovies(self):
        """This function searches youtube for movies read in from the input file movieList filename"""

        #A opening up our list of movies and runtimes for each movie.
        f = open(self.movieList,'r')

        #Printing starting search message
        print 'Starting search...\n'

        for val in f.readlines():
            #Splitting the line read in from in the input file into a list.
            TitleRuntimeYear = val.split('*')

            #Storing the title of the movie read in from the input file in its own variable called movieTitle
            movieTitle = TitleRuntimeYear[0]

            #Storing the runtime of the movies read in from the input file in its own variable called movieRuntime
            movieRuntime = TitleRuntimeYear[1]

            #Grabbing links off of page
            r = requests.get(r'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q='+movieTitle+'&type=video&videoDuration=long&key=' + self.apiKey)

            #turning the response json key value pairs
            data = r.json()

            #Creating empty dictionary that holds the title of the video along with the id of
            #the video
            IDAndTitleAndLength={}

            #The loop below determines the title and id of the video from the above api first api that was queried with requests
            for val in data['items']:
                #Creating empty dictionary that will eventually hold videoTitle,videoDuration of videos found on youtube
                titleAndDuration = []

                title = val['snippet']['title']
                videoId = val['id']['videoId']

                #Adding the title only to the titleAndDuration list. The runtime will be added after the next api query.
                titleAndDuration.append(title)

                #Filling dictionary with id:title pairs ex) 'sf@a234asdf':['Title of some video that may or may not be the video we are looking for']
                IDAndTitleAndLength[videoId] = titleAndDuration

            #Calling function to retrieve the runtimes of each of the videos found in the IDTitleAndLength dictionary
            self.findRuntimes(IDAndTitleAndLength,movieTitle,movieRuntime)

    def findRuntimes(self,IDAndTitleAndLength,movieTitle,movieRuntime):
        """This function searches youtube for the runtimes of each of the movies found in the IDAndTitleAndLength dictionary
        
        Args:
            IDAndTitleAndLength (dict) Dictionary containing the following videoID:Name of video found on youtube.(Will contain runtime at end of function)
            movieTitle (str) Title of movie read in from input file.
            moveieRuntime (str) Runtime of movie read in from input file
        """

        #Second API for determining the length of each of the videos found from the above api query
        videoLengthsLink = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id='

        #Adding list of IDs to api url
        for key in IDAndTitleAndLength.keys():
            videoLengthsLink =  videoLengthsLink + key + '%2C'

        #Creating rest of the videoLengthsLink
        videoLengthsLink = videoLengthsLink + '&fields=items&key=' + self.apiKey


        #Doing second search. This search will tell me the length of each of the videos in my IDAndTitleLength dictionary.
        #I called the variable IDAndTitleLength because after the below for loop is finished the dictionary will look like this
        #ex) sf@a234asdf:'Happy Gilmore*PT59M56S' I now have a dictionary that contains the video id of the movie found, the title of the movie
        #and the runtime of the movie
        r = requests.get(videoLengthsLink)

        #turning the response into json key value pairs
        data = r.json()

        #the for loop below adds the runtime of the video to the IDAndTitleAndLength dictionary
        for val in data['items']:
            IDAndTitleAndLength[val['id']].append(val['contentDetails']['duration'])

        #Calling compareRuntimes function
        self.compareRuntimes(IDAndTitleAndLength, movieTitle, movieRuntime)

        #sleeping for 5 seconds
        time.sleep(5)

    def compareRuntimes(self, IDAndTitleAndLength, movieTitle, movieRuntime):
        """This function checks to to see if runtimes found match what was read in from the input file

        Args:
            IDAndTitleAndLength (dict) Dictionary containing the following videoID:Name of video found on youtube, runtime of video found on youtube.
            movieTitle (str) Title of movie read in from input file.
            moveieRuntime (str) Runtime of movie read in from input file
        """
		
        #The for loop below looks through the IDAndTitleAndLength dictionary looking for runtimes
        for k,v in IDAndTitleAndLength.items():
            #Grabbing the runtime only
            runtime = v[1]
            title = v[0]
            videoID = k

            #converting movieRuntime sent in into this format HH:MM:00. Aparently seconds are not considered
            #part of a legitimate runtime.
            duration=isodate.parse_duration(runtime)
            convertedRuntime = time.strftime('%H:%M:00', time.gmtime(duration.seconds))

            #Checking for actual match and printing possible match output. I had to strip off the leading 0 from the converted
            #runtime in order for it to be in a format that will work for the runtime read in from the input file. Hopefully movies
            #won't be greater then 09:59:59 :)
            if movieRuntime == convertedRuntime[1:]:
                print "Possible match found: Title: " + movieTitle + " Link: " + 'https://www.youtube.com/watch?v=' + videoID



#Example use listed below
if __name__ == '__main__':
    #Initializes the object with the api key as the first aguement and the movie list file name as the second arguement
    a = FlickFinderV2("AIzaSyAPLEpZgnfkvyxX2QuFT60LFDKg84WWSJQ","2000_MovieList")

    #Starts the search
    a.searchMovies()
