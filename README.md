# simple-video-transcoding
 
## Guidelines
- Python 3.11.7
- Create a virtual environment with ```python -m venv venv```
- Install dependencies with ```pip install -r requirements.txt```
- Run the file `install_ffmpeg.ps1`
- For `FFmpeg` to work correctly when running the program from the console, change the `is_debug` value in the `global_vars.py` file from `False` to `True`

## Create an executable file using `Nuitka`
Make sure that the `is_debug` variable in the `global_vars.py` file is set to `False`. Also, you must have the following components installed in the `Visual Studio Installer`:

![](https://github.com/danredtmf/simple-video-transcoding/blob/main/readme-images/vsi-req.jpg)

The top part of the checkboxes was checked automatically after installing the `Desktop Development with C++` component.

If you are ready, you can run the `nuitka_final.ps1` file, having previously changed the `--company-name` field inside.

## Create an executable file using `pyinstaller`.
Make sure that the `is_debug` variable in the `global_vars.py` file is set to `False`. In this case, it is enough to run the `pyinstaller_final.ps1` file.
