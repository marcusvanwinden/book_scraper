import mysql.connector
import operations
import os
import time


database = mysql.connector.connect(
    host = "localhost",
    user = os.environ["DB_USER"],
    password = os.environ["DB_PASS"],
    database = ""
)

cursor = database.cursor()

cursor.execute("DROP DATABASE IF EXISTS bookcase")
cursor.execute("CREATE DATABASE bookcase")
cursor.execute("USE bookcase")
cursor.execute("""
    CREATE TABLE books (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(100) NOT NULL,
        price DECIMAL(5, 2),
        stock INT
    )
""")

if __name__ == "__main__":
    print("Hello! \U0001f600")
    time.sleep(1)
    book_urls = operations.scrape_book_urls(begin=1)
    books = operations.scrape_books(book_urls)
    operations.write_to_csv_file(books)

    try:
        current_book = 1
        for book in books:
            query = "INSERT INTO books (title, price, stock) VALUES (%s, %s, %s)"
            cursor.execute(query, (book["title"], book["price"], book["stock"]))
            print(f"Saving book {current_book}/{len(books)} to the database")
            current_book += 1
            time.sleep(0.1)
    except:
        pass

    database.commit()
    print("Completed!\nNow type 'open books.csv' \U0001f600")
