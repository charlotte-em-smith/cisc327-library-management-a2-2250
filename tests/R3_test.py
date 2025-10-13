import library_service
import unittest

class testR3(unittest.TestCase):
    def test_R3(self):
        # test patron for existence
        self.assertEqual(library_service.borrow_book_by_patron(None, 1), (False, "Invalid patron ID. Must be exactly 6 digits."))

        # test for valid patron (less)
        self.assertEqual(library_service.borrow_book_by_patron("123", 1), (False, "Invalid patron ID. Must be exactly 6 digits."))

        # test for valid patron (more)
        self.assertEqual(library_service.borrow_book_by_patron("1234567", 1), (False, "Invalid patron ID. Must be exactly 6 digits."))

        # test if book exists 
        self.assertEqual(library_service.borrow_book_by_patron("123456", 9999999999999), (False, "Book not found."))

        # test if patron has gone over borrowing limits
        #for i in range(5):
        #    success, message = library_service.borrow_book_by_patron("111111", 2)
        self.assertEqual(library_service.borrow_book_by_patron("123456", 3), (False, "You have reached the maximum borrowing limit of 5 books."))

        # test if available copies allows borrowing (neg)
        #self.assertEqual(library_service.borrow_book_by_patron("123456", 1), (False, "This book is currently not available."))


if __name__ == "__main__":
    unittest.main()