Brisket
==============

Brisket is a neat little tool for tracking those stupid #IfTheMovieWereJewishTweets and linking them to possible related movies on IMDb.

Configuring Brisket
---
You're going to have to add some Twitter API keys to the APIKeys class. This lets Brisket pull tweets without too much trouble. Also, check that TwitterFetcher.py reference `APIKeys` and not a file called `keys`. For those who prefer lists:

1. Open up APIKeys.py and add your Twitter keys and tokens.
2. Open TwitterFetcher.py and check look for a line that looks like this:

    `from keys import APIKeys`
    
    and change it to this:
    
    `from APIKeys import APIKeys`
    
    If the second line is already present and the first is not, you can disregard this step. 
    
You're ready to go!

Running Brisket
---
To run brisket, simply run `python Main.py` in your terminal. Brisket will log out some steps as it runs. Bear in mind that we're making many web requests, so this may take some time, depending on your internet connection.

