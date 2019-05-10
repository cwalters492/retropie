import os
import shutil

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from console_loader import ConsoleLoader
from rom_loader import RomLoader
from page_manager import PageManager


class Scraper(object):
    driver = None
    base_url = None

    def __init__(self, base_url='http://romhustler.net/', headless=False, download_directory=None):
        self.base_url = base_url
        download_directory = download_directory or os.path.join(os.getcwd(), 'roms')
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "profile.managed_default_content_settings.images": 2,
            'webdriver.load.strategy': 'unstable',
            'disk-cache-size': 4096,
        }
        options.add_experimental_option('prefs', prefs)
        if headless:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(self.base_url)
        self.console_loader = ConsoleLoader(driver=self.driver)
        self.rom_loader = RomLoader(driver=self.driver)

    def scrape(self, all_consoles=False, consoles=None, console=None, all_roms=False, roms=None, rom=None):
        search_consoles = tuple()
        if not all_consoles:
            search_consoles = consoles or tuple(console)
        # If not all_roms, search either roms one at a time or rom
        if not all_roms:
            self.search_many(roms=roms or tuple(rom), consoles=search_consoles)
        # If all_roms, go through all_consoles, consoles, or console and download each
        else:
            for console_name in self.console_loader.iter_consoles(consoles=search_consoles):
                print(f'Starting console "{console_name}"')
                page_manager = PageManager(driver=self.driver, page=1)
                while True:
                    self.rom_loader.download_all_roms()
                    try:
                        page_manager.next()
                    except:
                        break
                try:
                    os.mkdir(f'roms/{console_name}')
                except OSError:
                    pass
                files = os.listdir('roms')
                for fname in files:
                    if not os.path.isdir(f'roms/{fname}'):
                        shutil.move(f'roms/{fname}', f'roms/{console_name}/{fname}')

    def search_many(self, roms=(), consoles=()):
        for rom in roms:
            print(f'Searching for {rom}')
            self.search(rom, consoles=consoles)

    def search(self, rom, consoles=()):
        self.driver.find_element_by_css_selector('.dd_trigger').click()
        for console in consoles:
            try:
                for element in self.driver.find_elements_by_xpath(f'//*[@id="list_consoles"]/li/label[contains(text(), "{console}")]'):
                    element.click()
            except:
                print(f'Could not find console "{console}" in list.')
        search_box = self.driver.find_element_by_xpath('//*[@id="q"]')
        search_box.send_keys(f'{Keys.CONTROL}a{Keys.BACK_SPACE}')
        search_box.send_keys(f'{rom}\n')

    def __iter_consoles(self, console=None, consoles=()):
        if consoles:
            for console_name in consoles:
                console_name = self.console_loader.select_console(console_name=console_name)
                yield console_name
        if console:
            console_name = self.console_loader.select_console(console_name=console)
            yield console_name
        if not console and not consoles:
            console_count = len(self.driver.find_elements_by_css_selector('.atozArea a'))
            console_number = 0
            while console_number < console_count:
                console_name = self.console_loader.select_consoleconsole_number=console_number()
                console_number += 1
                yield console_name


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Scrape romhustler.com for Roms")
    parser.add_argument('--consoles', metavar='Consoles', type=str, nargs='*', help='the name of the consoles whose ROMs you want')
    parser.add_argument('--console', metavar='Console', type=str, nargs='?', help='the name of the console whose ROMs you want')
    parser.add_argument('--roms', metavar='Roms', type=str, nargs='*', help='the name of the ROMs you want')
    parser.add_argument('--rom', metavar='Rom', type=str, nargs='?', help='the name of the ROM you want')
    parser.add_argument('--all_consoles', action='store_true', help='flag to download for all consoles')
    parser.add_argument('--all_roms', action='store_true', help='flag to download all roms')
    parser.add_argument('--headless', action='store_true', help='scrape with headless browser')
    args = parser.parse_args()
    scraper = Scraper(headless=args.headless)
    print(args)
    roms = args.roms or (tuple(args.rom) if args.rom else tuple())
    consoles = args.consoles or (tuple(args.console) if args.console else tuple())
    scraper.scrape(consoles=consoles, roms=roms, all_consoles=args.all_consoles, all_roms=args.all_roms)
