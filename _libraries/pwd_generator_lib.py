# region Import
from random import SystemRandom
from math import pow

from _libraries.dict_worker_lib import DictFileWorker
# endregion


# TODO: обеспечить работу с конфигурационными *.ini файлами
# TODO: добавить возможность генеировать парольную фразу с пользовательскими настройками
class PwdGen(DictFileWorker):    
    # части речи слов, которые могут использоваться в составе пароля [прилагательное, наречие, существительное, числительное, глагол]
    PARTS_OF_SPEECH = ['ADJF', 'ADVB', 'NOUN', 'NUMR', 'INFN']

    # наборы символов, которые могут использоваться в составе генерируемого праоля (помимо букв латинского алфавита)
    NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    MINUS = ['-']
    UNDERLINE = ['_']
    SPECIAL = ['!', '?', '"', '#', '$', '%', '&', '\'', '*', '+', ',', '.', '/', ':', ';', '=', '@', '\\', '^', '|', '~']
    BRACKETS = ['(', ')', '[', ']', '{', '}', '<', '>']

    # шаблоны генерируемых парольных фраз - предствляют собой последовательность частей речи
    PASSPHRASE_PATTERNS = {
        2: f'ADJF NOUN',
        3: f'NOUN INFN NOUN',
        4: f'ADJF NOUN INFN NOUN',
        5: f'ADJF NOUN INFN ADJF NOUN',
        6: f'ADJF NOUN ADVB INFN ADJF NOUN'
    }
    # пресеты генерируемых парольных фраз
    # words_count: количество слов, их которых состоит парльная фразаи
    # char_count: количество букв каждого слова, которые используются в генерируемом пароле
    # is_numbers: использовать цифры в составе парольной фразы (в качестве разделителя, префикса или постфикса)
    # is_special: использовать дополнительные символы (спецсимволы) в составе парольной фразы (в качестве разделителя, префикса или постфикса)
    # use_upper_case: использовать заглавную букву в начале каждого слова парольной фразы
    PASSPHRASE_PRESETS = {
        "weak": {
            "words_count": 3,
            "char_count": 3,
            "use_numbers": False,
            "use_special": False,
            "use_upper_case": False
        },
        "standard": {
            "words_count": 4,
            "char_count": 3,
            "use_numbers": True,
            "use_special": False,
            "use_upper_case": True
        },
        "strong": {
            "words_count": 5,
            "char_count": 4,
            "use_numbers": True,
            "use_special": True,
            "use_upper_case": True
        }
    }

    # default constructor
    def __init__(self, dict_files_path:str) -> None:
        super().__init__()
        self.__dictionaries_filenames = {
            'ADJF': f'{dict_files_path}/adjectives.txt',
            'ADVB': f'{dict_files_path}/adverb.txt',
            'NOUN': f'{dict_files_path}/nouns.txt',
            'NUMR': f'{dict_files_path}/numeral.txt',
            'INFN': f'{dict_files_path}/verbs.txt'
        }
        self.__randomizer = SystemRandom()
    
    # default destructor
    def __del__(self):
        del(self.__randomizer)

    def generate_passphrase(self, pwd_complexity: str) -> list:
        """
        Меетод создания нескольких парольных фраз по заданным параметрам
        @param pwd_complexity: сложность генерируемой парольной фразы. Сложеность определяется ключами словаря PASSPHRASE_PRESETS иои пользовательскими настройками
        @return: список сгенерированных парольных фраз
        """
        # считываем параметры генериуемой парольной фразы из стандартных пресетов
        current_settings = self.PASSPHRASE_PRESETS.get(pwd_complexity)
        # определяем шаблон парольной (сложность парольной фразы определяет количество слов в ней, и как следствие - используемый шаблон парольной фразы)
        pwd_ptrn_prts = self.PASSPHRASE_PATTERNS.get(current_settings["words_count"]).split()

        # список для хранения слов парольнаой фразы на русском языке
        rus_passphrase = list()
        # генерация слов, которые войдут в парольную фразу
        for prt in pwd_ptrn_prts:
            rus_passphrase.append(self.__get_random_word(prt).lower())
                
        # получение слов парольной фразы на английском языке
        eng_passphrase = self.__change_layout(rus_passphrase)
                
        # отсекаем первые char_count каждого слова парольной фразы
        eng_passphrase = [word[:current_settings["char_count"]] for word in eng_passphrase]

        # при необходимости меняем регистр первой бкувы каждого слова
        if current_settings["use_upper_case"]:
            rus_passphrase = self.__set_upper_case(rus_passphrase)
            eng_passphrase = self.__set_upper_case(eng_passphrase)
                
        # при необходимости добавляем специальные символы в паролную фразу
        if current_settings["use_special"]:
            # определяем количество специльных символов, которые будут добавлены в парольную фразу
            # с учетом того, что при трансляции слова с русского языка на английский возможно появление специальных символов, программно
            # ограничиваем максимально возможное число добавляемых спецсимволов
            specials_count = self.__randomizer.randint(1, 4)
            for ind in range(specials_count):
                # выбираем специальный символ
                spec_ch = self.__randomizer.choice(self.SPECIAL)
                # определяем позицию, куда специальный символ будет вставлен
                pos = self.__randomizer.randint(0, len(rus_passphrase) + 1)
                # добавляем специальный символ в парольную фразу
                rus_passphrase.insert(pos, spec_ch)
                eng_passphrase.insert(pos, spec_ch)

        # при необходимости добавляем цифры в паролную фразу (пока цифры добавляются только в начало парольной фразы)
        if current_settings["use_numbers"]:
            # определяем количество цифр, которые будут добавлены в парольную фразу
            numbers_count = self.__randomizer.randint(1, 4)
            number = 0
            for ind in range(numbers_count):
                number = number + (int(self.__randomizer.random() * 10) * int(pow(10, ind)))
            rus_passphrase.insert(0, str(number))
            eng_passphrase.insert(0, str(number))

        return [eng_passphrase, rus_passphrase] 
    
    def __change_layout(self, pwd_prts:list) -> list:
        """
        Изменение языка слов, которые будут использоваться в составе парольной фразы. Изменение языка подразумевает замену русских букв на аглийсике
        в соответсвии с клавишами клавиатуры 
        @param pwd_prts: исходный список слов парольной фразы
        @return: преобразованный (замена русских бкв на английские) список слов парольной фразы
        """
        rus_layout = 'йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
        eng_layout = 'qwertyuiop[]asdfghjkl;\'zxcvbnm,.`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>~'

        tr_pwd_prts = list()
        # цикл по элементам списка слов, входящих в парольную фразу
        for ind in range(len(pwd_prts)):
            # далее буквы русского языка заменяются на буквы английского в соответствии с раскладкой
            # инициализация слова парольной фразы после изменения
            tr_wrd = ''
            # цикл, где выполняется замена букв
            for ltr in pwd_prts[ind]:
                tr_wrd = tr_wrd + eng_layout[rus_layout.find(ltr)]
            # pwd_prts[ind] = tr_wrd
            tr_pwd_prts.append(tr_wrd)
        return tr_pwd_prts

    def __set_upper_case(self, pwd_prts:list) -> list:
        """
        Изменение регистра первой буквы каждого слова, которое будет использоваться в составе парольной фразы.
        @param pwd_prts: исходный список слов парольной фразы
        @return: преобразованный (первая буква слова - заглавная) список слов парольной фразы
        """
        return [wrd.capitalize() for wrd in pwd_prts]

    def __get_random_word(self, prt_of_sppech: str) -> str:
        """
        Выбор случайного слова из словаря слов заданной части речи. Считанный файл сичтывается полностью; после из него случайным образом выбирется одно слово. 
        В конце необходимо удалить символ новой строки (\n) для выбранного слова.
        @param prt_of_sppech: [сокращение ~ часть речь] условное обозначение (сокращение) словаря, из которого будут считываться данные (строки)
        @return: случайное слово из словаря, которое далее будет использоваться в составе пароля
        """
        dict_content = self._read_dict_file(self.__dictionaries_filenames[prt_of_sppech])
        return self.__randomizer.choice(dict_content)[:-1]
