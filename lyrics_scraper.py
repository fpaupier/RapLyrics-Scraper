#!/usr/bin/python
# -*- coding: utf8 -*-

import argparse
import os
import logging

from genius.api import Genius

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="A Genius scraper to obtain lyric from a specified lists of lyricists"
)
parser.add_argument('-v',
                    '--verbose',
                    help='increase output verbosity',
                    action='store_true',
                    )

parser.add_argument('-l',
                    '--lyrics_dir',
                    help='lyrics save directory',
                    type=str,
                    default='lyrics',
                    )

parser.add_argument('-n',
                    '--songs_per_artists',
                    help='number of maximum songs to scrap per artist',
                    type=int,
                    default=200,
                    )

args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

artists = [
    'NF',
    'Eminem'
]

logger.info(f'Lyrics saved in directory{args.lyrics_dir}.')
logger.info(f'Number of artists to scrap {len(artists)}')

notDownloaded = []
dirname = os.path.dirname(__file__)
lyrics_folder = args.lyrics_dir
artist_processed_counter = 0

for artist in artists:
    # Initialization
    api = Genius()
    logger.info(f'Processing artist {artist}')
    try:
        artistScrap = api.search_artist(artist, max_songs=args.songs_per_artists)
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
logger.info('cat *_lyrics.txt > merged_lyrics.txt')
logger.info(f'\n Stats : sd'
            f'\n  - Number of artists to process: {len(artists)}'
            f'\n  - Success: {artist_processed_counter}'
            f'\n  - Failure: {len(notDownloaded)}'
            f'\n  - Sucess Rate: {artist_processed_counter/len(artists)}'
            )
