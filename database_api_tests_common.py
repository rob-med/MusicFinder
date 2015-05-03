import unittest, os

import database

#Path to the database file, different from the deployment db
db_path = 'db/testdb2.db'
db = database.MusicDatabase(db_path)

class BaseTestCase(unittest.TestCase):
    '''
    Base class for all test classes. It implements the setUp and the tearDown
    methods inherint by the rest of test classes.
    '''
   
    def setUp(self):
        '''
        Clean the database (in SQLite you can remove the whole database file) 
        and create a new one for loading the inital values. 
        '''
        #Be sure that there is no database.
        #This specially is useful if the clean process was not success.
        if os.path.exists(db_path):
            os.remove(db_path)
        #This method load the initial values from forum_data_dump.sql
        #It creates the database if it does not exist. 

    def tearDown(self):
        db.clean()
        pass

