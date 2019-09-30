# RapLyrics-Scraper

[![CircleCI](https://circleci.com/gh/fpaupier/RapLyrics-Scraper/tree/master.svg?style=svg)](https://circleci.com/gh/fpaupier/RapLyrics-Scraper/tree/master)

## Context

This project aims to provide high quality text dataset of rap music lyrics.
Such dataset are then fed to a neural network to build lyrics-generation model.
The resulting word-to-word lyrics-generative model is served on [raplyrics.eu](https://www.raplyrics.eu/?utm_source=github.com&utm_medium=github-readme&utm_campaign=github-scraper).

Feel free to tweak this scraper to fit your needs. Kudos to open source.

## Setup
- First you will need to  [create a genius API key](https://genius.com/api-clients/new)
 to be able to call their API. Once done, copy your `client_access_token` in  `genius/credentials.ini`.

- Get the repo - clone from GitHub
       
      
    $ git clone https://github.com/fpaupier/RapLyrics-Scraper

- Setup a virtualenv

This project is built on python3 - I recommend using a virtual environment.

```bash
`which python3` -m venv RapLyrics-Scraper
source RapLyrics-Scraper/bin/activate
pip install -r requirements.txt
```


## Run the lyrics scraper

- Update the list of artists you want to get the lyrics from and the number of songs
to get per artists. To do so, directly edit the `artists` list defined at `lyrics_scraper.py:39`.

- To run the script: be sure to set the `lyrics_dir` and `songs_per_artists` arguments.
    - Specify the directory in which the scraped lyrics should be saved with `lyrics_dir` 
    - Specify the number of songs to scrap per artist with the ``songs_per_artists`` arg.
   Run ``python lyrics_scraper.py --help`` for more information on the available arguments 

Let's say you want to scrap 2 songs per artist and save them in the folder ``my_lyrics_folder`` with a verbose output, run:
```bash
python lyrics_scraper.py --verbose --lyrics_dir='my_lyrics_folder' --songs_per_artists=2
```

- Once the scraping is done : one lyric file is generated per artist scraped. Merge the files with:
```bash
cat *_lyrics.txt > merged_lyrics.txt
```

## Utils
A toolbox is also provided to analyze some of the dataset properties.
To run a quick analysis of any ``.txt`` file, update the file to consider in `pre_processing/analysis.py` then run:
```bash
python pre_processing/analysis.py
```

## Notes

Currently we get the songs by decreasing popularity order.

## Related work

This project was intensively used to generate high quality text dataset that were consumed by:

   - [RapLyrics-Back](https://github.com/cyrilou242/RapLyrics-Back), to train and serve a lyrics-generative model.
    
   - [RapLyrics-Front](https://github.com/fpaupier/RapLyrics-Front) consumes the model trained and served by [RapLyrics-Back](https://github.com/cyrilou242/RapLyrics-Back) enabling [raplyrics.eu](https://www.raplyrics.eu/?utm_source=github.com&utm_medium=github-readme&utm_campaign=github-scraper) users to generate unique and inspirational lyrics.
