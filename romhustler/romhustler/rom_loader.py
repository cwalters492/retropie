import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RomLoader(object):
    rom_name = None
    rom_number = None
    driver = None

    def __init__(self, driver, rom_number=None, rom_name=None):
        self.driver = driver
        self.rom_number = rom_number
        self.rom_name = rom_name

    def download_all_roms(self):
        roms = self.driver.find_elements_by_css_selector('#roms_table a')
        rom_count = len(roms)
        for rom_number in range(3, rom_count):  # Start at 3 to skip the header links in the table
            print(rom_number, '/', len(self.driver.find_elements_by_css_selector('#roms_table a')))
            self.download_rom(rom_number=rom_number)
            rom_number += 1

    def download_rom(self, rom_number):
        roms = self.driver.find_elements_by_css_selector('#roms_table a')
        rom = roms[rom_number]
        if rom.text:
            rom_url = f'{rom.get_attribute("href")}'
            rom_text = rom.text
            self.driver.get(rom_url)
            if self.__rom_is_esa_protected():
                print(f'Skipping rom {rom_text} because it is ESA protected!')
                self.driver.back()
                return
            downloads = self.driver.find_elements_by_css_selector('.download_list a')
            download_count = len(downloads)
            download_number = 0
            while download_number < download_count:
                self.__download_from_link(download_number)
                download_number += 1
            self.driver.back()

    def __rom_is_esa_protected(self):
        try:
            self.driver.find_element_by_css_selector('#esa_notice')
            print('true')
            return True
        except Exception as e:
            return False

    def __find_rom_url(self):
        roms = self.driver.find_elements_by_css_selector('#roms_table a')
        if self.rom_number:
            rom = roms[self.rom_number]
            if rom.text:
                rom_url = f'{rom.get_attribute("href")}'
                self.driver.get(rom_url)

    def __download_from_link(self, download_number):
        downloads = self.driver.find_elements_by_css_selector('.download_list a')
        download = downloads[download_number]
        url = download.get_attribute('href')
        self.driver.get(url)
        self.__wait_for_download()
        while True:
            try:
                start_download_button = self.driver.find_element_by_link_text('here')
                start_download_button.click()
                break
            except Exception as e:
                time.sleep(1)
                if 'no such element' not in str(e):
                    raise
        self.driver.back()

    def __wait_for_download(self):
        while True:
            time.sleep(1)
            files = os.listdir('roms')
            for fname in files:
                if fname.endswith('.crdownload'):
                    break
            else:
                return
