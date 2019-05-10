import os
import shutil

from rom_loader import RomLoader


class ConsoleLoader(object):
    driver = None
    console_number = None
    console_name = None
    consoles = None
    
    def __init__(self, driver, console_number=None, console_name=None, consoles=None):
        self.driver = driver
        self.console_number = console_number
        self.console_name = console_name
        self.consoles = consoles

    def select_console(self):
        link = self.__find_console()
        if not link:
            if not self.console_name:
                print(f'No Console #{self.console_number}!')
            else:
                print(f'No Console Named {self.console_name}!')
            return
        link.click()

    def iter_consoles(self):
        if self.consoles:
            for console in self.consoles:
                try:
                    link = self.driver.find_element_by_xpath(f'//*[@id="consoles"]/div/div/div[3]/div//a[contains(text(), "{console}")]')
                    link.click()
                    yield console
                except Exception as e:
                    print(f'Cannot find console "{console}" in list.')


    def __find_console(self):
        if self.console_number:
            link = self.driver.find_elements_by_css_selector('.atozArea a')[self.console_number]
            self.console_name = link.text
            if not self.console_name:
                return None
            return link
        elif self.console_name:
            try:
                link = self.driver.find_element_by_link_text(self.console_name)
                return link
            except:
                return None
            pass

    def __move_files_to_console_directory(self):
        try:
            os.mkdir(f'roms/{self.console_name}')
        except OSError:
            pass
        files = os.listdir('roms')
        for fname in files:
            if not os.path.isdir(f'roms/{fname}'):
                shutil.move(f'roms/{fname}', f'roms/{self.console_name}/{fname}')
