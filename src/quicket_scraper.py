from requests.exceptions import RequestException, HTTPError
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
from datetime import datetime

BASE_URL = 'https://www.quicket.co.za/events/?page={}'

def scrape_page(page_number):
    session = HTMLSession()
    url = BASE_URL.format(page_number)
    
    
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise HTTPError for bad status codes
        response.html.render(timeout=30, sleep=5)
    except HTTPError as http_err:
        print(f"HTTP error occurred while fetching page {page_number}: {http_err}")
        return []
    except RequestException as req_err:
        print(f"Request error occurred while fetching page {page_number}: {req_err}")
        return []
    except Exception as e:
        print(f"Unexpected error occurred on page {page_number}: {e}")
        return []
    
    
    soup = BeautifulSoup(response.html.html, 'html.parser')
    json_scripts = soup.find_all('script', type='application/ld+json')

    events = []
    for script in json_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                for event in data:
                    if event.get('@type') == 'Event':
                        events.append(parse_event(event))
            elif data.get('@type') == 'Event':
                events.append(parse_event(data))
        except (json.JSONDecodeError, TypeError):
            continue

    print(f"Found {len(events)} events on page {page_number}")
    return events

def parse_event(event_data):
    """Extract event details from the JSON data and split date/time."""
    
    title = event_data.get('name', 'N/A')
    location = event_data.get('location', {}).get('name', 'N/A')
    address = event_data.get('location', {}).get('address', {}).get('streetAddress', 'N/A')
    url = event_data.get('url', 'N/A')
    
    # Extract start and end date-time strings
    start_datetime_str = event_data.get('startDate', 'N/A')
    end_datetime_str = event_data.get('endDate', 'N/A')
    
    # Convert ISO format to datetime objects for splitting
    start_date, start_time = split_datetime(start_datetime_str)
    end_date, end_time = split_datetime(end_datetime_str)

    return {
        'Event Title': title,
        'Event Location': f"{location}, {address}",
        'Start Date': start_date,
        'Start Time': start_time,
        'End Date': end_date,
        'End Time': end_time,
        'Event URL': url
    }
    
    
def split_datetime(datetime_str):
    """Split an ISO 8601 datetime string into separate date and time components."""
    if datetime_str == 'N/A':
        return 'N/A', 'N/A'
    
    try:
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        date = dt.date().isoformat()
        time = dt.time().strftime('%H:%M:%S')
        return date, time
    except ValueError:
        return 'Invalid Date', 'Invalid Time'

def split_datetime(datetime_str):
    """Split an ISO 8601 datetime string into separate date and time components."""
    if datetime_str == 'N/A':
        return 'N/A', 'N/A'
    
    try:
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        date = dt.date().isoformat()
        time = dt.time().strftime('%H:%M:%S')
        return date, time
    except ValueError:
        return 'Invalid Date', 'Invalid Time'

def save_events_to_csv(events, filename='quicket_events.csv'):
    """
    Saves the scraped events to a CSV file.

    Args:
        events (list): List of event dictionaries to save.
        filename (str): The name of the output CSV file.
    """
    df = pd.DataFrame(events)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    
 # Test rate limiting functionality 
def rate_limit(min_delay=1, max_delay=3):
    """
    Introduces a random delay between requests to prevent server overload.

    Args:
        min_delay (int): Minimum delay in seconds.
        max_delay (int): Maximum delay in seconds.
    """
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
    print(f"Rate limiting applied: sleeping for {delay:.2f} seconds")


