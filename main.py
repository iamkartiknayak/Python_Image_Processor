from PyQt6 import QtWidgets
from sys import argv

from gui import Ui_MainWindow
from fetch_files import FetchFiles, selected_images, target_dir
from fetch_profile import FetchUsername, default_target_dir
from fetch_edits import FetchEdits, filters, enhancements
from apply_edits import ApplyEdits
from switch_selection import SwitchSelection
from fetch_reset_stop_status import ResetStopSelection
from show_dialog import showDialog

quality_prev_value = [0]


class ImageProcessor(Ui_MainWindow):
    '''Class inherited from GUI.py to load MainWindow and access GUI elements such as Buttons, LineEdits etc. 
       The methods called inside the constructor is responsible for recording all the user interactions such as 
       clicking on a button or checking the checkbox etc'''

    def __init__(self, window):
        self.setupUi(window)
        self.selectDefaultTargetDirectory()

        self.btn_img_toggle.clicked.connect(self.toggleSourceSelection)
        self.btn_dir_toggle.clicked.connect(self.toggleSourceSelection)

        self.btn_browse_src.clicked.connect(self.checkSourceButtonStatus)
        self.btn_browse_target.clicked.connect(
            lambda: FetchFiles.selectTargetDirectoryPath(self))

        self.check_blur.clicked.connect(lambda: FetchEdits.getFilters(self))
        self.check_contour.clicked.connect(lambda: FetchEdits.getFilters(self))
        self.check_detail.clicked.connect(lambda: FetchEdits.getFilters(self))
        self.check_edge_enhance.clicked.connect(
            lambda: FetchEdits.getFilters(self))
        self.check_edge_enhance_more.clicked.connect(
            lambda: FetchEdits.getFilters(self))
        self.check_emboss.clicked.connect(lambda: FetchEdits.getFilters(self))
        self.check_find_edges.clicked.connect(
            lambda: FetchEdits.getFilters(self))
        self.check_sharpen.clicked.connect(lambda: FetchEdits.getFilters(self))
        self.check_smooth.clicked.connect(lambda: FetchEdits.getFilters(self))
        self.check_smooth_more.clicked.connect(
            lambda: FetchEdits.getFilters(self))

        self.input_color.textChanged.connect(
            lambda: FetchEdits.getEnhancements(self))
        self.input_contrast.textChanged.connect(
            lambda: FetchEdits.getEnhancements(self))
        self.input_sharpness.textChanged.connect(
            lambda: FetchEdits.getEnhancements(self))
        self.input_brightness.textChanged.connect(
            lambda: FetchEdits.getEnhancements(self))

        self.radio_thumbnail.clicked.connect(lambda: FetchEdits.getSize(self))
        self.radio_custom_size.clicked.connect(
            lambda: FetchEdits.getSize(self))
        self.radio_default_size.clicked.connect(
            lambda: FetchEdits.getSize(self))
        self.input_height.textChanged.connect(lambda: FetchEdits.getSize(self))
        self.input_width.textChanged.connect(lambda: FetchEdits.getSize(self))

        self.radio_jpg.clicked.connect(lambda: FetchEdits.getFormat(self))
        self.radio_jpeg.clicked.connect(lambda: FetchEdits.getFormat(self))
        self.radio_png.clicked.connect(lambda: FetchEdits.getFormat(self))
        self.radio_jfif.clicked.connect(lambda: FetchEdits.getFormat(self))
        self.radio_default_format.clicked.connect(
            lambda: FetchEdits.getFormat(self))

        self.check_compress.clicked.connect(
            lambda: FetchEdits.compressImage(self))
        self.compress_slider.valueChanged.connect(self.updateImageQualityValue)

        self.btn_apply_edits.clicked.connect(self.applyEdits)

        self.btn_reset_stop.clicked.connect(
            lambda: ResetStopSelection.resetStopToggleAutoSelection(self))

    def toggleSourceSelection(self):
        '''Function handles enabling and disabling source image selection toggle'''
        if self.btn_img_toggle.isEnabled():
            self.btn_img_toggle.setEnabled(False)
            self.btn_dir_toggle.setEnabled(True)
        else:
            self.btn_img_toggle.setEnabled(True)
            self.btn_dir_toggle.setEnabled(False)

    def checkSourceButtonStatus(self):
        '''Function initiates whether to open select file dialog box or select folder dialog box'''
        if self.btn_dir_toggle.isEnabled() == False:
            FetchFiles.select_src(self, flag="dir")

        else:
            FetchFiles.select_src(self, flag="files")

    def selectDefaultTargetDirectory(self):
        '''Function handles fetching username from fetch_profile.py and creating a folder 
           named IPEdits in user folder as default target directory'''
        FetchUsername.getDefaultTargetDirectoryPath(self)
        target_dir.extend(default_target_dir)

    def updateImageQualityValue(self):
        '''Function handles altering value in textbox displaying image quality in realtime as the 
           quality slider alters it"s value'''
        if self.compress_slider.value() % 10 == 0:
            quality_prev_value[0] = self.compress_slider.value()
            self.compress_quality.setText(str(self.compress_slider.value()))
        else:
            self.compress_slider.setValue(quality_prev_value[0])

    def applyEdits(self):
        '''Function initiates the process of applying edits to selected images and save'''
        if len(selected_images) == 0:
            showDialog("Select some images first", "ok", "warning")

        elif self.check_compress.isChecked() and self.compress_slider.value() <= 0:
            showDialog("Select Image Quality!", "ok", "info")
            self.compress_slider.setFocus()

        elif (len(filters) + len(enhancements) == 0) and (self.radio_default_size.isChecked() and self.radio_default_format.isChecked()) and not self.check_compress.isChecked():
            showDialog("Select some edits first", "ok", "warning")

        elif (self.radio_thumbnail.isChecked() or self.radio_custom_size.isChecked()) and (self.input_height.text() == "" or self.input_width.text() == ""):
            showDialog("Enter dimensions for image", "ok", "info")
            self.tabWidget.setCurrentIndex(2)
            self.input_height.setFocus()

        else:
            self.btn_reset_stop.setText("STOP")
            SwitchSelection.switch(self)
            ApplyEdits.applyEditsAndSaveImage(self)


app = QtWidgets.QApplication(argv)
MainWindow = QtWidgets.QMainWindow()
ui = ImageProcessor(MainWindow)
MainWindow.show()
app.exec()
