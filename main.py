# region Import
from os import path
from re import split
# endregion


# region Params
DIR_BASE = '/'.join(split(r'[\\/]', path.abspath(__file__))[:-1])
DIR_DICTIONARIES = DIR_BASE + '/_dictionaries'
CONFIG = 'conf.ini'
# endregion


def main():    
    from _libraries.menu_lib import Menu

    menu = Menu(DIR_DICTIONARIES, CONFIG)
    menu.show_main_menu()
    del(menu)


if __name__ in '__main__':
    main()
