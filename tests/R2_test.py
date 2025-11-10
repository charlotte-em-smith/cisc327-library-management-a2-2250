#import library_service
#import database
from ..services import library_service
from .. import database
import sqlite3
import unittest

class testR2(unittest.TestCase):
    def test_book_database_vals(self):
        # get database connection and cursor
        db = database.get_db_connection()
        cur = db.cursor()
        
        # select * from db and get column names from *
        cur.execute("SELECT * FROM books")
        col_names = [description[0] for description in cur.description]

        # test for existence of all required column headers in the database
        self.assertEqual(col_names, ['id', 'title', 'author', 'isbn', 'total_copies', 'available_copies'])

if __name__ == "__main__":
    unittest.main()