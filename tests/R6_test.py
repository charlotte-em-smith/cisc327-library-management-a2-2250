import library_service
import unittest
from datetime import datetime, timedelta

class testR6(unittest.TestCase):
    def test_R6(self):
        # test search term for existence
        self.assertEqual(library_service.search_books_in_catalog(None, "test"), [])
        #self.assertEqual(library_service.search_books_in_catalog(None, "test"), (False, "Search term is required."))

        # test type for existence
        self.assertEqual(library_service.search_books_in_catalog("test", None), [])
        #self.assertEqual(library_service.search_books_in_catalog("test", None), (False, "Search type is required."))

        # test for case sensitive title
        self.assertEqual(library_service.search_books_in_catalog("Test sensitive cases", "Title"), ["The Hunger Games"])
        #self.assertEqual(library_service.search_books_in_catalog("The Hunger games", "Title"), (True, "Search is successful"))   

        # test for partial matching
        self.assertEqual(library_service.search_books_in_catalog("The Hung", "Title"), ["The Hunger Games"])
        #self.assertEqual(library_service.search_books_in_catalog("1111111111111", "ISBN"), (True, "Search is successful"))

if __name__ == "__main__":
    unittest.main()