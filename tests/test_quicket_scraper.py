import pytest
from src.quicket_scraper import parse_event, split_datetime, scrape_page, save_events_to_csv, rate_limit
from requests.exceptions import HTTPError, RequestException
from unittest.mock import patch, Mock
import os
import pandas as pd
import json


# Sample JSON data for testing
sample_event_json = {
    "@context": "https://schema.org",
    "@type": "Event",
    "name": "Test Event",
    "startDate": "2025-02-13T16:00:00Z",
    "endDate": "2025-02-13T20:00:00Z",
    "location": {
        "@type": "Place",
        "name": "Test Venue",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "123 Test Street"
        }
    },
    "url": "https://www.quicket.co.za/events/123456-test-event/"
}

# Test for parsing event JSON
def test_parse_event():
    event = parse_event(sample_event_json)
    
    assert event['Event Title'] == "Test Event"
    assert event['Event Location'] == "Test Venue, 123 Test Street"
    assert event['Start Date'] == "2025-02-13"
    assert event['Start Time'] == "16:00:00"
    assert event['End Date'] == "2025-02-13"
    assert event['End Time'] == "20:00:00"
    assert event['Event URL'] == "https://www.quicket.co.za/events/123456-test-event/"

# Test for splitting datetime strings
def test_split_datetime():
    date_str = "2025-02-13T16:00:00Z"
    date, time = split_datetime(date_str)
    
    assert date == "2025-02-13"
    assert time == "16:00:00"

    # Test with invalid date format
    invalid_date_str = "invalid-date"
    date, time = split_datetime(invalid_date_str)
    
    assert date == "Invalid Date"
    assert time == "Invalid Time"

# Test for saving data to CSV
def test_save_events_to_csv(tmp_path):
    test_events = [
        {
            'Event Title': "Test Event",
            'Event Location': "Test Venue, 123 Test Street",
            'Start Date': "2025-02-13",
            'Start Time': "16:00:00",
            'End Date': "2025-02-13",
            'End Time': "20:00:00",
            'Event URL': "https://www.quicket.co.za/events/123456-test-event/"
        }
    ]
    
    test_file = tmp_path / "test_events.csv"
    save_events_to_csv(test_events, filename=str(test_file))
    
    assert os.path.exists(test_file)
    df = pd.read_csv(test_file)
    assert len(df) == 1
    assert df.iloc[0]['Event Title'] == "Test Event"

# Test for rate limiting
def test_rate_limit(mocker):
    mock_sleep = mocker.patch('time.sleep')
    rate_limit(1, 2)
    assert mock_sleep.call_count == 1
    delay = mock_sleep.call_args[0][0]
    assert 1 <= delay <= 2

# Test for handling invalid URL (HTTPError)
def test_scrape_page_invalid_url(mocker):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = HTTPError("404 Client Error: Not Found for url")
    mocker.patch('quicket_scraper.HTMLSession.get', return_value=mock_response)

    events = scrape_page(999)
    assert events == []

# Test for handling request errors (network issues)
def test_scrape_page_request_error(mocker):
    mocker.patch('quicket_scraper.HTMLSession.get', side_effect=RequestException("Connection error"))

    events = scrape_page(1)
    assert events == []

# Test for handling missing content in event JSON
def test_parse_event_missing_fields():
    incomplete_event_json = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": "Incomplete Event"
    }

    event = parse_event(incomplete_event_json)
    assert event['Start Date'] == 'N/A'
    assert event['Event Location'] == 'N/A, N/A'

# Test for scraping a page (mocked)
def test_scrape_page(mocker):
    mock_html_content = '<script type="application/ld+json">[{}]</script>'.format(json.dumps(sample_event_json))
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.html.render = Mock()
    mock_response.html.html = mock_html_content
    
    mocker.patch('quicket_scraper.HTMLSession.get', return_value=mock_response)

    events = scrape_page(1)
    assert len(events) == 1
    assert events[0]['Event Title'] == "Test Event"

if __name__ == "__main__":
    pytest.main()
