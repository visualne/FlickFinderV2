import requests
import re

class statusCheck:

    def __init__(self, videoID):
        """This constructor creates the statusCheck object 

        Args:
            videoID (str) The only parameter. This id corresponds to that of
            a video on youtube.
        """
        self.videoID = videoID

    def status(self):
        """This function returns the status of the video on youtube. It will check to see if the movie
        is a rental, or just some phoney link by looking for text in the html of the page"""

        #Full link to youtube video
        videoLink = 'http://www.youtube.com/watch?v=' + self.videoID

        #Grabbing the response and putting in variable r
        r = requests.get(videoLink)

        #Grabbing the html from the response and putting it in response
        #variable.
        response = r.text

        #Checking for various strings in the html that would lead one to believe 
        #the movie is a rental or just some phoney link if there is a match we will return true, 
        #that will mean it is a rental.
        match = re.search('watch-checkout-offers|TO WATCH FULL MOVIE|http://bit|online free full movie',response)

        #returning true if the above text was found in the page. This would
        #mean that the movie is a rental or a phone link of some kind.
        if match:
            return True
        else:
            return False

