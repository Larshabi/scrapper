import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from amazon_config import get_chrome_web_driver, get_web_driver_options, set_automation_as_head_less, set_browser_as_incognito, set_ignore_certificate_error, DIRECTORY, NAME, CURRENCY, FILTERS, BASE_URL


class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self, search_item, filters, base_url, currency) -> None:
        self.base_url = base_url
        self.search_item = search_item
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver =  get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"
        
    def run(self):
        print("Starting script")
        print(f"looking for {self.search_item} products...")
        links = self.get_product_links()
        print(links)
        return None
        
    def get_product_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element("xpath", '//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_item)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get(f"{self.driver.current_url}{self.price_filter}")
        print(f"our url is {self.driver.current_url}")
        time.sleep(2)
        result_list = self.driver.find_elements("class_name", 's-result-list')
        links = []
        try:
            results = result_list[0].find_elements("xpath", "//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
            links =  [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Did not get any product")
            print(e)
        return links
    
if __name__ == '__main__':
    am = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = am.run()
    