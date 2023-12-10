./venv/Scripts/activate.ps1;`
pyinstaller --windowed --onefile `
--add-binary "./resources/ffmpeg.exe;."`
--add-binary "./venv/Lib/site-packages/pymediainfo/MediaInfo.dll;."`
--name "Simple Video Transcoding" main.py;