#import library_service
#import database
from services import library_service
from unittest.mock import Mock
from unittest.mock import patch
import database
#from CISC_327_CS import database
import unittest


class TestR3():
    def test_valid_patron(self):
        # test patron for existence
        success, msg = library_service.borrow_book_by_patron(None, 1)
        assert success == False
        assert msg == "Invalid patron ID. Must be exactly 6 digits."
    
    def test_valid_patron_less(self):
        # test for valid patron (less)
        success, msg = library_service.borrow_book_by_patron("123", 1)
        assert success == False
        assert msg == "Invalid patron ID. Must be exactly 6 digits."

    def test_valid_patron_more(self):
        # test for valid patron (more)
        success, msg = library_service.borrow_book_by_patron("1234567", 1)
        assert success == False
        assert msg == "Invalid patron ID. Must be exactly 6 digits."

    def test_invalid_book_id(self):
        # test for invalid book id 
        success, msg = library_service.borrow_book_by_patron("123456", 9999999999999)
        assert success == False
        assert msg == "Book not found."

    def test_copy_not_available(self, mocker):
        mocker.patch('services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test', 'available_copies': 0})

        success, msg = library_service.borrow_book_by_patron("123456", 1)
        assert success == False
        assert msg == "This book is currently not available."

    def test_borrow_book_database_error(self, mocker):
        mocker.patch('services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test', 'available_copies': 3})
        mocker.patch('services.library_service.get_patron_borrow_count', return_value=2)
        mocker.patch('services.library_service.insert_borrow_record', return_value=False)

        result = library_service.borrow_book_by_patron('123456', 1)
        assert result == (False, "Database error occurred while creating borrow record.")

    def test_book_availability_database_error(self, mocker):
        mocker.patch('services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test', 'available_copies': 3})
        mocker.patch('services.library_service.get_patron_borrow_count', return_value=2)
        mocker.patch('services.library_service.update_book_availability', return_value=False)

        result = library_service.borrow_book_by_patron('123456', 1)
        assert result == (False, "Database error occurred while updating book availability.")

    def test_max_borrow_limits(self, mocker):
        mocker.patch('services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test', 'available_copies': 3})
        mocker.patch('services.library_service.get_patron_borrow_count', return_value=6)

        result = library_service.borrow_book_by_patron('123456', 1)
        assert result == (False, "You have reached the maximum borrowing limit of 5 books.")

    def test_borrow_book(self, mocker):
        mocker.patch('services.library_service.get_book_by_id', return_value={'id': 1, 'title': 'test', 'available_copies': 3})
        mocker.patch('services.library_service.get_patron_borrow_count', return_value=1)

        success, msg = library_service.borrow_book_by_patron("123458", 8)
        assert "Successfully borrowed" in msg
        assert success == True


if __name__ == "__main__":
    unittest.main()