from PIL import Image
from PyQt6 import QtCore, QtWidgets
import os
import webbrowser
from datetime import datetime
import time

from gui import Ui_MainWindow
from show_dialog import showDialog
from fetch_edits import filters, enhancements, size, file_format, compress_flag
from fetch_files import selected_images, src_dir, target_dir
from switch_selection import SwitchSelection
from generate_logs import generateLog, start_time, start_time_count, img_quality

stop_flag = [False]
image_original_date = ""


class ApplyEdits(Ui_MainWindow):
    '''Class inherited from gui.py to access GUI elements'''

    def __init__(self):
        super().__init__()

    def applyEditsAndSaveImage(self):
        '''Function handles applying and saving images along with generating logs'''
        global img_quality
        if not os.path.exists(target_dir[0]):
            os.mkdir(target_dir[0])

        def updateProgressbar(value):
            '''Function which handles updating the ProgressBar value'''
            global stop_flag

            if stop_flag[0] == True:
                self.process.terminate()
                stop_flag[0] = False
            else:
                self.progressBar.setValue(int(value))

        def endProcess():
            '''Function handles what to display once the operation is finished either normally or abnormally depending on stop_flag'''
            if stop_flag[0] == False:
                showDialog("Files were processed", "ok", "info")
            else:
                showDialog(
                    "The operation has been aborted by user", "ok", "info")

            self.progressBar.reset()
            self.btn_reset_stop.setText('RESET')
            SwitchSelection.switch(self)

            user_choice = showDialog(
                "Do you want to open target directory?", "okcancel", "info")
            if user_choice == QtWidgets.QMessageBox.StandardButton.Ok:
                webbrowser.open(f'{target_dir[0]}')
            else:
                showDialog(
                    f"Images have been saved in {target_dir[0]}", "ok", "info")

        img_quality[0] = self.compress_slider.value()
        self.process = RunApplyEdits()
        self.process.start()
        self.process.update_progress.connect(updateProgressbar)
        self.process.finished.connect(endProcess)


class RunApplyEdits(QtCore.QThread):
    update_progress = QtCore.pyqtSignal(float)
    '''Worker thread class to run worker thread operation'''

    def run(self):
        '''Function(Worker thread) handles applying edits to images in background and returning operation progress using emit() at the end of the code'''
        def applyFilters(image):
            '''Function handles applying selected filters to selected images'''
            for sfilter in filters:
                image = image.filter(sfilter)
            return image

        def applyEnhancements(image):
            '''Function handles applying selected enhancements to selected images'''
            for enhancement, value in enhancements.items():
                image = enhancement(image)
                image = image.enhance(value)
            return image

        def applySize(image):
            '''Function handles applying selected size to selected images'''
            resolution = (size[0], size[1])
            if size[2] == 'thumbnail':
                image.thumbnail(resolution, Image.ANTIALIAS)
            else:
                image = image.resize(resolution)
            return image

        def saveImages(image, image_text, exif_data):
            '''Function handles saving edited images'''

            try:
                if not len(file_format) == 1:
                    image_name = image_text.split('.')[:-1]
                    image_ext = image_text.split('.')[-1]
                    if compress_flag[0] == True:
                        image.save(
                            f'{target_dir[0]}/{image_name[0]}.{image_ext}', optimize=True, quality=img_quality[0], exif=exif_data)
                    else:
                        image.save(
                            f'{target_dir[0]}/{image_name[0]}.{image_ext}', exif=exif_data)
                else:
                    image_name = image_text.split('.')[:-1]
                    if compress_flag[0] == True:
                        image.save(
                            f'{target_dir[0]}/{image_name[0]}.{file_format[0]}', optimize=True, quality=img_quality[0], exif=exif_data)
                    else:
                        image.save(
                            f'{target_dir[0]}/{image_name[0]}.{file_format[0]}', exif=exif_data)
            except:
                generateLog(flag=False)

        os.chdir(src_dir[0])
        updation_value = 100 / len(selected_images)
        count = 1
        start_time[0] = datetime.now().strftime('%H:%M:%S')
        start_time_count[0] = time.time()
        for image in selected_images:
            value = count * updation_value
            image_text = image
            with Image.open(image) as image:
                exif_data = image.getexif()
                if not len(filters) == 0:
                    image = applyFilters(image)
                if not len(enhancements) == 0:
                    image = applyEnhancements(image)
                if not size[2] == None:
                    image = applySize(image)
                saveImages(image, image_text, exif_data)

            count += 1
            self.update_progress.emit(value)
        generateLog(flag=True)
