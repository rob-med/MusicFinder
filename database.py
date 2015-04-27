from datetime import datetime
import time, sqlite3, sys, re, os
#Default paths for .db and .sql files to create and populate the database.
DEFAULT_DB_PATH = 'db/musicdb.db'
DEFAULT_SCHEMA = "db/schema_dump.sql"
DEFAULT_DATA_DUMP = "db/forum_data_dump.sql"

'''

songs getFavorites(user)
user_profile getUserProfile(nickname)
'''

class MusicDatabase(object):

    def __init__(self, db_path=None):
        '''
        db_path is the address of the path with respect to the calling script.
        If db_path is None, DEFAULT_DB_PATH is used instead.
        '''
        super(MusicDatabase, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = DEFAULT_DB_PATH


    #Setting up the database. Used for the tests.
    #SETUP, POPULATE and DELETE the database
    def clean(self):
        '''
        Purge the database removing old values.
        '''
        os.remove(self.db_path)

    def load_init_values(self, schema=None, dump=None):
        '''
        Create the database and populate it with initial values. The schema
        argument defines the location of the schema sql file while the dump
        argument defines the location of the data dump sql file. If no value
        is provided default values are defined by the global variables
        DEFAULT_SCHEMA and DEFAULT_DATA_DUMP
        '''
        self.create_tables_from_schema(schema)
        self.load_table_values_from_dump(dump)

    def create_tables_from_schema(self, schema=None):
        '''
        Create programmatically the tables from a schema file.
        schema contains the path to the .sql schema file. If it is None,
        DEFAULT_SCHEMA is used instead.
        '''
        con = sqlite3.connect(self.db_path)
        if schema is None:
            schema = DEFAULT_SCHEMA
        with open (schema) as f:
            sql = f.read()
            cur = con.cursor()
            cur.executescript(sql)

    def load_table_values_from_dump(self, dump=None):
        '''
        Populate programmatically the tables from a dump file.
        dump is the  path to the .sql dump file. If it is None,
        DEFAULT_DATA_DUMP is used instead.
        '''
        con = sqlite3.connect(self.db_path)
        if dump is None:
            dump = DEFAULT_DATA_DUMP
        with open (dump) as f:
            sql = f.read()
            cur = con.cursor()
            cur.executescript(sql)

    #HELPERS
    def check_foreign_keys_status(self):
        '''
        Check if the foreign keys has been activated. Return and print in the
        screen if foreign keys are activated.
        '''
        con = None
        try:
            #Connects to the database.
            con = sqlite3.connect(self.db_path)
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            #Execute the pragma command
            cur.execute('PRAGMA foreign_keys')
            #We know we retrieve just one record: use fetchone()
            data = cur.fetchone()
            data_text = 'ON' if data == (1,) else 'OFF'
            print "Foreign Keys status: %s" % data_text

        except sqlite3.Error, excp:
            print "Error %s:" % excp.args[0]
            sys.exit(1)

        finally:
            if con:
                con.close()
        return data

    def set_and_check_foreign_keys_status(self):
        '''
        Activate the support for foreign keys and later check that the support
        exists. Print the results of this test.
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        con = None
        try:
            #connects to the database.
            con = sqlite3.connect(self.db_path)
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            #execute the pragma command, ON
            cur.execute(keys_on)
            #execute the pragma check command
            cur.execute('PRAGMA foreign_keys')
            #we know we retrieve just one record: use ftchone()
            data = cur.fetchone()
            data_text = 'ON' if data == (1,) else 'OFF'
            print "Foreign Keys status: %s" % data_text

        except sqlite3.Error, excp:
            print "Error %s:" % excp.args[0]
            sys.exit(1)

        finally:
            if con:
                con.close()
        return data


    #Here the helpers that transform database rows into dictionary.
    def _create_song_object(self, row):

        song_artist = row['artist']
        song_title = row['title']
        song_year = row['year']
        song_length = row['length']
        song_id = row['sid']
        song = {'songid':song_id, 'title': song_title,
                   'artist':song_artist, 'year':song_year,
                   'length':song_length}
        return song

    def _create_artist_object(self, row):

        artist_name = row['name']
        artist_genre = row['genre']
        artist_country= row['country']
        artist_language= row['language']
        artist_formed_in = row['formed_in']
        artist = {'name':artist_name, 'genre': artist_genre,
                   'country': artist_country, 'language': artist_language,
                   'formed_in': artist_formed_in}
        return artist

    def _create_playlist_object(self, row):

        pl_name = row['name']
        pl_user = row['user']
        pl_created = row['created_on']

        pl = {'name':pl_name, 'user': pl_user,
                   'created_on': pl_created}
        return pl
    def _create_user_object(self, row):

        name = row['nickname']
        gender = row['gender']
        age = row['age']
        country = row['country']
        user = {'nickname':name, 'gender': gender,
                   'age': age, 'country':country}
        return user

    def get_song(self, artist, title):

        #Create the SQL Query
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM songs WHERE artist = ? and title = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (artist, title,)
            cur.execute(query, pvalue)
            #Process the response.
            #Just one row is expected
            row = cur.fetchone()
            if row is None:
                return None
            #Build the return object
            return self._create_song_object(row)

    def get_user(self, nickname):

        #Create the SQL Query
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users WHERE nickname = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (nickname,)
            cur.execute(query, pvalue)
            #Process the response.
            #Just one row is expected
            row = cur.fetchone()
            if row is None:
                return None
            #Build the return object
            return self._create_user_object(row)


    def get_songs(self, artist):

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM songs where artist = ?'
        #Connects to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (artist,)
            cur.execute(query, pvalue)
            #Get results
            rows = cur.fetchall()
            if rows is None:
                return None
            #Build the return object
            songs = []
            for row in rows:
                song = self._create_song_object(row)
                songs.append(song)
            return songs

    def get_playlist(self, name, user):
        #Create the SQL Query
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM playlists where user = ? and name = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (user, name)
            cur.execute(query, pvalue)
            #Process the response.
            #Just one row is expected
            row = cur.fetchone()
            if row is None:
                return None
            #Build the return object
            return self._create_playlist_object(row)

    def get_playlists(self, user):
        #Create the SQL Query
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT name, user, created_on FROM playlists where user = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (user,)
            cur.execute(query, pvalue)
            #Process the response.
            #Just one row is expected
            rows = cur.fetchall()
            if rows is None:
                return None
            #Build the return object
            pls = []
            for row in rows:
                pl = self._create_playlist_object(row)
                pls.append(pl)
            return pls

    def get_songs_in_playlist(self, pl_name, pl_user):
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT sid, title, year, length, artist FROM song_in_playlist, songs where pl_name = ? and pl_user = ? and song = sid'
        #Connects to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (pl_name, pl_user,)
            cur.execute(query, pvalue)
            #Get results
            rows = cur.fetchall()
            if rows is None:
                return None
            #Build the return object
            songs = []
            for row in rows:
                song = self._create_song_object(row)
                songs.append(song)
            return songs


    def create_artist(self, name, genre, country, language, formed_in):
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'INSERT INTO artists (name,genre,country,language,formed_in) VALUES(?,?,?,?,?)'
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #If exists the replyto argument, check that the message exists in
            #the database table

            #Execute SQL Statement to get userid given nickname
            pvalue = (name,genre,country,language,formed_in,)
            cur.execute(stmnt, pvalue)
            #Extract user id
            #Return the id in
            return cur.lastrowid

    def create_song(self, title, year, length, artist):
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'INSERT INTO songs (title,year,length,artist) VALUES(?,?,?,?)'
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #If exists the replyto argument, check that the message exists in
            #the database table

            #Execute SQL Statement to get userid given nickname
            pvalue = (title,year,length,artist,)
            cur.execute(stmnt, pvalue)
            #Extract user id
            #Return the id in
            return cur.lastrowid
    def create_user(self, nickname, password):
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'INSERT INTO users (nickname,password) VALUES(?,?)'
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #If exists the replyto argument, check that the message exists in
            #the database table

            #Execute SQL Statement to get userid given nickname
            pvalue = (nickname,password,)
            cur.execute(stmnt, pvalue)
            #Extract user id
            #Return the id in
            return cur.lastrowid


    def create_playlist(self, name, user):
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'INSERT INTO playlists (name, user, created_on) VALUES(?,?,?)'
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #If exists the replyto argument, check that the message exists in
            #the database table
            timestamp = time.mktime(datetime.now().timetuple())

            #Execute SQL Statement to get userid given nickname
            pvalue = (name, user, timestamp,)
            cur.execute(stmnt, pvalue)
            #Extract user id
            #Return the id in
            return cur.lastrowid

    def append_song_to_playlist(self, song, plname, pluser):
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'INSERT INTO song_in_playlist (song, pl_name, pl_user, added_on) VALUES(?,?,?,?)'
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #If exists the replyto argument, check that the message exists in
            #the database table
            timestamp = time.mktime(datetime.now().timetuple())

            #Execute SQL Statement to get userid given nickname
            pvalue = (song, plname, pluser, timestamp,)
            cur.execute(stmnt, pvalue)
            #Extract user id
            #Return the id in
            return cur.lastrowid


    def get_artist(self, name):
        #Create the SQL Query
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM artists WHERE name = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (name,)
            cur.execute(query, pvalue)
            #Process the response.
            #Just one row is expected
            row = cur.fetchone()
            if row is None:
                return None
            #Build the return object
            return self._create_artist_object(row)

    def get_users(self):
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users'
          #Nickname restriction

        con = sqlite3.connect(DEFAULT_DB_PATH)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            #Get results
            rows = cur.fetchall()
            if rows is None:
                return None
            #Build the return object
            users = []
            for row in rows:
                u = self._create_user_object(row)
                users.append(u)
            return users

    def get_artists(self, genre = None, country = None, language = None):
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM artists'
          #Nickname restriction
        if genre is not None or country is not None or language is not None:
            query+=" where "
            add = 0
        if genre is not None:
            query += "genre = '%s'" % genre
            add = 1
        if country is not None:
            if add:
                query += " and "
            query += "country = '%s'" % country
        if language is not None:
            if add:
                query += " and "
            query += "language = '%s'" % language

        con = sqlite3.connect(DEFAULT_DB_PATH)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            #Get results
            rows = cur.fetchall()
            if rows is None:
                return None
            #Build the return object
            artists = []
            for row in rows:
                artist = self._create_artist_object(row)
                artists.append(artist)
            return artists

    def delete_playlist(self, user, title):
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'DELETE FROM playlists WHERE user = ? and name = ?'
        #connects  to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (user,title,)
            cur.execute(stmnt, pvalue)
            #Check that the message has been deleted
            if cur.rowcount < 1:
                return False
            #Return true if message is deleted.
            return True

    def delete_user(self, nickname):
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'DELETE FROM users WHERE nickname = ?'
        #connects  to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (nickname,)
            cur.execute(stmnt, pvalue)
            #Check that the message has been deleted
            if cur.rowcount < 1:
                return False
            #Return true if message is deleted.
            return True



    def contains_playlist(self,user,title):
        return self.get_playlist(title, user) is not None

    def modify_playlist(self, user, title, new_user, new_title, created_on):
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'UPDATE playlists SET name = ? , user = ?, created_on = ?\
                 WHERE user = ? and name = ?'
        #Connects  to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (new_title, new_user, created_on, user, title,)
            cur.execute(stmnt, pvalue)
            if cur.rowcount < 1:
                return None
            return new_title

    def modify_user(self, old_nickname, age, country, gender):
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'UPDATE users SET age = ?, country = ?, gender = ? \
                 WHERE nickname = ?'
        #Connects  to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            pvalue = (age, country, gender, old_nickname,)
            cur.execute(stmnt, pvalue)
            if cur.rowcount < 1:
                return None
            return old_nickname

    def delete_song(self, artist, title):

        keys_on = 'PRAGMA foreign_keys = ON'

        query = 'DELETE FROM songs WHERE artist = ? and title = ?'

        con = sqlite3.connect(self.db_path)
        with con:

            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(keys_on)

            pvalue = (artist,title)
            cur.execute(query, pvalue)

            if cur.rowcount < 1:
                return False
            return True

    def contains_song(self, artist, title):
        return self.get_song(artist, title) is not None




