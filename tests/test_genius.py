import unittest

from genius.api import _API, Genius
from genius.artist import Artist
from genius.song import Song

api = Genius()


class TestCredentials(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print('\n---------------------\nTesting credentials...\n'
              'Comparing to pops Genius API keys...\n')
        cls.client_id = '8g35AydfE3iLO0pzUloc0hIsX9f7HJUSvI8rzMJPe142jEGaeN4bDRbsgexCNSkO'
        cls.client_secret = 'vp4tmXezkMJyf7J1-Nu1PUyepjZMOEAuZR3JOBxkdbTVJ0T84eWiPrkxp18rIeqtNYOUJfCMXjNc9TbO1V6dOA'
        cls.client_access_token = 'Ofx6Mjnd9uIp0yb_Rh-ukkWqTWu8JJ4hUAQUB363BE18WgvszI-GFHh6pAfkL_EM'

    def test_load_client_access_token(self):
        """
        Check the scraper correctly loads the credentials.
        :return:
        """
        assert _API._load_credentials() == self.client_access_token


class TestArtist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Artist tests...\n")
        cls.artist_name = "The Beatles"
        cls.new_song = "We can work it out"
        cls.max_songs = 3
        cls.artist = api.search_artist(cls.artist_name, max_songs=cls.max_songs)

    def test_artist(self):
        msg = "The returned object is not an instance of the Artist class."
        self.assertIsInstance(self.artist, Artist, msg)

    def test_name(self):
        msg = "The artist object name does not match the requested artist name."
        self.assertEqual(self.artist.name, self.artist_name, msg)

    def test_add_song_from_same_artist(self):
        msg = "The new song was not added to the artist object."
        self.artist.add_song(api.search_song(self.new_song, self.artist_name))
        self.assertEqual(self.artist.num_songs, self.max_songs + 1, msg)

    def test_add_song_from_different_artist(self):
        msg = "A song from a different artist was incorrectly allowed to be added."
        self.artist.add_song(api.search_song("These Days", "Jackson Browne"))
        self.assertEqual(self.artist.num_songs, self.max_songs, msg)


class TestSong(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n---------------------\nSetting up Song tests...\n")
        cls.artist_name = 'Andy Shauf'
        cls.song_title = 'Begin Again'
        cls.album = 'The Party'
        cls.year = '2016-05-20'
        cls.song = api.search_song(cls.song_title, cls.artist_name)

    def test_song(self):
        msg = "The returned object is not an instance of the Song class."
        self.assertIsInstance(self.song, Song, msg)

    def test_title(self):
        msg = "The returned song title does not match the title of the requested song."
        self.assertEqual(self.song.title, self.song_title, msg)

    def test_artist(self):
        msg = "The returned artist name does not match the artist of the requested song."
        self.assertEqual(self.song.artist, self.artist_name)

    def test_album(self):
        msg = "The returned album name does not match the album of the requested song."
        self.assertEqual(self.song.album, self.album, msg)

    def test_year(self):
        msg = "The returned year does not match the year of the requested song"
        self.assertEqual(self.song.year, self.year, msg)

    def test_lyrics(self):
        lyrics = 'Begin again\nThis time you should take a bow at the'
        self.assertTrue(self.song.lyrics.startswith(lyrics))

    def test_media(self):
        msg = "The returned song does not have a media attribute."
        self.assertTrue(hasattr(self.song, 'media'), msg)
