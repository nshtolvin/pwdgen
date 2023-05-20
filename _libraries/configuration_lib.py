# region Import
from configparser import ConfigParser

from _libraries import logger_lib
# endregion


# Class for configuration
class Config(ConfigParser):
    # default constructor
    def __init__(self, conf_filename):
        super().__init__()
        self.__filename = conf_filename
        self.read(self.__filename)
    
    # read parameters from file
    def read_settings(self):
        self.read(self.__filename)

    # write parameters to file
    def write_settings(self):
        pass

    def get_paraams(self):
        return self.get('passphrase', 'char_count')
