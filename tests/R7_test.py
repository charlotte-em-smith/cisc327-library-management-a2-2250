#import library_service
from CISC_327_CS.services import library_service
#import database
from CISC_327_CS import database
import sqlite3
import unittest

class testR7(unittest.TestCase):
    def test_patron_database_vals(self):
        # get database connection and cursor
        db = database.get_db_connection()
        cur = db.cursor()
        
        # select * from db and get column names from *
        cur.execute("SELECT * FROM borrow_records")
        col_names = [description[0] for description in cur.description]

        # test for existence of all required column headers in the database
        self.assertEqual(col_names, ['id', 'patron_id', 'book_id', 'borrow_date', 'due_date', 'return_date'])
        
if __name__ == "__main__":
    unittest.main()