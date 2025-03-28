# Quicket Web Scraper

## Overview
This Python script scrapes event data from the [Quicket Events](https://www.quicket.co.za/events/) page, including event titles, locations, dates, and times. The data is stored in a CSV file.

## Features
- Scrapes event data from the first 10 pages.
- Extracts event title, location, date, and time.
- Saves the data into a CSV file.
- Implements rate limiting to prevent overloading the server.
- Handles errors gracefully for invalid URLs and missing content.

## Setup Instructions

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Neme88/quicket-web-scraper_app.git
    cd quicket-web-scraper_app
    ```

2. **Set Up Virtual Environment:**
    ```bash
    python or python3 -m venv venv
    ```
    ## Activating the virtual environment: 
    ### For macOS/Linux users:
    ```bash
    source venv/bin/activate
    ```
    ## Activating the virtual environment
    ### For Windows:
    ```bash
    .\venv\Scripts\activate
    ```
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
**Create a .env file and copy BASE_URL in the .env.example file in the root directory**
## For linux/Mac users:
```bash
cp .env.example .env
```
## For windows users:
```bash
copy .env.example .env          # command prompt users
    or
Copy-Item .env.example .env     # PowerShell users. 
```
## Running the Script

To run the web scraper, use:
```bash
python src/run_scraper.py
```
## Running the Tests Script

### For Linux/Mac Users:
```bash
PYTHONPATH=./src pytest tests/
```

### For Windows Users:
set PYTHONPATH=./src && pytest tests/
```
Note:
The PYTHONPATH=./src ensures that Python recognizes the modules inside the `src` directory. Without this, the tests may fail due to import errors.
```
### Test Output
If everything is set correctly, you'll see:
```bash
============================= test session starts =============================
platform linux -- Python 3.10.x, pytest-8.x.x
collected 8 items

tests/test_quicket_scraper.py ........                                      [100%]

============================== 8 passed in 1.20s =============================
```
