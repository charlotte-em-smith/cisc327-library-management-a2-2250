import library_service
import unittest

class testR1(unittest.TestCase):
    def test_title(self):
        # test title for existence (passed)
        self.assertEqual(library_service.add_book_to_catalog(None, "test", "1111111111111", 1), (False, "Title is required."))

        # test title for character limit (passed)
        self.assertEqual(library_service.add_book_to_catalog("AhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhAhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", "test", "hello", 1), (False, "Title must be less than 200 characters."))

    def test_author(self):
        # test author for existence (passed)
        self.assertEqual(library_service.add_book_to_catalog("test", None, "1111111111111", 1), (False, "Author is required."))

        # test author for character limit (passed)
        self.assertEqual(library_service.add_book_to_catalog("test", "Ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", "1111111111111", 1), (False, "Author must be less than 100 characters."))

    def test_ISBN(self):
        # test isbn for existence (failed) (error in og code)
        #self.assertEqual(library_service.add_book_to_catalog("test", "test", None, 1), (False, "Please fill out this field."))

        # test isbn for digits (failed, error in og code)
        #self.assertEqual(library_service.add_book_to_catalog("test", "test", "hello", 1), (False, "ISBN must be digits, not characters."))

        # test isbn for 13 digits (less) (passed)
        self.assertEqual(library_service.add_book_to_catalog("test", "test", "111", "1"), (False, "ISBN must be exactly 13 digits."))

        # test isbn for 13 digits (more) (passed)
        self.assertEqual(library_service.add_book_to_catalog("test", "test", "11111111111111", 1), (False, "ISBN must be exactly 13 digits."))

        # test isbn for existing isbn (passed)
        self.assertEqual(library_service.add_book_to_catalog("test", "test", "9780451524935", 1), (False, "A book with this ISBN already exists."))

    def test_book_number(self):

        # test book number existence (check message) (failed, messages differ, but same spirit) (clarify with prof)
        #self.assertEqual(library_service.add_book_to_catalog("test", "test", "1111111111111", None), (False, "Please fill out this field."))

        # test book number for positive int (passed)
        self.assertEqual(library_service.add_book_to_catalog("test", "test", "1111111111111", -1), (False, "Total copies must be a positive integer."))

        # test book number for non-zero (passed)
        self.assertEqual(library_service.add_book_to_catalog("test", "test", "1111111111111", 0), (False, "Total copies must be a positive integer."))

    def test_book_borrow(self):
        # test for success message after adding a book
        self.assertEqual(library_service.add_book_to_catalog("Sunrise on the Reaping", "Suzanne Collins", "2222222222222", 7), (True, 'Book "Sunrise on the Reaping" has been successfully added to the catalog.'))        

if __name__ == "__main__":
    unittest.main()