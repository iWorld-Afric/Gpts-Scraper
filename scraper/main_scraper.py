import requests
from bs4 import BeautifulSoup
from scraper.data_processor import process_and_save_data
from scraper.url_tracker import track_url, is_url_visited
# from crawler.crawler import get_urls # This import is no longer necessary for the new function
import shelve
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def scrape_page(url):
    if is_url_visited(url):
        return f"Skipped {url}"

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        raw_text = ' '.join([element.get_text().strip() for element in soup.find_all(['p', 'h1'])])
        process_and_save_data(url, raw_text)
        track_url(url)
        return f"Completed {url}"
    except Exception as e:
        return f"Error at {url}: {e}"

def scrape_website_from_db(db_path, filter_path, max_workers=10):
    # Open the visited URLs database and filter the URLs
    with shelve.open(db_path) as db:
        urls_to_scrape = [url for url in db.keys() if filter_path in url]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(scrape_page, url): url for url in urls_to_scrape}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                print(data)  # Printing the result of each completed future
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")

# Example usage
# This will need to be updated to reflect the new function usage or removed.
# scrape_website("https://gptsdex.com", "/gpt-store/", 2)
