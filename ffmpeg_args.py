class FFMPEGArgs:
    """Класс для удобного передачи информации в функцию создания процесса `ffmpeg`."""
    def __init__(self, input_file: str, output_options: dict[str, str], output_file: str):
        self.input_file = input_file
        self.output_options = output_options
        self.output_file = output_file

    def get_input_file(self):
        """Возвращает `путь\имя.расширение` входного файла в виде строки"""
        return self.input_file

    def get_output_options(self):
        """Возвращает словарь с параметрами для процесса `ffmpeg`"""
        return self.output_options

    def get_output_file(self):
        """Возвращает `путь\имя.расширение` выходного файла в виде строки"""
        return self.output_file
