# coding: utf8
import logging

logger = logging.getLogger(__name__)


class Artist(object):
    """An artist from the Genius.com database.
    
    Attributes:
        name: (str) Artist name.
        num_songs: (int) Total number of songs listed on Genius.com
    
    """                            

    def __init__(self, json_dict):
        """Populate the Artist object with the data from *json_dict*"""
        self._body = json_dict['artist']
        self._url = self._body['url']
        self._api_path = self._body['api_path']
        self._id = self._body['id']
        self._songs = []
        self._num_songs = len(self._songs)
        
    @property
    def name(self):            
        return str(self._body['name'].encode("utf-8", errors='ignore').decode("utf-8"))
                    
    @property
    def image_url(self):
        return self._body['image_url']
    
    @property
    def songs(self):
        return self._songs
    
    @property
    def num_songs(self):
        return self._num_songs          
        
    def add_song(self, newsong):
        """Add a Song object to the Artist object"""
        
        if any([song.title == newsong.title for song in self._songs]):
            logger.info(f'{newsong.title} already in {self.name}, not adding song.')
            return 1  # Failure
        if newsong.artist == self.name:
            self._songs.append(newsong)
            self._num_songs += 1
            return 0  # Success
        else:
            logger.info(f"Can't add song by {newsong.artist}, artist must be {self.name}.")
            return 1  # Failure

    def __str__(self):
        """Return a string representation of the Artist object."""                        
        if self._num_songs == 1:
            return f'{self.name}, {self._num_songs} song'
        else:
            return f'{self.name}, {self._num_songs} songs'
    
    def __repr__(self):
        return repr((self.name, f'{self._num_songs} song(s)'))