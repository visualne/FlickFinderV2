import requests
import re

class rentalCheck:

    def __init__(self, videoID):
        """This constructor creates the rentalCheck object 

        Args:
            videoID (str) The only parameter. This id corresponds to that of
            a video on youtube.
        """
        self.videoID = videoID

    def status(self):
        """This function returns the rental status of the video on youtube. """

        #Full link to youtube video
        videoLink = 'http://www.youtube.com/watch?v=' + self.videoID

        #Grabbing the response and putting in variable r
        r = requests.get(videoLink)

        #Grabbing the html from the response and putting it in response
        #variable.
        response = r.text

        #Checking for the string 'rent or purchase' in the html
        #if there is a match we will return true, that will mean
        #it is a rental.
        match = re.search('watch-checkout-offers',response)

        #returning true if the above text was found in the page. This would
        #mean that the movie is a rental.
        if match:
            return True
        else:
            return False
