# coding: utf8

import os
import sys
import ssl
import re
import logging
from string import punctuation

from urllib.request import Request, urlopen, quote
from bs4 import BeautifulSoup
import requests
import socket
import json

from genius.song import Song
from genius.artist import Artist

logger = logging.getLogger(__name__)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class _API(object):
    """Interface with the Genius.com API"""
    
    # Genius API constants
    _API_URL = "https://api.genius.com/"    
    _API_REQUEST_TYPES =\
        {'song': 'songs/', 'artist': 'artists/', 'artist-songs': 'artists/songs/', 'search': 'search?q='}
    
    def __init__(self, client_access_token=''):        
        if client_access_token == '':
            creds = self._load_credentials()
            if not isinstance(creds, type(None)):
                self._CLIENT_ACCESS_TOKEN = creds
            else:
                logger.error('Could not load client access token. \n Check that you have a valid credentials.ini')
        else:
            self._CLIENT_ACCESS_TOKEN = client_access_token
        self._HEADER_AUTHORIZATION = f'Bearer  {self._CLIENT_ACCESS_TOKEN}'

    @staticmethod
    def _load_credentials():
        """Load the Genius.com API authorization information from the 'credentials.ini' file"""
        creds_file = os.path.join(DIR_PATH, 'credentials.ini')
        with open(creds_file, 'r') as creds:
            lines = [str(line.rstrip('\n')) for line in creds]
            for line in lines:
                if "client_access_token" in line:
                    client_access_token = line.split(": ")[1]
                    return client_access_token
        logger.error('No credentials loaded.')
        return None
    
    def _make_api_request(self, request_term_and_type, page=1):
        """Send a request (song, artist, or search) to the Genius API, returning a json object
        
        INPUT:
            request_term_and_type: (tuple) (request_term, request_type)
        
        *request term* is a string. If *request_type* is 'search', then *request_term* is just
        what you'd type into the search box on Genius.com. If you have an song ID or an artist ID,
        you'd do this: self._make_api_request('2236','song')
        
        Returns a json object.
        """        
        
        # The API request URL must be formatted according to the desired request type
        api_request = self._format_api_request(request_term_and_type, page=page)
        
        # Add the necessary headers to the request
        request = Request(api_request)        
        request.add_header('Authorization', self._HEADER_AUTHORIZATION)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
        while True:  # FIXME: Really ? A while True ?!
            try:
                gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars : Is this line really necessary ? try without.
                response = urlopen(request, context=gcontext, timeout=4)  # timeout set to 4 seconds; automatically retries if times out
                raw = response.read().decode('utf-8')
            except socket.timeout:
                logger.warning('Timeout raised and caught')
                continue
            break
                                
        return json.loads(raw)['response']
        
    def _format_api_request(self, term_and_type, page=1):
        """Format the request URL depending on the type of request"""            
        request_term, request_type = str(term_and_type[0]), term_and_type[1]                
        assert (request_type in self._API_REQUEST_TYPES), 'Unknown API request type'

        if request_type == 'artist-songs':
            return f'{self._API_URL}artists/{quote(request_term)}/songs?per_page=50&page={page}&sort=popularity'
        return f'{self._API_URL}{self._API_REQUEST_TYPES[request_type]}{quote(request_term)}'

    @staticmethod
    def _scrape_song_lyrics_from_url(URL):
        """Use BeautifulSoup to scrape song info off of a Genius song URL"""                                
        page = requests.get(URL)    
        html = BeautifulSoup(page.text, 'html.parser')
        
        # Scrape the song lyrics from the HTML
        lyrics = html.find('div', class_='lyrics').get_text().encode('utf-8', 'ignore').decode('utf-8')
        lyrics = re.sub('\[.*\]', '', lyrics)  # Remove [Verse] and [Bridge] stuff
        lyrics = re.sub('\n{2}', '\n', lyrics)  # Remove gaps between verses
        lyrics = str(lyrics).strip('\n')
        
        return lyrics

    @staticmethod
    def _clean_string(s):
        """
        Weak string cleaner.

        :param s (str): string to clean
        :return (str): cleansed string
        """
        s = str(s.encode('utf-8', errors='ignore').decode('utf-8')).lower().replace('-', ' ').replace("”", '').replace('’', '')
        if sys.version_info[0] == 2:
            return s.translate(None, punctuation)
        translator = str.maketrans('', '', punctuation)
        return s.translate(translator)


class Genius(_API):
    """User-level interface with the Genius.com API.
     User can search for songs (getting lyrics) and artists (getting songs)
     """
    
    def search_song(self, song_title, artist_name=''):
        """Search Genius.com for *song_title* by *artist_name*"""                
                    
        # Perform a Genius API search for the song
        if artist_name != '':
            logger.info(f'Searching for {song_title} by {artist_name}...')
        else:            
            logger.info(f'Searching for {song_title}...')

        search_term = f'{song_title} {artist_name}'
        json_search = self._make_api_request((search_term, 'search'))
                
        # Loop through search results, stopping as soon as title and artist of result match request
        n_hits = min(10, len(json_search['hits']))
        for i in range(n_hits):
            search_hit = json_search['hits'][i]['result']
            found_title = self._clean_string(search_hit['title'])
            found_artist = self._clean_string(search_hit['primary_artist']['name'])
                                    
            # Download song from Genius.com if title and artist match the request
            if found_title == self._clean_string(song_title) and\
                    found_artist == self._clean_string(artist_name) or\
                    artist_name == '':
                # Found correct song, accessing API ID
                json_song = self._make_api_request((search_hit['id'], 'song'))
                
                # Scrape the song's HTML for lyrics
                lyrics = self._scrape_song_lyrics_from_url(json_song['song']['url'])

                # Create the Song object
                song = Song(json_song, lyrics)
                                
                logger.info('Done.')
                return song
        
        logger.warning('Specified song was not first result :(')
        return None
        
    def search_artist(self, artist_name, verbose=True, max_songs=None):
        """Allow user to search for an artist on the Genius.com database by supplying an artist name.
        Returns an Artist() object containing all songs for that particular artist."""
                                
        logger.info(f'Searching for {artist_name}...\n')
    
        # Perform a Genius API search for the artist                
        json_search = self._make_api_request((artist_name, 'search'))
        for hit in json_search['hits']:
            found_artist = hit['result']['primary_artist']
            if self._clean_string(found_artist['name']) == self._clean_string(artist_name.lower()):
                artist_id = found_artist['id']
                break
            else:                                                            
                artist_id = None                                                                                        
        assert (not isinstance(artist_id, type(None))), 'Could not find artist. Check spelling?'
        
        # Make Genius API request for the determined artist ID
        json_artist = self._make_api_request((artist_id, 'artist'))

        # Create the Artist object
        artist = Artist(json_artist)
        
        if max_songs > 0 or isinstance(max_songs, type(None)):
            # Access the api_path found by searching
            artist_search_results = self._make_api_request((artist_id, 'artist-songs'))        

            # Download each song by artist, store as Song objects in Artist object
            keep_searching = True
            n_songs = 0
            while keep_searching:            
                for json_song in artist_search_results['songs']:
                    # TODO: Shouldn't I use self.search_song() here?
                    # Scrape song lyrics from the song's HTML
                    lyrics = self._scrape_song_lyrics_from_url(json_song['url'])            

                    # Create song object for current song
                    song = Song(json_song, lyrics)
                    if artist.add_song(song) == 0:
                        n_songs += 1
                        if verbose:
                            try:
                                logger.info(f'Song {n_songs}: "{title}"')
                            except Exception:
                                # FIXME Run to see what kind of exception it yields for more specific exception catching
                                pass
                    
                    # Check if user specified a max number of songs for the artist
                    if not isinstance(max_songs, type(None)):
                        if artist.num_songs >= max_songs:
                            keep_searching = False
                            logger.info(f'\nReached user-specified song limit ({max_songs}).')
                            break

                # Move on to next page of search results
                next_page = artist_search_results['next_page']                
                if isinstance(next_page, type(None)):
                    break
                else:  # Get next page of artist song results
                    artist_search_results = self._make_api_request((artist_id, 'artist-songs'), page=next_page)           

            logger.info(f'Found {artist.num_songs} songs.\n')

        logger.info('Done.')
        return artist

    @staticmethod
    def save_artist_lyrics(artist):
        filename = f"Lyrics_{artist.name.replace(' ', '')}.txt"
        with open(filename, 'w') as lyrics_file:
            [lyrics_file.write(s.lyrics.encode('utf8') + 5*'\n') for s in artist.songs]
        logger.info(f'Wrote lyrics for {artist.num_songs} songs.')


if __name__ == '__main__':
    G = Genius()    

    if sys.argv[1] == '--search_song':            
        if len(sys.argv) == 4:                        
            song = G.search_song(sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 3:
            song = G.search_song(sys.argv[2])
        lyrics = song.lyrics.replace('\n', '\n    ')
        logger.info(f'"{song.title}" by {song.artist}:\n    {lyrics}')
    elif sys.argv[1] == '--search_artist':
        artist = G.search_artist(sys.argv[2], max_songs=5)
        print(artist)

