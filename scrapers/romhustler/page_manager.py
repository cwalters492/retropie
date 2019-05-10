from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PageManager(object):
    driver = None
    page = None

    def __init__(self, driver, page=1):
        self.driver = driver
        self.page = page

    def next(self):
        try:
            self.page += 1
            self.driver.find_element_by_xpath('//*[@class="pagi_nav"]//a[contains(text(), "next")]').click()
        except:
            print(f'Failed to reach page {self.page + 1}')
            self.page -= 1
            raise


if __name__ == '__main__':
    from scraper import Scraper
    scraper = Scraper(base_url='http://romhustler.net/roms/atari2600')
    page_manager = PageManager(driver=scraper.driver)
    while True:
        try:
            page_manager.next()
        except:
            break
    print('Done!')
