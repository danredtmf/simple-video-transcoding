import PySimpleGUI as sg

from windows.main import main_window
from settings import Settings
import global_vars

sg.theme('dark grey 2')

if __name__ == '__main__':
    global_vars.config = Settings()
    main_window()
