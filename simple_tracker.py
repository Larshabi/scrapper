import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from amazon_config import get_chrome_web_driver, get_web_driver_options, set_automation_as_head_less, set_browser_as_incognito, set_ignore_certificate_error, DIRECTORY, NAME, CURRENCY, FILTERS, BASE_URL
from selenium.webdriver.common.by import By


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
        if not links:
            print("Stopped script")
            return
        print(f"Got {len(links)} links to the products")
        print("Getting info about products")
        products = self.get_product_info(links)
        return None
        
    def get_product_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products
    def get_asins(self, links):
        return [self.get_asin(link) for link in links]
    
    @staticmethod
    def get_asin(product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]
    
    def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - getting data")
        product_short_url = self.get_shorten_url(asin)
        self.driver.get(f"{product_short_url}?language=en_GB")
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        
        if title and seller and price:
            product_info = {
                'asin':asin,
                'url':product_short_url,
                'title':title,
                'seller':seller,
                'price':price
             }
            return product_info
        return None
    
    def get_title(self):
        pass
    
    def get_seller(self):
        pass
    
    def get_price(self):
        pass
        
    def get_shorten_url(self, asin):
        return self.base_url + 'dp/' + asin
        
    def get_product_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element("xpath", '//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_item)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get(f"{self.driver.current_url}{self.price_filter}")
        print(f"our url is {self.driver.current_url}")
        result_list = self.driver.find_elements(By.CLASS_NAME, 's-result-item')
        links = []
        try:
            i = 0 
            while i < len(result_list):
                results = result_list[i].find_elements("xpath", "//div/div/div/div/div/div[2]/div/div/div[1]/h2/a")
                links =  [link.get_attribute('href') for link in results]
                i = i + 1
            return links
        except Exception as e:
            print("Did not get any product")
            print(e)
        return links
    
if __name__ == '__main__':
    am = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = am.run()
    