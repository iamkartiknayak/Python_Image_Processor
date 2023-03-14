import os

from gui import Ui_MainWindow

default_target_dir = []


class FetchUsername(Ui_MainWindow):
    '''Class inherited from gui.py to access GUI elements'''

    def __init__(self):
        super().__init__()

    def getDefaultTargetDirectoryPath(self):
        '''Function handles fetching username and creating default target directory'''
        global default_target_dir

        home_directory = os.path.expanduser("~")
        default_target_dir.append(f"{home_directory}\IPEdits")
        if not os.path.exists(default_target_dir[0]):
            os.mkdir(default_target_dir[0])

        self.display_target_path.setText(
            default_target_dir[0].replace("\\", "/"))
        return default_target_dir
