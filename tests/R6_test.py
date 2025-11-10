#import library_service
from CISC_327_CS.services import library_service
import unittest
from datetime import datetime, timedelta

class TestR6():
    def test_R6(self):
        # test search term for existence
        msg = library_service.search_books_in_catalog(None, "test")
        assert msg == []

        # test type for existence
        msg = library_service.search_books_in_catalog("test", None)
        assert msg == []
    
    def test_case_sensitive_title(self, mocker):
        # test for case sensitive title 
        mocker.patch('CISC_327_CS.services.library_service.get_books_by_title', return_value=[{'author': 'F. Scott Fitzgerald', 'available_copies': 3, 'id': 1, 'isbn': '9780743273565', 'title': 'The Great Gatsby', 'total_copies': 3}])

        msg = library_service.search_books_in_catalog("The Great gatsby", "Title")
        assert any(book['title'] == "The Great Gatsby" for book in msg)
        
    def test_partial_matching_title(self, mocker):  
        # test for partial matching
        mocker.patch('CISC_327_CS.services.library_service.get_books_by_title', return_value=[{'author': 'F. Scott Fitzgerald', 'available_copies': 3, 'id': 1, 'isbn': '9780743273565', 'title': 'The Great Gatsby', 'total_copies': 3}])

        msg = library_service.search_books_in_catalog("The great", "Title")
        assert any(book['title'] == "The Great Gatsby" for book in msg)

    def test_search_w_isbn(self, mocker):
        mocker.patch('CISC_327_CS.services.library_service.get_book_by_isbn', return_value=[{'author': 'F. Scott Fitzgerald', 'available_copies': 3, 'id': 1, 'isbn': '9780743273565', 'title': 'The Great Gatsby', 'total_copies': 3}])

        msg = library_service.search_books_in_catalog("9780743273565", "isbn")
        assert any(book['title'] == "The Great Gatsby" for book in msg)

    def test_search_w_author(self, mocker):
        mocker.patch('CISC_327_CS.services.library_service.get_books_by_author', return_value=[{'author': 'F. Scott Fitzgerald', 'available_copies': 3, 'id': 1, 'isbn': '9780743273565', 'title': 'The Great Gatsby', 'total_copies': 3}])

        msg = library_service.search_books_in_catalog("F. Scott Fitzgerald", "author")
        assert any(book['title'] == "The Great Gatsby" for book in msg)

if __name__ == "__main__":
    unittest.main()