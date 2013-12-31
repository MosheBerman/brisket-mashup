Brisket
==============

Brisket is a neat little tool for tracking those stupid #IfTheMovieWereJewishTweets and linking them to possible related movies on IMDb.

Configuring Brisket
---
You're going to have to add some Twitter API keys to the APIKeys class. This lets Brisket pull tweets without too much trouble. Also, check that TwitterFetcher.py reference `APIKeys` and not a file called `keys`. For those who prefer lists:

1. Open up APIKeys.py and add your Twitter keys and tokens. (More on this in the next section.)
2. Open TwitterFetcher.py and check look for a line that looks like this:

    `from keys import APIKeys`
    
    and change it to this:
    
    `from APIKeys import APIKeys`
    
    If the second line is already present and the first is not, you can disregard this step. 
    
You're ready to go!

Twitter API Keys:
---
Go to [dev.twitter.com/apps](https://dev.twitter.com/apps) and create a new application. You'll use the two keys at the top of the page *as well as the ones that you'll generate by scrolling to the bottom and pushing the button*.

The four keys you're looking for are:

1. Consumer key
2. Consumer Secret
3. Access token
4. Access token secret

You'll find all of these in the details tab of your new application. 


Running Brisket
---
To run brisket, simply run `python Main.py` in your terminal. Brisket will log out some steps as it runs. Bear in mind that we're making many web requests, so this may take some time, depending on your internet connection. 

On unixes, run as sudo so that Brisket can save the results.

Live Demo:
---
You can see a live demo at http://mosheberman.com/brisket/index.html

License
---
You can do anything you want as long you obey these three rules:
 
1. Don't take anything here without crediting Moshe Berman and Charles Carr. 
2. Don't sell this or use it to make money in any way. (If you do, We'll be expecting renumeration.)
3. Don't use this to violate any laws or license agreements with companies. 