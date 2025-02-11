### quicket_scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

BASE_URL = 'https://www.quicket.co.za/events/?page={}'

def scrape_page(page_number):
    """
    Scrapes event data from a specific page number on Quicket.

    Args:
        page_number (int): The page number to scrape.

    Returns:
        list: A list of dictionaries containing event details.
    """
    url = BASE_URL.format(page_number)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    events = []

    for event in soup.find_all('div', class_='event-card'):
        title = event.find('h3').get_text(strip=True) if event.find('h3') else 'N/A'
        location = event.find('div', class_='location').get_text(strip=True) if event.find('div', class_='location') else 'N/A'
        date = event.find('div', class_='date').get_text(strip=True) if event.find('div', class_='date') else 'N/A'
        time_ = event.find('div', class_='time').get_text(strip=True) if event.find('div', class_='time') else 'N/A'

        events.append({
            'Event Title': title,
            'Event Location': location,
            'Event Date': date,
            'Event Time': time_
        })

    return events


