#import library_service
from services import library_service
import database
#from CISC_327_CS import database
import sqlite3
import unittest


class TestR7():
    def test_patron_database_vals(self):
        # get database connection and cursor
        db = database.get_db_connection()
        cur = db.cursor()
        
        # select * from db and get column names from *
        cur.execute("SELECT * FROM borrow_records")
        col_names = [description[0] for description in cur.description]

        # test for existence of all required column headers in the database
        assert col_names == ['id', 'patron_id', 'book_id', 'borrow_date', 'due_date', 'return_date']

    def test_patron_status_report(self, mocker):
        mocker.patch('services.library_service.get_patron_borrowed_books', return_value=[{'book_id': 1, 'title': 'test', 'author': 'test', 'borrow_date': '2025-07-09', 'due_date': '2025-07-09', 'is_overdue': False}])
        mocker.patch('services.library_service.get_patron_borrow_count', return_value=1)
        mocker.patch('services.library_service.calculate_late_fee_for_book', return_value={'days_overdue': 0, 'fee_amount': 0.00, 'status': 'No late fee'})
        mocker.patch('services.library_service.get_borrow_records', return_value=[{'book_id': 1, 'title': 'test', 'author': 'test', 'borrow_date': '2025-07-09', 'due_date': '2025-07-09','is_overdue': False}])
        

        result = library_service.get_patron_status_report("123456")
        assert result['currently_borrowed'] == [{'book_id': 1, 'title': 'test', 'author': 'test', 'borrow_date': '2025-07-09', 'due_date': '2025-07-09', 'is_overdue': False}]
        assert result['current_borrow_count'] == 1
        assert result['total_fees'] == 0.00
        assert result['borrowing_history'] == [{'book_id': 1, 'title': 'test', 'author': 'test', 'borrow_date': '2025-07-09', 'due_date': '2025-07-09', 'is_overdue': False}]

        
if __name__ == "__main__":
    unittest.main()