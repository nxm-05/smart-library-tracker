import sqlite3
from datetime import date

# Initialize database and trigger
def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Create books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            genre TEXT,
            status TEXT,
            pages INTEGER,
            read_pages INTEGER
        )
    ''')

    # Create alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            message TEXT,
            date TEXT
        )
    ''')

    # Drop trigger if it exists
    cursor.execute('DROP TRIGGER IF EXISTS book_finished_alert')

    # Create trigger
    cursor.execute('''
        CREATE TRIGGER book_finished_alert
        AFTER UPDATE ON books
        WHEN new.read_pages >= new.pages
        BEGIN
            INSERT INTO alerts(message, date) 
            VALUES ('You finished reading ' || new.title, DATE('now'));
        END;
    ''')

    conn.commit()
    conn.close()

# Add a book
def add_book():
    title = input("Book title: ")
    author = input("Author: ")
    genre = input("Genre: ")
    pages = int(input("Total pages: "))
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books(title, author, genre, status, pages, read_pages)
        VALUES (?, ?, ?, 'reading', ?, 0)
    ''', (title, author, genre, pages))
    conn.commit()
    conn.close()
    print(f"Book '{title}' added!")

# Update progress
def update_progress():
    book_id = int(input("Book ID to update: "))
    pages_read = int(input("Pages read: "))
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET read_pages = read_pages + ? WHERE id = ?', (pages_read, book_id))
    conn.commit()
    conn.close()
    print(f"Updated book ID {book_id} with {pages_read} pages read!")

# Show all books
def show_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    print("\n=== BOOKS ===")
    for b in books:
        print(f"ID: {b[0]}, Title: {b[1]}, Author: {b[2]}, Genre: {b[3]}, Status: {b[4]}, Pages: {b[5]}, Read: {b[6]}")

# Show alerts
def show_alerts():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts')
    alerts = cursor.fetchall()
    conn.close()
    print("\n=== ALERTS ===")
    for alert in alerts:
        print(alert[0])

import pandas as pd

# Show analytics
def show_analytics():
    conn = sqlite3.connect('library.db')
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()

    if df.empty:
        print("No books in library yet!")
        return

    print("\n=== LIBRARY ANALYTICS ===")
    # Total books
    print(f"Total books: {len(df)}")
    # Total pages read
    print(f"Total pages read: {df['read_pages'].sum()}")
    # Average completion %
    df['completion'] = df['read_pages'] / df['pages'] * 100
    print(f"Average completion: {df['completion'].mean():.2f}%")
    # Books fully read
    finished = df[df['read_pages'] >= df['pages']]
    print(f"Books finished: {len(finished)}")

# Main Menu
def main_menu():
    while True:
        print("\n1. Add Book\n2. Update Progress\n3. Show Books\n4. Show Alerts\n5. Analytics\n6. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            update_progress()
        elif choice == '3':
            show_books()
        elif choice == '4':
            show_alerts()
        elif choice == '5':
            show_analytics()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Run program
init_db()
main_menu()