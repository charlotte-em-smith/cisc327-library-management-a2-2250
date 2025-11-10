#import library_service
from ..services import library_service
import unittest
from datetime import datetime, timedelta

class TestR5():
    def test_late_fee_invalid_id(self, mocker):
        success, msg = library_service.calculate_late_fee_for_book("12345", 1)
        assert success == False
        assert msg == "Invalid patron ID. Must be exactly 6 digits."

    def test_no_overdue_fees(self, mocker):
        # test for no overdue fees
        mocker.patch('CISC_327_CS.services.library_service.get_patron_borrowed_books', return_value=[{'book_id': 1, 'title': 'test', 'author' : "test", "borrow_date" : "2025-07-09", "due_date": "2025-07-09",  'is_overdue': False}])

        result = library_service.calculate_late_fee_for_book("123458", 1)
    
        assert result['days_overdue'] == 0
        assert result['fee_amount'] == 0.00
        assert result['status'] == 'No late fee'

    def test_one_week_late(self, mocker):
        # test for 1 week late (1 week of late fees)
        mocker.patch('CISC_327_CS.services.library_service.get_patron_borrowed_books', return_value=[{'book_id': 1, 'title': 'test', 'author' : "test", "borrow_date" : "2025-07-09", "due_date": "2025-07-09",  'is_overdue': False}])

        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)
        result = library_service.calculate_late_fee_for_book("123458", 1, start_date, end_date)
    
        assert result['days_overdue'] == 7
        assert result['fee_amount'] == 3.50
        assert result['status'] == 'Acquired late fees'

    def test_two_weeks_late(self, mocker):
        # test for 2 week late (2 week of late fees)
        mocker.patch('CISC_327_CS.services.library_service.get_patron_borrowed_books', return_value=[{'book_id': 1, 'title': 'test', 'author' : "test", "borrow_date" : "2025-07-09", "due_date": "2025-07-09",  'is_overdue': False}])

        start_date = datetime.now()
        end_date = start_date + timedelta(days=14)
        result = library_service.calculate_late_fee_for_book("123458", 1, start_date, end_date)
    
        assert result['days_overdue'] == 14
        assert result['fee_amount'] == 10.50
        assert result['status'] == 'Acquired late fees'

    def test_max_late_fee(self, mocker):
        # test for for max late fee for one book (15$)
        mocker.patch('CISC_327_CS.services.library_service.get_patron_borrowed_books', return_value=[{'book_id': 1, 'title': 'test', 'author' : "test", "borrow_date" : "2025-07-09", "due_date": "2025-07-09",  'is_overdue': False}])

        start_date = datetime.now()
        end_date = start_date + timedelta(days=21)
        result = library_service.calculate_late_fee_for_book("123458", 1, start_date, end_date)
    
        assert result['days_overdue'] == 21
        assert result['fee_amount'] == 15.00
        assert result['status'] == 'Max amount of late fees'
        

if __name__ == "__main__":
    unittest.main()