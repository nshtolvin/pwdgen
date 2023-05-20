# region Import
from re import match

from _libraries.pwd_generator_lib import PwdGen
# endregion

class Menu:
    # default constructor
    def __init__(self, dict_files_path:str) -> None:
        self.__pwd_gen = PwdGen(dict_files_path)
    
    # default destructor
    def __del__(self):
        del(self.__pwd_gen)

    def show_main_menu(self):
        while True:
            print('Please, select password complexity:')
            print('[1] Weak')
            print('[2] Standard')
            print('[3] Strong')
            # print('[4] Custom')
            print('[0] exit')

            switcher = {
                1: 'weak',
                2: 'standard',
                3: 'strong'
                # 4: None
            }

            try:
                # считываем ввведенную пользователем сложность генерируемой парольной фразы
                compl = input('-> ')
                if int(compl) == 0: break

                # считываем количество парольных фраз заданной сложности, которые необходимо сгенерировать
                # по умолчанию генерируется пять парольных фраз; максимально допускается сгенерировать 20 паролей
                print('Please, select the number of generated passphrases [1..20, default = 5]: ', end='')
                pwd_count = input()
                if match(r'^[0-9]+$', pwd_count) is None or int(pwd_count) not in range(1, 21):
                    pwd_count = 5

                # TODO: сформировать описание принципа построения пароля
                # генерируем парольные фразы и выводим пользователю
                for ind in range(int(pwd_count)):
                    passphrase = self.__pwd_gen.generate_passphrase(switcher.get(int(compl)))
                    print(f"{''.join(passphrase[0])}\t {' '.join(passphrase[1])}")
            except Exception:            
                print('Something went wrong. Possibly an invalid input!')
                continue
            except KeyboardInterrupt:
                break


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
