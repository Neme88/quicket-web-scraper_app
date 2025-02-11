
from quicket_scraper import scrape_page, save_events_to_csv, rate_limit

def main():
    """Main function to scrape the first 10 pages of events from Quicket and save to a CSV file."""
    all_events = []
    
    for page in range(1, 11):
        print(f"Scraping page {page}...")
        events = scrape_page(page)
        all_events.extend(events)
        rate_limit()
    
    save_events_to_csv(all_events)

if __name__ == "__main__":
    main()
