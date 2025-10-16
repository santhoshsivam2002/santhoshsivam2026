import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import sys

class LibraryManagementSystem:
    def __init__(self):
        self.connection = None
        self.connect_to_database()
        
    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='globallibrary',
                user='root',  # Change if needed
                password='Rajalakshmi@2025'   # Add your MySQL password here
            )
            
            if self.connection.is_connected():
                print("Successfully connected to the database")
                
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            sys.exit(1)
    
    def register_member(self):
        print("\n--- New Member Registration ---")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")
        
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO library_members (member_name, email, join_date, phone_number) VALUES (%s, %s, %s, %s)"
            join_date = datetime.now().date()
            values = (name, email, join_date, phone)
            
            cursor.execute(query, values)
            self.connection.commit()
            
            print(f"\nRegistration successful! Welcome to Global Library, {name}!")
            print(f"Your details: Name: {name}, Email: {email}, Phone: {phone}")
            
            return cursor.lastrowid  # Return the new member ID
            
        except Error as e:
            print(f"Error registering member: {e}")
            return None
    
    def display_books(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT b.book_id, b.book_title, b.book_author, b.book_isbn, b.published_year, b.genre, 
                   bc.copy_id, bc.status
            FROM books b
            LEFT JOIN book_copies bc ON b.book_id = bc.book_id
            ORDER BY b.book_title
            """
            
            cursor.execute(query)
            books = cursor.fetchall()
            
            print("\n--- Available Books at Global Library ---")
            print("{:<5} {:<30} {:<20} {:<15} {:<10} {:<15} {:<10}".format(
                "ID", "Title", "Author", "ISBN", "Year", "Genre", "Status"
            ))
            print("-" * 105)
            
            for book in books:
                print("{:<5} {:<30} {:<20} {:<15} {:<10} {:<15} {:<10}".format(
                    book['book_id'],
                    book['book_title'][:27] + '...' if len(book['book_title']) > 27 else book['book_title'],
                    book['book_author'][:17] + '...' if len(book['book_author']) > 17 else book['book_author'],
                    book['book_isbn'],
                    book['published_year'],
                    book['genre'],
                    book['status']
                ))
                
            return True
            
        except Error as e:
            print(f"Error fetching books: {e}")
            return False
    
    def borrow_book(self, member_id):
        isbn = input("\nEnter the ISBN of the book you want to borrow: ")
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Check if book exists and is available
            query = """
            SELECT b.book_id, bc.copy_id, b.book_title, b.book_author
            FROM books b
            JOIN book_copies bc ON b.book_id = bc.book_id
            WHERE b.book_isbn = %s AND bc.status = 'Available'
            LIMIT 1
            """
            
            cursor.execute(query, (isbn,))
            book = cursor.fetchone()
            
            if not book:
                print("Book not available for borrowing.")
                return False
            
            # Calculate dates
            checkout_date = datetime.now().date()
            due_date = checkout_date + timedelta(days=14)  # 2 weeks loan period
            
            # Create loan record
            loan_query = """
            INSERT INTO loans (copy_id, member_id, checkout_date, due_date)
            VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(loan_query, (book['copy_id'], member_id, checkout_date, due_date))
            
            # Update book status
            update_query = "UPDATE book_copies SET status = 'Checked Out' WHERE copy_id = %s"
            cursor.execute(update_query, (book['copy_id'],))
            
            self.connection.commit()
            
            print(f"\nYou have successfully borrowed '{book['book_title']}' by {book['book_author']}")
            print(f"Checkout date: {checkout_date}")
            print(f"Due date: {due_date}")
            
            # Calculate price (simple fixed price for demo)
            price = 5.00  # $5 for all books
            print(f"\nThe rental fee for this book is: ${price:.2f}")
            
            return price
            
        except Error as e:
            print(f"Error borrowing book: {e}")
            return False
    
    def process_payment(self, amount):
        print("\n--- Payment Options ---")
        print("1. Cash")
        print("2. Credit/Debit Card")
        print("3. GPay/UPI")
        print("4. Library Wallet")
        
        option = input("Select payment method (1-4): ")
        
        if option in ['1', '2', '3', '4']:
            print(f"Payment of ${amount:.2f} processed successfully!")
            return True
        else:
            print("Invalid payment option.")
            return False
    
    def run(self):
        print("=" * 50)
        print("      WELCOME TO GLOBAL LIBRARY")
        print("=" * 50)
        
        # Check if user is a member
        is_member = input("Are you already a member? (y/n): ").lower()
        
        if is_member == 'y':
            # For simplicity, we'll just register as new member
            # In a real system, you would verify existing members
            print("Please provide your details to continue:")
            member_id = self.register_member()
        else:
            member_id = self.register_member()
        
        if not member_id:
            print("Registration failed. Exiting.")
            return
        
        # Show available books
        if not self.display_books():
            return
        
        # Allow borrowing
        price = self.borrow_book(member_id)
        if not price:
            return
        
        # Process payment
        if self.process_payment(price):
            print("\nThank you for your payment!")
            print("Your book has been successfully checked out.")
            print("Please return it by the due date to avoid late fees.")
        else:
            print("Payment failed. Please try again.")
        
        print("\nThank you for visiting Global Library!")
        print("We hope to see you again soon!")

# Run the application
if __name__ == "__main__":
    library_system = LibraryManagementSystem()
    library_system.run()
