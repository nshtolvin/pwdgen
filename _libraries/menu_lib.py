# region Import
from re import match

from _libraries.pwd_generator_lib import PwdGen
# endregion

class Menu:
    # default constructor
    def __init__(self, dict_files_path:str, conf_filename:str) -> None:
        self.__pwd_gen = PwdGen(dict_files_path, conf_filename)
    
    # default destructor
    def __del__(self):
        del(self.__pwd_gen)
    
    def show_main_menu(self):
        # считываем пресеты (наборы параметров) исходя из которых будут формироваться парольные фразы
        # здесь они нужны для формирования пользовательского меню
        pwd_presets = self.__pwd_gen.get_passphrase_presets()
        
        # формируем словарь, используемый как меню
        switcher = dict()
        ind = 1
        for key in pwd_presets.keys():
            switcher[ind] = key
            ind = ind + 1
        
        while True:
            # вывод меню, исходя из ранее сформированного словаря switcher
            print('Please, select password complexity:')
            for key in switcher.keys():
                print(f'    [{key}] {switcher[key].capitalize()}')
            print('\nPassphrase options')
            print('    [5] Show current custom passphrase options')
            print('    [6] Set custom passphrase options')
            print('[0] exit')

            # switcher = {1: 'weak', 2: 'standard', 3: 'strong', 4: 'custom'}
            try:
                # считываем ввведенную пользователем сложность генерируемой парольной фразы  или выбранный пункт меню
                compl_input = input('-> ')
                if int(compl_input) == 0: break
                if int(compl_input) == 5:
                    self.__pwd_gen.show_passphrase_options('custom')
                    continue
                if int(compl_input) == 6:
                    # задание параметров пользовательского парольной фразы
                    self.__pwd_gen.set_custom_passphrase_options()
                    pwd_presets = self.__pwd_gen.get_passphrase_presets()
                    continue
                # определяем сложность генерируемого пароля из пресетов (=str)
                compl = switcher.get(int(compl_input))

                # считываем количество парольных фраз заданной сложности, которые необходимо сгенерировать
                # по умолчанию генерируется пять парольных фраз; максимально допускается сгенерировать 20 паролей
                print('Please, select the number of generated passphrases [1..20, default = 5]: ', end='')
                pwd_count = input()
                if match(r'^[0-9]+$', pwd_count) is None or int(pwd_count) not in range(1, 21):
                    pwd_count = 5
                
                print()
                # генерируем парольные фразы и выводим пользователю
                for ind in range(int(pwd_count)):
                    passphrase = self.__pwd_gen.generate_passphrase(compl)
                    print(f"{''.join(passphrase[0])}\t {' '.join(passphrase[1])}")
                
                print(f'\n[Note]\nThe password is formed from the first {pwd_presets[compl]["char_count"]} letters of each word.')
                print(f'Numbers are used only at the beginning of the password; special characters are used as separators between words')
            except Exception:            
                print('Something went wrong. Possibly an invalid input!')
                continue
            except KeyboardInterrupt:
                break
            finally:
                print()
            
            # compl_input = input('-> ')
            # if int(compl_input) == 0: break
            #     # задание параметров пользовательского парольной фразы
            # if int(compl_input) == 5:
            #     self.__pwd_gen.show_passphrase_options('custom')
            #     continue
            # if int(compl_input) == 6:
            #     self.__pwd_gen.set_custom_passphrase_options()
            #     pwd_presets = self.__pwd_gen.get_passphrase_presets()
            #     continue
            #     # определяем сложность генерируемого пароля из пресетов (=str)
            # compl = switcher.get(int(compl_input))

            #     # считываем количество парольных фраз заданной сложности, которые необходимо сгенерировать
            #     # по умолчанию генерируется пять парольных фраз; максимально допускается сгенерировать 20 паролей
            # print('Please, select the number of generated passphrases [1..20, default = 5]: ', end='')
            # pwd_count = input()
            # if match(r'^[0-9]+$', pwd_count) is None or int(pwd_count) not in range(1, 21):
            #     pwd_count = 5
                    
            #     # генерируем парольные фразы и выводим пользователю
            # for ind in range(int(pwd_count)):
            #     passphrase = self.__pwd_gen.generate_passphrase(compl)
            #     print(f"{''.join(passphrase[0])}\t {' '.join(passphrase[1])}")
                
            # print(f'\n[Note]\nThe password is formed from the first {pwd_presets[compl]["char_count"]} letters of each word.')
            # print(f'Numbers are used only at the beginning of the password; special characters are used as separators between words\n')

    # pwdgen = XKCD(None)
    # while True:
    #     print('Please, select password complexity:')
    #     print('[1] Weak')
    #     print('[2] Normal')
    #     print('[3] Strong')
    #     print('[4] Custom')
    #     print('[0] exit')

    #     switcher = {
    #         1: pwdgen.weak,
    #         2: pwdgen.normal,
    #         3: pwdgen.strong,
    #         4: pwdgen.custom
    #     }

    #     inpt = input('-> ')
    #     try:
    #         if int(inpt) == 0: break
    #         pwd_fun = switcher.get(int(inpt))
    #         print(pwd_fun())
    #     except Exception:            
    #         print('Something went wrong. Possibly an invalid input!')
    #         continue
    # del(pwdgen)
