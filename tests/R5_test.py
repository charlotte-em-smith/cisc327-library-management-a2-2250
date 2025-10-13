import library_service
import unittest
from datetime import datetime, timedelta

class testR5(unittest.TestCase):
    def test_R5(self):
        # test for 2 weeks of borrowing time
        success, message = library_service.calculate_late_fee_for_book("123456", 1)
    
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=14)
        assert success == True
        assert due_date in message
        
        # test for 1 week late (1 week of late fees)
        self.assertEqual(library_service.calculate_late_fee_for_book("123456", 1), (True, "You currently have $3.50 in late fees for this book."))

        # test for 2 weeks late (2 weeks of late fees)
        self.assertEqual(library_service.calculate_late_fee_for_book("123456", 1), (True, "You currently have $10.50 in late fees for this book."))

        # test for for max late fee for one book (15$)
        self.assertEqual(library_service.calculate_late_fee_for_book("123456", 1), (True, "You currently have the maximum amount ($15) in late fees for this book."))

if __name__ == "__main__":
    unittest.main()