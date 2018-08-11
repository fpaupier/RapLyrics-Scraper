# RapLyrics-Scraper

## Context

This project aims to provide high quality text dataset of rap music lyrics.
Such dataset are then fed to a neural network to build lyrics-generation model.

Of course you can tweak it to fit your needs. Kudos to open source.

## Setup
- First you will need to  [create a genius API key](https://genius.com/api-clients/new)
 to be able to call their API. Once done, copy your `client_access_token` in  `genius/credentials.ini`.

- Get the repo - clone from GitHub:

    $ git clone https://github.com/fpaupier/RapLyrics-Scraper

- Setup a virtualenv

This project is built on python3 - Install the required libraries.

    $ mkvirtualenv --python  `which python3 -r requirements.txt RapLyrics-Scraper

Make sure you set up your PyCharm to use the correct Python interpreter.
I strongly recommend the use of one virtualenv per project.

## Notes

Currently we get the songs by decreasing popularity order.

## Warning
Please keep in mind that it is the François' Genius API credentials that are used in the [genius/credentials.ini](genius/credentials.ini) file by default.  
Do not abuse it. plz 🙏