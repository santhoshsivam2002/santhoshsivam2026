Library Management System
A complete Python and MySQL-based Library Management System that digitalizes library operations with automated workflows, member management, and real-time inventory tracking.

🚀 Features
Core Functionalities
Member Registration & Management - New member sign-up with automated welcome system

Book Catalog Management - Comprehensive book database with copy tracking

Borrowing System - Automated checkout with due date calculations

Payment Processing - Multiple payment options (Cash, Card, UPI, Wallet)

Real-time Availability - Live book status and genre-based searching

🛠️ Technology Stack
Backend: Python with MySQL Connector

Database: MySQL with advanced triggers and procedures

Architecture: Object-Oriented Design

Automation: Database triggers for real-time updates


🗄️ Database Schema
-- Core Tables
library_members (member_id, member_name, email, join_date, phone_number)
books (book_id, book_title, book_author, book_isbn, published_year, genre)
book_copies (copy_id, book_id, status)
loans (loan_id, copy_id, member_id, checkout_date, due_date, return_date)
WELCOMELETTER (member_id, status_member, joindate_time)

🔧 Key Database Features
Automated Copy Creation: Trigger auto-creates book copies when new books are added

Member Welcome System: Trigger sends welcome messages upon registration

Advanced Queries: Genre filtering, member activity reports, availability status

💻 Python Application

class LibraryManagementSystem:
    def register_member(self)          # New member registration
    def display_books(self)            # Show available books
    def borrow_book(self, member_id)   # Book checkout process
    def process_payment(self, amount)  # Payment handling


Key Python Features
Database Integration: Secure MySQL connection management

Error Handling: Comprehensive exception handling

User-Friendly CLI: Interactive menu-driven interface

Date Management: Automated due date calculations (14-day loans)

📊 Advanced SQL Queries & Triggers
Sample Queries:
Find available Fiction books

Identify members who never borrowed books

Books published after 2020 with availability status

Automation Triggers:
LIB_MEMBERS_STATUS: Auto-welcome new members

add_first_copy: Auto-create copies for new books

🎯 Business Logic
Loan Period: 14 days standard borrowing

Rental Fee: Fixed pricing structure

Inventory Management: Real-time status tracking

Member Analytics: Borrowing patterns and engagement metrics

🚀 Getting Started
Set up MySQL database with provided schema

Configure database connection in Python script

Run the application for interactive library management

Perfect for educational institutions, community libraries, or as a learning project for database management and Python development!






    


