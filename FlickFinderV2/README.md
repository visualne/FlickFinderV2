###DISCLAIMER 
I did not upload any of the pirated content that this script may or may not find. This script is only to be used for educational purposes only.

###Overvew

This script reads in a list of movies and runtimes from an input file. It then
hits the youtube apis with the title of the movie, looking for movies on youtube
that are very close to the runtime of the movie read in.

Usage example: python FlickFinder.py --apikey alkjsdfjadsj;fkla --movielist 2001Movies.txt

*You will have to install the isodate python module in order to get this to run

#Things to do
- Check for 200 status for both api calls
- Add more regular expressions to status function in statusCheck class that looks for movies that are phoney.
- When google updates the youtube api with a way to check to see if a movie is a rental the code will need to be changed.
- Clean up the compare runtimes function
