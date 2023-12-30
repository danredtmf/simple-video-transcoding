import os

video_formats: tuple = ('.ogv', '.mp4 (H264)', '.mp4 (H265)')
video_file_types: tuple = (('Video Files', ('*.mp4', '*.ogv', '*.mkv')),)

is_debug: bool = False
ffmpeg_path = "./resources/ffmpeg.exe" if is_debug else os.path.join(os.path.dirname(__file__), "ffmpeg.exe")

ffmpeg_output_ogv_theora: dict[str, str] = {'c:v': 'libtheora', 'q:v': '0', 'c:a': 'libvorbis', 'q:a': '0'}
ffmpeg_output_mp4_h264: dict[str, str] = {'c:v': 'libx264'}
ffmpeg_output_mp4_h265: dict[str, str] = {'c:v': 'libx265'}

version = '1.0.0'
languages = ('en', 'ru')
config_name = 'config.ini'
config = None

# 1.1 Чтобы выбрать исходный видеофайл, нажмите кнопку "Select Input"
# 1.2 Найдите и выберете видеофайл в появившемся окне и нажмите кнопку "Открыть"
# 2.1 Выберете видеоформат из списка "Video Format"
# 3.1 Чтобы выбрать путь экспорта, нажмите кнопку "Select Path" (опционально)
# 3.2 Выберете каталог, куда хотите сохранить выходной видеофайл, и нажмите кнопку "Выбор папки"
# 4.1 Поменяйте имя выходного файла в поле "Output Name" (если файла с таким именем и расширением нет в каталоге экспорта)
# 5.1 Чтобы начать процесс конвертирования, нажмите кнопку "Launch"
# 6.1 Ожидайте окончания процесса конвертирования. В начале может появится или появится / исчезнуть пустое окно командной строки - это нормально.
# 7.1 После завершения процесса конвертирования программа откроет каталог, где был сохранен выходной файл.
# Поздравляем! Вы знаете, как пользоваться "Simple Video Transcoding"!
tutorial_text = '''1.1 To select the source video file, click the "Select Input" button
1.2 Locate and select a video file in the window that appears and click the "Open" button
2.1 Select a video format from the "Video Format" list
3.1 To select the export path, click the "Select Path" button (optional)
3.2 Select the directory where you want to save the output video file and click the "Select Folder" button
4.1 Change the output file name in the "Output Name" field (if there is no file with such name and extension in the export directory)
5.1 To start the conversion process, click the "Launch" button
6.1 Wait for the end of the conversion process. A blank command prompt window may appear or appear / disappear at the beginning - this is normal.
7.1 When the conversion process is complete, the program will open the directory where the output file was saved.
\nCongratulations! You know how to use "Simple Video Transcoding"!'''

about_text = f'''Simple Video Transcoding
Version {version}
Author: DanRedTMF'''