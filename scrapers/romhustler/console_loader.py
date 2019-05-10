

class ConsoleLoader(object):
    driver = None
    
    def __init__(self, driver):
        self.driver = driver

    def select_console(self, console_number=None, console_name=None):
        link = self.__find_console(console_number=console_number, console_name=console_name)
        if not link:
            if not console_name:
                print(f'No Console #{console_number}!')
            else:
                print(f'No Console Named {console_name}!')
            return
        link_text = link.text
        link.click()
        return link_text

    def iter_consoles(self, consoles):
        if consoles:
            for console in consoles:
                try:
                    link = self.driver.find_element_by_xpath(f'//*[@id="consoles"]/div/div/div[3]/div//a[contains(text(), "{console}")]')
                    link.click()
                    yield console
                except Exception as e:
                    print(f'Cannot find console "{console}" in list.')

    def __find_console(self, console_name=None, console_number=None):
        if console_number:
            try:
                link = self.driver.find_elements_by_css_selector('.atozArea a')[console_number]
                if not link.text:
                    return None
            except:
                return None
            return link
        elif console_name:
            try:
                link = self.driver.find_element_by_link_text(console_name)
                return link
            except:
                return None
