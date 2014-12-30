import requests
import isodate
import time

class TuneFinder:

    def __init__(self, apiKey, playListFilename):
        """ TuneFinder constructor """

        self.apiKey = apiKey
        self.playListFilename = playListFilename

    def searchPlaylist(self):
        """ searchPlaylist method this method will be used to pull in runtimes of music in playlist that
            will later be used to hit the youtube apis to create the music playlist. """

        f = open('SamplePlaylist.txt','r')

        #Printing starting search message
        print 'Starting search...\n'

        for val in f.readlines():
            
            #Getting band name from value read in from input file
            band = val.split('*')[0]

            #Getting title of song
            song = val.split('*')[2]

            #Getting runtime of song
            songRuntime = val.split('*')[3].strip()

            #The songTitle variable below holds the band name and title of song to search. ex)Prodigy Breath
            songTitle = band + ' ' + song

            #Grabbing links off of page
            r = requests.get(r'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q='+songTitle+'&type=video&key=' + self.apiKey)

            #turning the response into json key value pairs
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
            self.findRuntimes(IDAndTitleAndLength,songTitle,songRuntime)

    def findRuntimes(self,IDAndTitleAndLength,songTitle,songRuntime):
        """This function searches youtube for the runtimes of each of the movies found in the IDAndTitleAndLength dictionary
        
        Args:
            IDAndTitleAndLength (dict) Dictionary containing the following videoID:Name of video found on youtube.(Will contain runtime at end of function)
            songTitle (str) Title of song in format 'Band Song_Name' ex) Nirvana Lithium
            runtime (str) Runtime of song read in from input file
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
        #ex) sf@a234asdf:'Nirvana Lithium*PT1M2S' I now have a dictionary that contains the video id of the movie found, the title of the movie
        #and the runtime of the movie
        r = requests.get(videoLengthsLink)

        #turning the response into json key value pairs
        data = r.json()

        #the for loop below adds the runtime of the video to the IDAndTitleAndLength dictionary
        for val in data['items']:
            IDAndTitleAndLength[val['id']].append(val['contentDetails']['duration'])

        #Calling compareRuntimes function
        self.compareRuntimes(IDAndTitleAndLength, songTitle, songRuntime)

        #sleeping for 5 seconds
        time.sleep(5)


    def compareRuntimes(self, IDAndTitleAndLength, songTitle, songRuntime):
        """This function checks to to see if runtimes found match what was read in from the input file

        Args:
            IDAndTitleAndLength (dict) Dictionary containing the following videoID:Name of video found on youtube, runtime of video found on youtube.
            songTitle (str) song title that is combination of band and song title. Variable created in searchPlaylist function
            runtime (str) Runtime of song read in from input file
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
            #convertedRuntime = time.strftime('%H:%M:00', time.gmtime(duration.seconds))
            convertedRuntime = time.strftime('%M:%S', time.gmtime(duration.seconds))

            #Checking for actual match and printing possible match output.
            if songRuntime == convertedRuntime:
                print "Possible match found: Title: " + songTitle + " Link: " + 'https://www.youtube.com/watch?v=' + videoID

if __name__ == '__main__':
    a = TuneFinder("AIzaSyAPLEpZgnfkvyxX2QuFT60LFDKg84WWSJQ","SamplePlaylist.txt")

    a.searchPlaylist()
