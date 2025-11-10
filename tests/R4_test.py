#import library_service
from ..services import library_service
#import database
from .. import database
#from CISC_327_CS import database
import unittest

class TestR4():
    def test_R4(self):
        # test patron for existence
        success, msg = library_service.return_book_by_patron(None, 1)
        assert success == False
        assert msg == "Invalid patron ID. Must be exactly 6 digits."

        # test patron for too short
        success, msg = library_service.return_book_by_patron("123", 1)
        assert success == False
        assert msg == "Invalid patron ID. Must be exactly 6 digits."

    def test_book_id_existence(self):
        # test book id for existence
        success, msg = library_service.return_book_by_patron("123456", None)
        assert success == False
        assert msg == 'Invalid book id.'

    def test_book_returned_by_patron(self):
        # test if book was borrowed by patron
        success, msg = library_service.return_book_by_patron("123457", 1)
        assert success == False
        assert msg == 'Invalid book id.'

    def test_availability_error_returning_book(self, mocker):
        mocker.patch('CISC_327_CS.services.library_service.get_patron_borrowed_books', return_value=[{'book_id': 1, 'title': 'test', 'author' : "test", "borrow_date" : "2025-07-09", "return_date": "2025-07-09",  'is_overdue': '2025-010-11'}])
        mocker.patch('CISC_327_CS.services.library_service.update_book_availability', return_value=False)

        result = library_service.return_book_by_patron('123456', 1)
        assert result == (False, "Error changing availibility.")       

    
    def test_updating_error_returning_book(self, mocker):
        mocker.patch('CISC_327_CS.services.library_service.get_patron_borrowed_books', return_value=[{'book_id': 1, 'title': 'test', 'author' : "test", "borrow_date" : "2025-07-09", "return_date": "2025-07-09",  'is_overdue': '2025-010-11'}])
        mocker.patch('CISC_327_CS.services.library_service.update_borrow_record_return_date', return_value=False)

        result = library_service.return_book_by_patron('123456', 1)
        assert result == (False, "Error updating borrow record.")

    def test_returning_book(self, mocker):
        mocker.patch('CISC_327_CS.services.library_service.get_patron_borrowed_books', return_value=[{'book_id': 1, 'title': 'test', 'author' : "test", "borrow_date" : "2025-07-09", "return_date": "2025-07-09",  'is_overdue': '2025-010-11'}])

        success, msg = library_service.return_book_by_patron('123456', 1)
        assert success == True
        assert "Successfully returned" in msg

if __name__ == "__main__":
    unittest.main()