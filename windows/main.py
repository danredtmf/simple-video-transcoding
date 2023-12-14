from __future__ import annotations

import asyncio
import threading
import os

import PySimpleGUI as sg
import psutil
import win32con
import win32gui
import win32process
from ffmpeg.asyncio import FFmpeg
from ffmpeg.progress import Progress
from pymediainfo import MediaInfo

from ffmpeg_args import FFMPEGArgs
from global_vars import video_formats, video_file_types, ffmpeg_path, ffmpeg_output_ogv_theora, ffmpeg_output_mp4_h264, \
    ffmpeg_output_mp4_h265
from pathlib import Path

input_file = ""
input_file_frames = 0
video_format = ""
video_preset = ""
output_path = ""
output_name = ""
output_current_frame = 1


def main_window():
    """Логика главного окна"""
    global input_file, output_path, output_name, video_format, video_preset

    # Макет окна
    layout = [
        [
            sg.Text('Input File:', size=(12, 1)),
            sg.Input(readonly=True, key='key:input', enable_events=True),
            sg.FileBrowse(button_text='Select Input', file_types=video_file_types),
        ],
        [
            sg.Text('Video Format:', size=(12, 1)),
            sg.Combo(
                values=video_formats,
                enable_events=True,
                key='key:video_format_list',
                readonly=True,
            ),
        ],
        [
            sg.Text('Output Path:', size=(12, 1)),
            sg.Input(readonly=True, key='key:output', enable_events=True),
            sg.FolderBrowse(button_text='Select Path'),
        ],
        [
            sg.Text('Output Name:', size=(12, 1)),
            sg.Input(key='key:name', enable_events=True),
            sg.Button('Launch'),
        ],
        [
            sg.Text("Progress:", size=(12, 1), key='key:progress_info'),
            sg.ProgressBar(max_value=1, orientation='h', expand_x=True, size=(0, 20), key='key:progress'),
        ]
    ]

    window = sg.Window(title='Simple Video Transcoding', layout=layout, modal=True, finalize=True)

    # События
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == 'key:input':
            input_file = values['key:input']

            if values['key:output'] == '' and values['key:name'] == '':
                output_name = Path(input_file).name.split('.')[0]
                output_path = Path(input_file).parent
                window['key:output'].update(output_path)
                window['key:name'].update(output_name)
        
        if event == 'key:video_format_list':
            video_preset = values['key:video_format_list']
            if video_preset == video_formats[0]:
                video_format = '.ogv'
            elif video_preset == video_formats[1]:
                video_format = '.mp4'
            elif video_preset == video_formats[2]:
                video_format = '.mp4'
        
        if event == 'key:output':
            output_path = values['key:output']
        
        if event == 'Launch':
            if input_file != '' and output_path != '' and video_format != '' and output_name != '':
                output_name = values['key:name']

                if check_output_name() and check_input_file():
                    process_info_input(window)
                    disable_interactive(window)

                    if video_preset == video_formats[0]:
                        asyncio.run(
                            ffmpeg_start(window, FFMPEGArgs(
                                input_file,
                                ffmpeg_output_ogv_theora,
                                get_output_full_file_name()
                            ))
                        )
                    elif video_preset == video_formats[1]:
                        asyncio.run(
                            ffmpeg_start(window, FFMPEGArgs(
                                input_file,
                                ffmpeg_output_mp4_h264,
                                get_output_full_file_name()
                            ))
                        )
                    elif video_preset == video_formats[2]:
                        asyncio.run(
                            ffmpeg_start(window, FFMPEGArgs(
                                input_file,
                                ffmpeg_output_mp4_h265,
                                get_output_full_file_name()
                            ))
                        )
    window.close()


def check_output_name() -> bool:
    """Не пропускает, если файл с таким именем и расширением уже существует"""
    output_name = get_output_file_name()

    # Сравнения имён входного и выходного файла, и имён файлов в папке вывода
    for file in os.listdir(output_path):
        if file == output_name:
            sg.popup("Error!", "Output file name already exists!")
            return False

    return True


def check_input_file() -> bool:
    """Не пускает, если исходного файла не существует"""
    input_path = Path(input_file).parent

    for file in os.listdir(input_path):
        if file == get_input_file_name():
            return True
    
    sg.popup("Error!", "Input file does not exist!")
    return False


def process_info_input(window: sg.Window):
    """Обновляет прогресс-бар перед процессом FFmpeg"""
    global input_file_frames
    media_info = MediaInfo.parse(input_file)
    for track in media_info.tracks:
        if track.track_type == "Video":
            input_file_frames = int(track.to_data()['frame_count'])
            window['key:progress'].update(max=input_file_frames, current_count=output_current_frame)
            window['key:progress_info'].update(get_progress_percent_string())
            break


def get_progress_percent():
    """Возвращает прогресс процесса в процентах"""
    return round((output_current_frame / input_file_frames) * 100)


def get_progress_percent_string():
    """Возвращает прогресс процесса в процентах в виде строки"""
    return f'Progress: {get_progress_percent()}%'


def get_input_file_name():
    """Возвращает `имя.расширение` входного файла"""
    return f'{Path(input_file).name.split(".")[0]}.{Path(input_file).name.split(".")[-1]}'


def get_output_file_name():
    """Возвращает `имя.расширение` выходного файла"""
    global output_name, video_format
    return f'{output_name}{video_format}'


def get_output_full_file_name():
    """Возвращает `путь\имя.расширение` выходного файла"""
    global output_path
    return f'{Path(output_path).joinpath(get_output_file_name())}'


def minimize_cb(handle, pid):
    """Вызываемая функция при сворачивании окна. Также, данная функция скрывает окно из панели задач"""
    _, process_id = win32process.GetWindowThreadProcessId(handle)
    if process_id == pid:
        win32gui.ShowWindow(handle, win32con.SW_HIDE)


def minimize(pid):
    """Сворачивание окна"""
    try:
        win32gui.EnumWindows(minimize_cb, pid)
    except Exception as e:
        print('minimize failed', e)


def minimize_ffmpeg_process():
    """Функция, отвечающая за сворачивания окна консоли вывода процесса `ffmpeg`.\n
    Бесконечно ищет процесс `ffmpeg`, затем скрывает её. Данную функцию нужно запускать в отдельном потоке."""
    process_name = "ffmpeg"
    pid = None

    while pid is None:
        for proc in psutil.process_iter():
            if process_name in proc.name():
                pid = proc.pid
                break

    minimize(pid)


def disable_interactive(window: sg.Window):
    """Выключает интерактивные элементы"""
    window["Select Input"].update(disabled=True)
    window['key:video_format_list'].update(disabled=True)
    window["Select Path"].update(disabled=True)
    window['key:name'].update(disabled=True)
    window['Launch'].update(disabled=True)


def enable_interactive(window: sg.Window):
    """Включает интерактивные элементы"""
    window["Select Input"].update(disabled=False)
    window['key:video_format_list'].update(disabled=False)
    window["Select Path"].update(disabled=False)
    window['key:name'].update(disabled=False)
    window['Launch'].update(disabled=False)


async def ffmpeg_start(window: sg.Window, ffmpeg_args: FFMPEGArgs):
    """Запускает процесс `ffmpeg` асинхронно."""
    ffmpeg = (
        FFmpeg(executable=ffmpeg_path)
        .input(ffmpeg_args.get_input_file())
        .output(
            ffmpeg_args.get_output_file(),
            ffmpeg_args.get_output_options()
        )
    )

    @ffmpeg.on("start")
    def on_start(_arguments: list[str]):
        threading.Thread(target=minimize_ffmpeg_process).start()

    @ffmpeg.on("stderr")
    def on_stderr(_line):
        pass

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        global output_current_frame
        output_current_frame = progress.frame
        window['key:progress'].update(current_count=output_current_frame)
        window['key:progress_info'].update(get_progress_percent_string())
        print(get_progress_percent_string())

    @ffmpeg.on("completed")
    def on_completed():
        global output_current_frame
        output_current_frame = 1
        window['key:progress'].update(max=1, current_count=0)
        window['key:progress_info'].update('Progress:')
        enable_interactive(window)
        os.startfile(os.path.realpath(output_path))
        print("completed")

    @ffmpeg.on("terminated")
    def on_terminated():
        print("terminated")
        enable_interactive(window)

    await ffmpeg.execute()
