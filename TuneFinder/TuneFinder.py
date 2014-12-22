class TuneFinder:

    def __init__(self, apiKey, playListFilename):
        """ TuneFinder constructor """

        self.apiKey = apiKey
        self.playListFilename = playListFilename

        print apiKey
        print playListFilename

    def searchPlaylist(self):
        """ searchPlaylist method this method will be used to pull in runtimes of music in playlist that
            will later be used to hit the youtube apis to create the music playlist. """

        f = open('SamplePlaylist.txt','r')

        for val in f.readlines():
            print val


if __name__ == '__main__':
    a = TuneFinder("fefde07cea7c7f8803e15d47ddb89035","SamplePlaylist.txt")

    a.searchPlaylist()
