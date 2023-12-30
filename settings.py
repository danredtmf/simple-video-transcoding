import os
from configparser import ConfigParser
from global_vars import config_name, languages

class Settings():
    def __init__(self) -> None:
        self.__config = ConfigParser()
        self.__load_config()
    
    def __load_config(self) -> None:
        """Загружает конфигурацию"""
        self.__check_config()
    
    def __read_config(self) -> None:
        """Читает конфигурацию из файла"""
        self.__config.read(config_name)

    def __check_config(self) -> None:
        """Проверяет на существование и корректность конфигурации"""
        if not os.path.exists(config_name):
            self.__generate()
            self.save()
            self.__read_config()
        else:
            self.__read_config()
            if self.__has_settings():
                if self.__has_language():
                    if not self.get_language() in languages:
                        self.__generate_language()
                        self.save()
                else:
                    self.__generate_language()
                    self.save()
            else:
                self.__generate()
                self.save()
    
    def __generate(self) -> None:
        """Генерирует секцию `Settings` и / или её опции, если её / их нет"""
        if not self.__has_settings():
            self.__generate_settings()
        if not self.__has_language():
            self.__generate_language()
    
    def __generate_settings(self) -> None:
        """Генерирует секцию `Settings`"""
        self.__config.add_section('Settings')

    def __generate_language(self, language = 'en') -> None:
        """Генерирует опцию `language` в `Settings`"""
        if language in languages:
            self.__config.set('Settings', 'language', language)
        else:
            self.__config.set('Settings', 'language', 'en')
    
    def __has_settings(self) -> bool:
        """Проверяет наличие сукции `Settings`"""
        return True if self.__config.has_section('Settings') else False

    def __has_language(self) -> bool:
        """Проверяет наличие опции `language` в `Settings`"""
        return True if self.__config.has_option('Settings', 'language') else False

    def get_language(self) -> str:
        """Возвращает опцию `language`"""
        return self.__config.get('Settings', 'language')
    
    def set_language(self, language) -> None:
        """Устанавливает значение в опцию `language` секции `Settings`"""
        if self.__has_settings():
            self.__generate_language(language)
            self.save()
        else:
            self.__generate_settings()
            self.__generate_language(language)
            self.save()

    def save(self) -> None:
        """Сохраняет конфигурацию в файл"""
        with open(config_name, 'w') as file:
            self.__config.write(file)
