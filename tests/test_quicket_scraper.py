import pytest
from src.quicket_scraper import scrape_page 
import time 

# Test successful page fetch
def test_scrape_page_success():
    """
    Test that scraping def test_scrape_page_success():
    """
    events = scrape_page(1)
    assert isinstance(events, list), "Expected result to be a list."
    assert len(events) > 0, "Expected at least one event on the first page."
    
# Test data structure of scraped events
def test_event_data_structure():
    """
    Test that each event contains the expected keys.
    """
    events = scrape_page(1)
    if events:  # Only test structure if events exist
        event = events[0]
        assert 'Event Title' in event, "Missing 'Event Title' key in event data."
        assert 'Event Location' in event, "Missing 'Event Location' key in event data."
        assert 'Event Date' in event, "Missing 'Event Date' key in event data."
        assert 'Event Time' in event, "Missing 'Event Time' key in event data."

# Test handling of invalid page
def test_scrape_invalid_page():
    """
    Test that scraping an invalid page returns an empty list.
    """
    events = scrape_page(9999)  # Assuming this page does not exist
    assert events == [], "Expected an empty list for non-existent pages."

# Test rate limiting functionality
def test_rate_limit():
    """
    Test that rate limiting introduces a delay between requests.
    """
    start_time = time.time()
    rate_limit(1, 2)
    end_time = time.time()
    elapsed_time = end_time - start_time
    assert 1 <= elapsed_time <= 2.5, "Rate limiting did not introduce the correct delay."

