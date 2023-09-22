./venv/Scripts/activate.ps1;`
python -m nuitka --mingw64 --disable-console --standalone --onefile --enable-plugin=tk-inter `
--include-data-files=./venv/Lib/site-packages/pymediainfo/MediaInfo.dll=MediaInfo.dll `
--include-data-files=./resources/ffmpeg.exe=ffmpeg.exe `
--company-name="DanRedTMF" `
--product-name="Simple Video Transcoding" `
--product-version="0.0.1" `
--output-filename="Simple Video Transcoding" `
--output-dir="SVT" `
--jobs=4 `
main.py;