This script reads in a list of movies and runtimes from an input file. It then
hits the youtube apis with the title of the movie, looking for movies on youtube
that are very close to the runtime of the movie read in.

*You will have to use your own api key. You can replace it as the first argument in
the call to the constructor at the bottom of the code.
*You will have to install the isodate python module in order to get this to run

#Things to do
- Hit the search api in such a way that it won't return results related to movies youtube is trying to get you to rent
- There is some strangeness when the isodate does conversion of time, and the script errors out. Look into it.
- Clean up the compare runtimes function
