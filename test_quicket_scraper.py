from quicket_scraper import scrape_page 

# Test successful page fetch

def test_scrape_page_success():
    """
    Test that scraping def test_scrape_page_success():

    Test that scraping the first page returns a list of events.
    
    events = scrape_page(1)
    assert isinstance(events, list), "Expected result to be a list."
    assert len(events) > 0, "Expected at least one event on the first page."
    the first page returns a list of events.
    """
    events = scrape_page(1)
    assert isinstance(events, list), "Expected result to be a list."
    assert len(events) > 0, "Expected at least one event on the first page."
