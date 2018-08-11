#!/usr/bin/python
# -*- coding: utf8 -*-

import argparse
import os
import logging

import genius

parser = argparse.ArgumentParser(
    description="A Genius scraper to obtain lyric from a specified lists of rapper"
)
parser.add_argument('-v',
                    '--verbose',
                    help='increase output verbosity',
                    action='store_true'
                    )

parser.add_argument('-l',
                    '--lyrics_dir',
                    help='directory in which to save the scraped lyrics',
                    type=str,
                    default='lyrics'
                    )

args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

print(args.lyrics_dir)

# To define
MAX_SONGS = 2

artistsList = [
    "Eminem",
    "NF",
    "the notorious big",
    "Jay-z",
    "Kendrick Lamar",
    "Kanye West",
    "Nas",
    "J Cole",
    "Lupe Fiasco",
    "Pusha-T",
    "Lil Wayne",
    "André 3000",
    "Immortal Technique",
    "Talib Kweli",
    "Ice Cube",
    "Big L",
    "Drake",
    "Rakim",
    "Deniro Farrar",
    "Eazy-E",
    "Logic",
    "Mos Def",
    "Common",
    "Scarface",
    "Royce Da 59",
    "Chance The Rapper",
    "Childish Gambino",
    "Tyler The Creator",
    "Action Bronson",
    "Mac Miller",
    "A$AP Rocky",
    "Joey Bada",
    "CunninLynguists",
    "A$AP Ant",
    "Isaiah Rashad",
    "Earl Sweatshirt",
    "Montana of 300",
    "Bas",
]
artistsList = ['Eminem']
logger.info(f"Number of artists to scrap {len(artistsList)}")
notDownloaded = []
dirname = os.path.dirname(__file__)
lyrics_folder = args.lyrics_dir
artist_processed_counter = 0

for artist in artistsList:
    # Initialization
    api = genius.Genius()
    logger.info(f'Processing artist {artist}')
    try:
        artistScrap = api.search_artist(artist, max_songs=MAX_SONGS)
        if artistScrap.num_songs > 0:
            lyrics = ''
            for song in artistScrap.songs:
                new_lyrics = song._body['lyrics']
                lyrics = f'{lyrics}\n{new_lyrics}'

            logger.info(f'Nb characters for {artist}: {len(lyrics)}')

            if not os.path.exists(lyrics_folder):
                os.makedirs(lyrics_folder)
            with open(os.path.join(dirname, f'{lyrics_folder}/{artist}_lyrics.txt'), 'w') as f:
                f.write(lyrics)
                artist_processed_counter += 1
    except:
        logger.error(f'Could not process artist {artist}')
        notDownloaded.append(artist)

logger.info('Success. All artists have been processed')
logger.info(f'Artists for whom the scrapping failed: {notDownloaded}')
logger.info('Merge the files with')
logger.info('cat *_lyrics.txt > fusion.txt')
logger.info(f'\n Stats : sd'
            f'\n  - Number of artists to process: {len(artistsList)}'
            f'\n  - Success: {artist_processed_counter}'
            f'\n  - Failure: {len(notDownloaded)}'
            f'\n  - Sucess Rate: {artist_processed_counter/len(artistsList)}'
            )

