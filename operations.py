from bs4 import BeautifulSoup
from csv import DictWriter, DictReader
from requests import get
from re import search
from time import sleep


BASE_URL = "http://books.toscrape.com/"


def scrape_book_urls(begin=1):
    book_urls = []
    page_url = f"catalogue/page-{begin}.html"
    while page_url:
        print(f"Scraping {BASE_URL}{page_url}")
        response = get(f"{BASE_URL}{page_url}")
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all(class_="product_pod")
        book_urls.extend(f"catalogue/{book.h3.a['href']}" for book in books)
        next_button = soup.find(class_="next")
        page_url = f"catalogue/{next_button.a['href']}" if next_button else None
    return book_urls


def scrape_books(book_urls):
    books = []
    current_book = 1
    for book_url in book_urls:
        response = get(f"{BASE_URL}{book_url}")
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1").get_text(strip=True)
        price = float(soup.find(class_="price_color").get_text(strip=True)[2:])
        stock = int(search("\d+", soup.find(class_="instock availability").get_text(strip=True)).group())
        books.append({"title": title, "price": price, "stock": stock})
        print(f"Scraping book {current_book}/{len(book_urls)}")
        current_book += 1
    return books


def write_to_csv_file(books):
    current_book = 1
    with open("books.csv", "w") as csv_file:
        fieldnames = ["title", "price", "stock"]
        dict_writer = DictWriter(csv_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        for book in books:
            print(f"Writing book {current_book}/{len(books)} to the csv file")
            dict_writer.writerow(book)
            current_book += 1
            sleep(0.1)


def get_all_books():
    books = []
    with open("books.csv", "r") as csv_file:
        dict_reader = DictReader(csv_file)
        books.extend(book for book in dict_reader)
    return books
