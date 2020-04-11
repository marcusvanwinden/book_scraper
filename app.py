# Import required packages
import pyodbc
import operations
import os
import time

# Establish connection with a MSSQL database
connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={os.environ.get('DB_SERVER')};"
    f"DATABASE={os.environ.get('DB_DATABASE')};"
    f"UID={os.environ.get('DB_USER')};"
    f"PWD={os.environ.get('DB_PASSWORD')};",
    autocommit=True
)

# Instantiate cursor
cursor = connection.cursor()

# Drop table Books if it already exists
cursor.execute("""
    IF OBJECT_ID('[dbo].[Books]') IS NOT NULL
        DROP TABLE [dbo].[Books]
""")

# Create the books table
cursor.execute("""
    CREATE TABLE [dbo].[Books] (
        [BookId] INTEGER IDENTITY(1, 1),
        [Title] VARCHAR(100) NOT NULL,
        [Price] DECIMAL(5, 2),
        [Stock] INTEGER,
        CONSTRAINT PK_BookId PRIMARY KEY([BookId])
    )
""")

if __name__ == "__main__":
    # Print welcome screen
    operations.clear_screen()
    print("Hello \U0001f600\n")
    time.sleep(2)
    begin_page = None
    # Ask user for valid page number
    while begin_page not in range(1, 51):
        try:
            print("At what page would you like to start scraping?\n\n"
                  "Please type a number between 1 and 50.\n\n"
                  "The higher the number, the faster the program will be done.\n"
            )
            begin_page = int(input("Number > "))
            if begin_page not in range(1, 51):
                raise Exception()
        except:
            operations.clear_screen()
    # Start scraping
    operations.clear_screen()
    print("Let the scraping begin! \U0001f600")
    time.sleep(2)
    book_urls = operations.scrape_book_urls(begin=begin_page)
    books = operations.scrape_books(book_urls)
    operations.write_to_csv_file(books)

    try:
        current_book = 1
        for book in books:
            query = """
                INSERT INTO [dbo].[Books] (title, price, stock)
                VALUES (?, ?, ?)"""
            cursor.execute(query, (book["title"], book["price"], book["stock"]))
            print(f"Saving book {current_book}/{len(books)} to the database")
            current_book += 1
            time.sleep(0.1)
    except:
        pass

    # Commit data to the database
    connection.commit()
    operations.clear_screen()
    print("Completed!\nNow type 'open books.csv' \U0001f600")
