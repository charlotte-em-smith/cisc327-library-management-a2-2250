"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_books_by_author, get_books_by_title, get_borrow_records, get_patron_borrow_count, get_patron_borrowed_books,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if isbn.isdigit() != True:
        return False, "ISBN must be digits, not characters."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

# return book is implemented (minor changes to make)
def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.

    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to return
        
    Returns:
        tuple: (success: bool, message: str)
    
    TODO: Implement R4 as per requirements
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book has been borrowed by patron
    books = get_patron_borrowed_books(patron_id)
    #borrowed_book = {}
    borrowed = False
    for book in books:
        if book_id == int(book["book_id"]):
            borrowed = True
            #borrowed_book = book
            break
    if borrowed == False:
        return False, "Invalid book id."
    
    # Change availibility of book
    #fix this error message
    availibility_success = update_book_availability(book_id, 1)
    if availibility_success == False:
        return False, "Error changing availibility."
    
    # Update borrow record
    #fix error message
    return_date = datetime.now()
    return_success = update_borrow_record_return_date(patron_id, book_id, return_date)
    if return_success == False:
        return False, "Error updating borrow record."
    
    #somehow change patron_borrowed_books, and remove the book returned
    #not gonna worry about this until I need to (ie it breaks something else)

    return True, f'Successfully returned "{book["title"]}". Return date: {return_date.strftime("%Y-%m-%d")}.'

#late fees is implemented.
def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    
    TODO: Implement R5 as per requirements 
    
    
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """

    #assume borrow_redcords returns return_date as well, if not adjust it so it does
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book has been borrowed by patron
    books = get_patron_borrowed_books(patron_id)
    borrowed = False
    for book in books:
        if book_id == int(book["book_id"]):
            borrowed = True
            break
    if borrowed == False:
        return False, books

    if book["is_overdue"] == False:
        return { 
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'No late fee'
    }

    late_fee = 0
    due_date = book["due_date"]
    return_date = book["return_date"]

    diff = return_date - due_date

    #calculate late fees
    if diff >= timedelta(days=7):
        late_fee += 0.5*7
        if diff > timedelta(days=18):
            late_fee += 11.5
        else:
            late_fee += diff.days - 7
    else:
        late_fee += 0.5*int(diff.days)

    #return fee amounts
    return { 
        'fee_amount': late_fee,
        'days_overdue': diff.days,
        'status': 'Acquired late fees'
    }
    
#search is implemented
def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    
    TODO: Implement R6 as per requirements
    """
    #title, author, isbn
    #do error checking here
    if search_type == "isbn":
        book = get_book_by_isbn(search_term)
    elif search_type == "title" or search_type == "Title":
        search_term = search_term.title()       
        book = get_books_by_title(search_term)
    elif search_type == "author" or search_type == "Author":
        search_term = search_term.title()
        book = get_books_by_author(search_term)
    else:
        book = None
    
    
    if book == None:
        return [search_type == "Title"] 
    return book

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.

    - Currently borrowed books with due dates
    - Total late fees owed  
    - Number of books currently borrowed
    - Borrowing history
    
    TODO: Implement R7 as per requirements
    """
    # Currently borrowed books
    current_borrow_records = get_patron_borrowed_books(patron_id)

    # Number of currently borrowed books
    borrow_count = get_patron_borrow_count(patron_id)

    # Total late fees
    total_fees = 0
    for record in current_borrow_records:
        ans = calculate_late_fee_for_book(patron_id, record)
        total_fees += ans['fee_amount']

    # Borrowing history
    borrow_history = get_borrow_records(patron_id)

    return {
        'currently_borrowed': current_borrow_records,
        'current_borrow_count': borrow_count,
        'total_fees': total_fees,
        'borrowing_history': borrow_history
    }
