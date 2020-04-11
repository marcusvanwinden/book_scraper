# Import required packages
import bs4
import csv
import requests
import re
import time
import os

BASE_URL = "http://books.toscrape.com/"


def scrape_book_urls(begin=1):
    book_urls = []
    page_url = f"catalogue/page-{begin}.html"
    while page_url:
        print(f"Scraping {BASE_URL}{page_url}")
        response = requests.get(f"{BASE_URL}{page_url}")
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        books = soup.find_all(class_="product_pod")
        book_urls.extend(f"catalogue/{book.h3.a['href']}" for book in books)
        next_button = soup.find(class_="next")
        page_url = f"catalogue/{next_button.a['href']}" if next_button else None
    return book_urls


def scrape_books(book_urls):
    books = []
    current_book = 1
    for book_url in book_urls:
        response = requests.get(f"{BASE_URL}{book_url}")
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1").get_text(strip=True)
        price = float(soup.find(class_="price_color").get_text(strip=True)[2:])
        stock = int(re.search("\d+", soup.find(class_="instock availability").get_text(strip=True)).group())
        books.append({"title": title, "price": price, "stock": stock})
        print(f"Scraping book {current_book}/{len(book_urls)}")
        current_book += 1
    return books


def write_to_csv_file(books):
    current_book = 1
    with open("books.csv", "w") as csv_file:
        fieldnames = ["title", "price", "stock"]
        dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        for book in books:
            print(f"Writing book {current_book}/{len(books)} to the csv file")
            dict_writer.writerow(book)
            current_book += 1
            time.sleep(0.1)


def get_all_books():
    books = []
    with open("books.csv", "r") as csv_file:
        dict_reader = csv.DictReader(csv_file)
        books.extend(book for book in dict_reader)
    return books


def clear_screen():
    os.system("cls") if os.name == "nt" else os.system("clear")
