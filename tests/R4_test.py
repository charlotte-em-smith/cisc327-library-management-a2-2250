import library_service
import database
import unittest

class testR4(unittest.TestCase):
    def test_R4(self):
        # test patron for existence
        self.assertEqual(library_service.return_book_by_patron(None, 1), (False, "Invalid patron ID. Must be exactly 6 digits."))

        # test book id for existence
        self.assertEqual(library_service.return_book_by_patron(123456, None), (False, 'Invalid book id.'))

        # test if book was borrowed by patron
        self.assertEqual(library_service.return_book_by_patron(123456, 1), (False, 'Invalid book id.'))

        # test for update of available copies
        # test book availibility function on a book that shouldn't increase (7/7 copies available)
        self.assertEqual(database.update_book_availability(1, 1), False)

        # test book availibility function on a book that souldn't decrease (no books left)
        self.assertEqual(database.update_book_availability(1, -1), False)

        # test for late fees displayed
        success, message = library_service.return_book_by_patron(123456, 1)
    
        assert success == True
        assert "due in late fees" in message

if __name__ == "__main__":
    unittest.main()