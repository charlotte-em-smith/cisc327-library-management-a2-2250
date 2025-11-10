#import library_service
from services import library_service
import unittest


class TestR1():
    def test_title(self):
        # test title for existence (passed)
        success, msg = library_service.add_book_to_catalog(None, "test", "1111111111111", 1)
        assert success == False
        assert msg == "Title is required."

        # test title for character limit (passed)
        success, msg = library_service.add_book_to_catalog("AhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhAhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", "test", "hello", 1)
        assert success == False
        assert msg == "Title must be less than 200 characters."

    def test_author(self):
        # test author for existence (passed)
        success, msg = library_service.add_book_to_catalog("test", None, "1111111111111", 1)
        assert success == False
        assert msg == "Author is required."

        # test author for character limit (passed)
        success, msg = library_service.add_book_to_catalog("test", "Ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", "1111111111111", 1)
        assert success == False
        assert msg == "Author must be less than 100 characters."

    def test_ISBN(self):
        # test isbn for 13 digits (less) (passed)
        success, msg = library_service.add_book_to_catalog("test", "test", "111", "1")
        assert success == False
        assert msg == "ISBN must be exactly 13 digits."

    def test_ISBN_chars(self):
        # test isbn for digits not charaters
        success, msg = library_service.add_book_to_catalog("test", "test", "abcabcabcabca", 1)
        assert success == False
        assert msg == "ISBN must be digits, not characters."

    def test_existing_ISBN(self):
        success, msg = library_service.add_book_to_catalog("test", "test", "9780451524935", 1)
        assert success == False
        assert msg == "A book with this ISBN already exists."

    def test_book_number(self):
        # test book number for positive int (passed)
        success, msg = library_service.add_book_to_catalog("test", "test", "1111111111111", -1)
        assert success == False
        assert msg == "Total copies must be a positive integer."

        # test book number for non-zero (passed)
        success, msg = library_service.add_book_to_catalog("test", "test", "1111111111111", 0)
        assert success == False
        assert msg == "Total copies must be a positive integer."

    def test_isb_exists(self):
        # test fnor existing book
        success, msg = library_service.add_book_to_catalog("Sunrise on the Reaping", "F. Scott Fitzgerald", "9780743273565", 7)
        assert success == False
        assert msg == 'A book with this ISBN already exists.' 

    def test_add_book_to_catalogue(self, mocker):
        # test for success message after adding a book  (change before actual thing)
        mocker.patch('services.library_service.get_book_by_isbn', return_value=False)
        mocker.patch('services.library_service.insert_book', return_value=True)

        success, msg = library_service.add_book_to_catalog("Percy Jackson 1", "Suzanne Collins", "2222222222225", 5)
        #assert success == True
        assert "successfully added" in msg  
  

if __name__ == "__main__":
    unittest.main()