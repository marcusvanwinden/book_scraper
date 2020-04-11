# Book Scraper

### Prerequisites

1. Install the Microsoft ODBC Driver for SQL Server<br>(https://docs.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)
2. Set environment variable DB_SERVER="<YOUR_SERVER>"
3. Set environment variable DB_DATABASE="<YOUR_DATABASE>"
4. Set environment variable DB_USER="<YOUR_USER>"
5. Set environment variable DB_PASSWORD="<YOUR_PASSWORD>"

### Installation

1. Download the project
2. Open the terminal and change directory to the project folder
3. Type "python3 -m venv venv"
4. Type "source/venv/bin/activate"
5. Type "pip3 install -r requirements.txt"
6. Type "python3 app.py"

### Description

This program scrapes a thousand books from a website, stores it in a CSV file, and inserts it into a MySQL database.
