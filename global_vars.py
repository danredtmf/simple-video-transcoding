import os

ffmpeg_presets: tuple = ('Simple Encoding - Decoding', 'Simple Cut')
video_formats: tuple = ('.ogv', '.mp4 (H264)', '.mp4 (H265)')
video_file_types: tuple = (('Video Files', ('*.mp4', '*.ogv', '*.mkv')),)

win_main_min_size: tuple = ()
win_main_min_size_encdec_simple: tuple = ()

is_debug: bool = False
ffmpeg_path = "./resources/ffmpeg.exe" if is_debug else os.path.join(os.path.dirname(__file__), "ffmpeg.exe")

ffmpeg_output_ogv_theora: dict[str, str] = {'c:v': 'libtheora', 'q:v': '0', 'c:a': 'libvorbis', 'q:a': '0'}
ffmpeg_output_mp4_h264: dict[str, str] = {'c:v': 'libx264'}
ffmpeg_output_mp4_h265: dict[str, str] = {'c:v': 'libx265'}
