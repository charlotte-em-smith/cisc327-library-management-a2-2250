import library_service
import unittest
from datetime import datetime, timedelta

class testR5(unittest.TestCase):
    def test_R5(self):
        # test for no overdue fees
        self.assertEqual(library_service.borrow_book_by_patron("123458", 2), True, f'Successfully borrowed "To Kill a Mockingbird". Due date: 2025-10-27.')
        result = library_service.calculate_late_fee_for_book("123458", 2)
    
        assert result[1] == 0
        

        # change function to have optional start and end date
        # test for 1 week late (1 week of late fees)
        # self.assertEqual(library_service.calculate_late_fee_for_book("123456", 1), (True, "You currently have $3.50 in late fees for this book."))

        # # test for 2 weeks late (2 weeks of late fees)
        # self.assertEqual(library_service.calculate_late_fee_for_book("123456", 1), (True, "You currently have $10.50 in late fees for this book."))

        # # test for for max late fee for one book (15$)
        # self.assertEqual(library_service.calculate_late_fee_for_book("123456", 1), (True, "You currently have the maximum amount ($15) in late fees for this book."))

if __name__ == "__main__":
    unittest.main()