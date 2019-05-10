import os
import re
import shutil


class RomCollection(object):
    base_rom_directory = None

    def __init__(self, base_rom_directory='./roms'):
        self.base_rom_directory = base_rom_directory

    def contains(self, console, rom_title):
        normalized_rom_title = self.__normalize_rom_title(rom_title)
        if not os.path.exists(f'{self.base_rom_directory}/{console}'):
            return False
        for filename in os.listdir(f'{self.base_rom_directory}/{console}'):
            if self.__normalize_rom_filename(filename) == normalized_rom_title:
                return True
        return False

    def add(self, console, file_path):
        try:
            os.mkdir(f'{self.base_rom_directory}/{console}')
        except OSError:
            pass
        _, filename = os.path.split(file_path)
        shutil.move(file_path, f'{self.base_rom_directory}/{console}/{filename}')

    def __normalize_rom_title(self, rom_title):
        normalized_rom_title = re.sub(r'[^0-9a-zA-Z]+', ' ', rom_title)
        normalized_rom_title = normalized_rom_title.lower()
        normalized_rom_title = re.sub(r'( a |a | the |the | a$| the$)', '', normalized_rom_title)
        normalized_rom_title = re.sub(r' ', '', normalized_rom_title)
        return normalized_rom_title.lower()

    def __normalize_rom_filename(self, rom_filename):
        rom_title = rom_filename[:rom_filename.rfind('.')]
        return self.__normalize_rom_title(rom_title)


if __name__ == '__main__':
    collection = RomCollection(base_rom_directory='../roms')
    print(collection.contains(console='Atari 5200', rom_title='5200Basic'))
    print(collection.contains(console='Atari 5200', rom_title='Activision Decathlon, The (1984) (Activision)'))
