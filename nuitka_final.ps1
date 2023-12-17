./venv/Scripts/activate.ps1;`
python -m nuitka --clang --disable-console --standalone --onefile --enable-plugin=tk-inter `
--include-data-files=./venv/Lib/site-packages/pymediainfo/MediaInfo.dll=MediaInfo.dll `
--include-data-files=./resources/ffmpeg.exe=ffmpeg.exe `
--nofollow-import-to=pyinstaller `
--company-name="" `
--product-name="Simple Video Transcoding" `
--product-version="1.0.0" `
--output-filename="Simple Video Transcoding" `
--output-dir="SVT" `
--jobs=6 `
main.py;