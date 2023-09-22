from __future__ import annotations

import asyncio
import threading

import PySimpleGUI as sg
import psutil
import win32con
import win32gui
import win32process
from ffmpeg.asyncio import FFmpeg
from ffmpeg.progress import Progress
from pymediainfo import MediaInfo

from ffmpeg_args import FFMPEGArgs
from global_vars import video_formats, video_file_types, ffmpeg_path, ffmpeg_output_ogv_theora, ffmpeg_output_mp4_h264
from pathlib import Path

input_file = ""
input_file_frames = 0
video_format = ""
output_path = ""
output_name = ""
output_current_frame = 1


def make_simple_video_transcoding_window():
    global input_file, output_path, output_name, video_format
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

    window = sg.Window(title='Simple Video Transcoding', layout=layout, modal=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'key:input':
            input_file = values['key:input']
            output_name = Path(input_file).name.split('.')[0]
            output_path = Path(input_file).parent

            window['key:output'].update(output_path)
            window['key:name'].update(output_name)
        if event == 'key:video_format_list':
            ext = values['key:video_format_list']
            if ext == video_formats[0]:
                video_format = '.ogv'
            elif ext == video_formats[1]:
                video_format = '.mp4'
        if event == 'key:output':
            output_path = values['key:output']
        if event == 'Launch':
            if input_file != '' and output_path != '' and video_format != '' and output_name != '':
                output_name = values['key:name']
                if check_output_name():
                    process_info_input(window)
                    threading.Thread(target=minimize_ffmpeg_process).start()
                    if video_format == video_formats[0]:
                        asyncio.run(
                            ffmpeg_start(window, FFMPEGArgs(
                                input_file,
                                ffmpeg_output_ogv_theora,
                                get_output_full_file_name()
                            ))
                        )
                    elif video_format == video_formats[1].split()[0]:
                        asyncio.run(
                            ffmpeg_start(window, FFMPEGArgs(
                                input_file,
                                ffmpeg_output_mp4_h264,
                                get_output_full_file_name()
                            ))
                        )
    window.close()


def check_output_name() -> bool:
    output_prompt = get_input_file_name()
    output_full_name = get_output_file_name()
    if output_prompt == output_full_name:
        sg.popup("Error!", "Output file name already exists!")
        return False
    return True


def process_info_input(window: sg.Window):
    global input_file_frames
    media_info = MediaInfo.parse(input_file)
    for track in media_info.tracks:
        if track.track_type == "Video":
            input_file_frames = int(track.to_data()['frame_count'])
            window['key:progress'].update(max=input_file_frames, current_count=output_current_frame)
            window['key:progress_info'].update(get_progress_percent_string())


def get_progress_percent():
    return round((output_current_frame / input_file_frames) * 100)


def get_progress_percent_string():
    return f'Progress: {get_progress_percent()}%'


def get_input_file_name():
    return f'{Path(input_file).name.split(".")[0]}.{Path(input_file).name.split(".")[-1]}'


def get_output_file_name():
    global output_name, video_format
    return f'{output_name}{video_format}'


def get_output_full_file_name():
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
    process_name = "ffmpeg"
    pid = None

    while pid is None:
        for proc in psutil.process_iter():
            if process_name in proc.name():
                pid = proc.pid
                break

    minimize(pid)


async def ffmpeg_start(window: sg.Window, ffmpeg_args: FFMPEGArgs):
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
        # print("arguments:", arguments)
        pass

    @ffmpeg.on("stderr")
    def on_stderr(_line):
        # print("stderr:", line)
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
        print("completed")
        window['key:progress'].update(max=1, current_count=0)
        window['key:progress_info'].update('Progress:')

    @ffmpeg.on("terminated")
    def on_terminated():
        print("terminated")

    await ffmpeg.execute()
