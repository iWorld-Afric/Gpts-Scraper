# page_handler.py

from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import utils

class PageHandler:
    def __init__(self, driver, visited_urls_db):
        self.driver = driver
        self.visited_urls_db = visited_urls_db

    def process_page(self):
        while True:
            self.scroll_page_to_end()
            new_urls = self.extract_urls()
            self.write_urls_to_db(new_urls)
            if not self.click_load_more():
                break

    def scroll_page_to_end(self):
        utils.scroll_to_bottom(self.driver)

    def click_load_more(self):
        try:
            load_more_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mantine-Button-root span.mantine-Button-label"))
            )
            load_more_button.click()
            time.sleep(3)
            return True
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            return False

    def extract_urls(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        urls = set()
        for link in soup.find_all('a', href=True):
            full_url = urljoin(self.driver.current_url, link['href'])
            if full_url not in self.visited_urls_db:
                urls.add(full_url)
        return urls

    def write_urls_to_db(self, urls):
        for url in urls:
            if url not in self.visited_urls_db:
                print(f"New URL found: {url}")
                self.visited_urls_db[url] = True
