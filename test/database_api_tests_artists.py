import sqlite3, unittest

from .database_api_tests_common import BaseTestCase, db, db_path

class ArtistsDbAPITestCase(BaseTestCase):

    artist1 = {'name': 'Clap! Clap!',
               'genre': 'electronic',
                'country': "Italy",
                'language': "Italian",
                'formed_in': 2014
                }
    artist2 = {
            'name': 'The Vaccines',
                           'genre': 'rock',
                'country': "England",
                'language': "English",
                'formed_in': 2008

    }
    initial_size = 2

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_artists_table_created(self):
        '''
        Checks that the table initially contains 20 messages(check
        forum_data_dump.sql).
        '''
        print '('+self.test_artists_table_created.__name__+')', \
               self.test_artists_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM artists'
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
            artists = cur.fetchall()
            #Assert
            self.assertEquals(len(artists), self.initial_size)
        if con:
            con.close()

    def test_create_artist_object(self):
        '''
        Check that the method _create_artist_object works return adequate
        values for the first database row.
        '''
        print '('+self.test_create_artist_object.__name__+')', \
               self.test_create_artist_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM artists WHERE name = "Clap! Clap!"'
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
            artist = db._create_artist_object(row)
            self.assertDictContainsSubset(artist, self.artist1)

    def test_get_artist(self):
        '''
        Test get_artist with id msg-1 and msg-10
        '''
        print '('+self.test_get_artist.__name__+')', \
              self.test_get_artist.__doc__
        #Test with an existing artist
        a = db.get_artist(self.artist1['name'])
        self.assertDictContainsSubset(a, self.artist1)


    def test_get_noexistingartist(self):
        '''
        Test get_artist with msg-200 (no-existing)
        '''
        print '('+self.test_get_noexistingartist.__name__+')',\
              self.test_get_noexistingartist.__doc__
        #Test with an existing artist
        a = db.get_artist("NoExisting")
        self.assertIsNone(a)

    def test_get_artists(self):
        '''
        Test that get_artists work correctly
        '''
        print '('+self.test_get_artists.__name__+')', self.test_get_artists.__doc__
        artists = db.get_artists()
        #Check that the size is correct
        self.assertEquals(len(artists), self.initial_size)
        #Iterate throug artists and check if the artists with artist1_id and
        #artist2_id are correct:
        for artist in artists:
            if artist['name'] == self.artist1['name']:
                self.assertDictContainsSubset(artist, self.artist1)

    def test_get_artists_specific_genre(self):
        '''
        Get all artists from user Mystery. Check that their ids are 13 and 14.
        '''
        #artists sent from Mystery are 13 and 14
        print '('+self.test_get_artists_specific_genre.__name__+')', \
        self.test_get_artists_specific_genre.__doc__
        artists = db.get_artists("rock")
        self.assertEquals(len(artists), 1)
        #artists id are 13 and 14
        for artist in artists:
            self.assertIn(artist['name'], ('The Vaccines'))
            self.assertNotIn(artist['name'], ('Clap! Clap!'))

    def test_create_artist(self):
        '''
        Test that a new artist can be created
        '''
        print '('+self.test_create_artist.__name__+')',\
              self.test_create_artist.__doc__
        artistid = db.create_artist("Editors","indie-rock","England","English",2004)
        self.assertIsNotNone(artistid)
        #Get the expected modified artist
        new_artist = {}
        new_artist['name'] = 'Editors'
        new_artist['genre'] = 'indie-rock'
        new_artist['country'] = 'England'
        new_artist['language'] = 'English'
        new_artist['formed_in'] = 2004


        #Check that the artists has been really modified through a get
        resp2 = db.get_artist("Editors")
        self.assertDictContainsSubset(new_artist, resp2)

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()

