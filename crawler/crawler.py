# crawler.py

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import shelve
from page_handler import PageHandler

class Crawler:
    def __init__(self, base_url, cache_file='visited_urls.db'):
        self.base_url = base_url
        self.visited_urls = shelve.open(cache_file)
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def crawl(self):
        self.driver.get(self.base_url)
        handler = PageHandler(self.driver, self.visited_urls)
        handler.process_page()

        while True:
            current_url = self.driver.current_url
            if current_url not in self.visited_urls:
                self.visited_urls[current_url] = True
                urls = handler.process_page()
                print(f"Found URLs on {current_url}: {len(urls)}")
                
            next_url = handler.get_next_url()
            if next_url and next_url not in self.visited_urls:
                self.driver.get(next_url)
            else:
                break

    def close(self):
        self.visited_urls.close()
        self.driver.quit()
    
    def get_urls(self):
        return self.visited_urls.keys()
        #TODO: return the keys of the visited_urls db
        

# Example usage
crawler = Crawler("https://gptsdex.com")
crawler.crawl()
crawler.close()
