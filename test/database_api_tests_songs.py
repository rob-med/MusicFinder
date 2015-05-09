import sqlite3, unittest

from .database_api_tests_common import BaseTestCase, db, db_path

class SongsDbAPITestCase(BaseTestCase):

    song1 = {'title': 'I know',
               'artist': 'Placebo',
                'year': 1996,
                'length': "3:41",
                'sid': 1
                }
    song2 = {'title': 'Zombie',
               'artist': 'Cranberries',
                'year': 1994,
                'length': "5:21",
                'sid': 6
                }
    initial_size = 20

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_songs_table_created(self):
        '''
        Checks that the table initially contains 20 songs(check
        forum_data_dump.sql).
        '''
        print '('+self.test_songs_table_created.__name__+')', \
               self.test_songs_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM songs'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query)
            songs = cur.fetchall()
            #Assert
            self.assertEquals(len(songs), self.initial_size)
        if con:
            con.close()

    def test_create_song_object(self):
        '''
        Check that the method _create_song_object works return adequate
        values for the first database row.
        '''
        print '('+self.test_create_song_object.__name__+')', \
               self.test_create_song_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM songs WHERE title = "Zombie"'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            song = db._create_song_object(row)
            self.assertDictContainsSubset(song, self.song2)

    def test_get_song(self):
        '''
        Test get_song with artist = Cranberries and title = Zombie
        '''
        print '('+self.test_get_song.__name__+')', \
              self.test_get_song.__doc__
        #Test with an existing song
        a = db.get_song('Cranberries','Zombie')
        self.assertDictContainsSubset(a, self.song2)


    def test_get_noexistingsong(self):
        '''
        Test get_song with artist = Evanescence and title = Going under
        '''
        print '('+self.test_get_noexistingsong.__name__+')',\
              self.test_get_noexistingsong.__doc__
        #Test with an existing artist
        a = db.get_song('Evanescence', 'Going under')
        self.assertIsNone(a)

    def test_get_songs(self):
        '''
        Test that get_songs works correctly
        '''
        print '('+self.test_get_songs.__name__+')', self.test_get_songs.__doc__
        songs = db.get_songs()
        #Check that the size is correct
        self.assertEquals(len(songs), self.initial_size)
        #Iterate throug artists and check if the artists with artist1_id and
        #artist2_id are correct:
        for song in songs:
            if song['title'] == self.song1['title']:
                self.assertDictContainsSubset(song, self.song1)

    # def test_get_songs_specific_genre(self):
    #     '''
    #     Get all artists from user Mystery. Check that their ids are 13 and 14.
    #     '''
    #     #artists sent from Mystery are 13 and 14
    #     print '('+self.test_get_artists_specific_genre.__name__+')', \
    #     self.test_get_artists_specific_genre.__doc__
    #     artists = db.get_artists(genre = 'Rock')
    #     self.assertEquals(len(artists), 3)
    #     #artists id are 13 and 14
    #     for artist in artists:
    #         self.assertIn(artist['name'], ('Cranberries', 'Muse', 'Mana'))
    #         self.assertNotIn(artist['name'], ('Clap! Clap!'))

    def test_create_song(self):
        '''
        Test that a new song can be created
        '''
        print '('+self.test_create_song.__name__+')',\
              self.test_create_song.__doc__
        song = db.create_song("Society",2007,"3:56","Eddie Vedder")
        self.assertIsNotNone(song)
        #Get the expected modified artist
        new_song = {}
        new_song['title'] = 'Society'
        new_song['artist'] = 'Eddie Vedder'
        new_song['year'] = 2007
        new_song['length'] = '3:56'
        #Check that the artists has been really modified through a get
        resp2 = db.get_song('Eddie Vedder', 'Society')
        self.assertDictContainsSubset(new_song, resp2)

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()

