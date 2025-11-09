#import library_service
from CISC_327_CS.services import library_service
import unittest
from datetime import datetime, timedelta

class testR5(unittest.TestCase):
    def test_R5(self):
        # test for no overdue fees
        self.assertEqual(library_service.borrow_book_by_patron("123458", 2), (True, f'Successfully borrowed "To Kill a Mockingbird". Due date: 2025-10-27.'))
        result = library_service.calculate_late_fee_for_book("123458", 2)
    
        assert result['days_overdue'] == 0
        assert result['fee_amount'] == 0.00
        assert result['status'] == 'No late fee'

    def test_one_week_late(self):
        # test for 1 week late (1 week of late fees)
        library_service.return_book_by_patron("123458", 2)
        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)
        self.assertEqual(library_service.borrow_book_by_patron("123458", 2), (True, f'Successfully borrowed "To Kill a Mockingbird". Due date: 2025-10-27.'))
        result = library_service.calculate_late_fee_for_book("123458", 2, start_date, end_date)
    
        assert result['days_overdue'] == 7
        assert result['fee_amount'] == 3.50
        assert result['status'] == 'Acquired late fees'

    def test_two_weeks_late(self):
        # test for 2 week late (2 week of late fees)
        library_service.return_book_by_patron("123458", 2)
        start_date = datetime.now()
        end_date = start_date + timedelta(days=14)
        self.assertEqual(library_service.borrow_book_by_patron("123458", 2), (True, f'Successfully borrowed "To Kill a Mockingbird". Due date: 2025-10-27.'))
        result = library_service.calculate_late_fee_for_book("123458", 2, start_date, end_date)
    
        assert result['days_overdue'] == 14
        assert result['fee_amount'] == 10.50
        assert result['status'] == 'Acquired late fees'

    def test_max_late_fee(self):
        # test for for max late fee for one book (15$)
        library_service.return_book_by_patron("123458", 2)
        start_date = datetime.now()
        end_date = start_date + timedelta(days=21)
        self.assertEqual(library_service.borrow_book_by_patron("123458", 2), (True, f'Successfully borrowed "To Kill a Mockingbird". Due date: 2025-10-27.'))
        result = library_service.calculate_late_fee_for_book("123458", 2, start_date, end_date)
    
        assert result['days_overdue'] == 21
        assert result['fee_amount'] == 15.00
        assert result['status'] == 'Max amount of late fees'
        

if __name__ == "__main__":
    unittest.main()