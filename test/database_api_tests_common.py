import unittest, os

import database

#Path to the database file, different from the deployment db
db_path = 'db/db_test.db'
db = database.MusicDatabase(db_path)

class BaseTestCase(unittest.TestCase):
    '''
    Base class for all test classes. It implements the setUp and the tearDown
    methods inherint by the rest of test classes.
    '''
   
    def setUp(self):
        if os.path.exists(db_path):
            os.remove(db_path)

        db.load_init_values()

    def tearDown(self):
        db.clean()
        pass

