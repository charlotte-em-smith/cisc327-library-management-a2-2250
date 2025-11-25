import pytest
from playwright.sync_api import Page, expect
import datetime
from datetime import datetime, timedelta

def test_e2e_1(page: Page):
    # End-to-end testing: User opens catalogue. User goes to search page.
    # User searches for 'To Kill a Mockingbird', and borrows it.
    # User goes to return book page, and returns 'To Kill a Mockingbird'.

    # Go to catalogue
    page.goto("http://127.0.0.1:5000/catalog")

    # Get search page, and check it has correct heading
    page.get_by_role("link", name="Search").click()
    expect(page.get_by_role("heading", name="Search Books")).to_be_visible()

    # Fill in the search term, as well as the search type. Then press search
    page.get_by_label("Search Term").fill("To Kill a Mockingbird")
    page.select_option("select#type", value="title")
    page.get_by_role("button", name="🔍 Search").click()

    # Check out the book that was searched
    page.fill('input[name="patron_id"]', "123456")
    page.get_by_role("button", name="Borrow").click()

    # Go to book Return Book, check it has correct heading
    page.get_by_role("link", name="Return Book").click()
    expect(page.get_by_role("heading", name="Return Book")).to_be_visible()

    # Fill out info to return the book, and return it
    page.fill('#patron_id', '123456')
    page.fill('#book_id', "2")
    page.get_by_role("button", name="Process Return").click()

    # Ensure it was properly returned
    expect(page.get_by_text('Successfully returned "How to Kill a Mockingbird". Return date: ' + str(datetime.now().isoformat()) + "."))


def test_e2e_2(page: Page):
    # End-to-end testing: User opens catalogue. User goes to add book page.
    # User adds 'Six of Crows', and borrows it.
    # User goes to return book page, and returns 'Six of Crows'.

    # Go to catalogue
    page.goto("http://127.0.0.1:5000/catalog")

    # Get add book page, and check it has correct heading
    page.get_by_role("link", name="Add Book").click()
    expect(page.get_by_role("heading", name="Add New Book")).to_be_visible()

    # Fill in title, author isbn and total copies for new book
    page.get_by_label("Title *").fill("Six of Crows")
    page.get_by_label("Author *").fill("Leigh Bardugo")
    page.get_by_label("ISBN *").fill("3333333333333")
    page.get_by_label("Total Copies *").fill("3")

    # Submit new book fields
    page.get_by_role("button", name="Add Book to Catalog").click()

    # Check that book was added
    expect(page.get_by_text('Book "Six of Crows" has been successfully added to the catalog.')).to_be_visible()

    # Get back to catalog page, and check it has correct heading
    page.get_by_role("link", name="Catalog").click()
    expect(page.get_by_role("heading", name="Book Catalog")).to_be_visible()

    # Borrow newly added book
    page.get_by_text('Six of Crows').locator('xpath=ancestor::tr').locator('input[name="patron_id"]').fill('123458')
    page.get_by_text('Six of Crows').locator('xpath=ancestor::tr').locator('button.btn-success').click()

    # Ensure it was succesfully borrowed
    expect(page.get_by_text("Successfully borrowed 'Six of Crows'. Due date: " + str((datetime.now() + timedelta(days=14)).isoformat())))

    # Obtain the book id of new book
    book_id = page.get_by_text('Six of Crows').locator('xpath=ancestor::tr').locator('input[name="book_id"]').get_attribute('value')

    # Go to book Return Book, check it has correct heading
    page.get_by_role("link", name="Return Book").click()
    expect(page.get_by_role("heading", name="Return Book")).to_be_visible()
    
    # Return the book
    page.fill('#patron_id', '123458')
    page.fill('#book_id', book_id)
    page.get_by_role("button", name="Process Return").click()

    # Ensure it was properly returned
    expect(page.get_by_text('Successfully returned "HSix of Crows". Return date: ' + str(datetime.now().isoformat()) + "."))

    

