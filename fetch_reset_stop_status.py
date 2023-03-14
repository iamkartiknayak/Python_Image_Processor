from PyQt6 import QtWidgets

from gui import Ui_MainWindow
from show_dialog import showDialog
from fetch_edits import filters, enhancements, size, file_format, compress_flag
from fetch_files import src_dir, target_dir, selected_images, img_count
from apply_edits import stop_flag
from fetch_profile import default_target_dir


class ResetStopSelection(Ui_MainWindow):

    def __init__(self):
        super().__init__()

    def resetStopToggleAutoSelection(self):
        '''Function handles whether to stop the ongoing operation or to reset selected edits and values'''
        if self.btn_reset_stop.text() == 'RESET':
            user_choice = showDialog(
                "Do you want to reset selection?", "okcancel", "question")

            if user_choice == QtWidgets.QMessageBox.StandardButton.Ok:
                checkBoxList = [self.check_blur, self.check_contour, self.check_detail, self.check_edge_enhance, self.check_edge_enhance_more,
                                self.check_emboss, self.check_find_edges, self.check_sharpen, self.check_smooth, self.check_smooth_more, self.check_compress]

                inputBoxList = [self.input_color, self.input_contrast, self.input_sharpness, self.input_brightness,
                                self.input_height, self.input_width, self.display_src_path, self.display_selected_images]

                # Clearing UI data
                for item in checkBoxList:
                    item.setChecked(False)

                for item in inputBoxList:
                    item.clear()

                self.radio_default_format.setChecked(True)
                self.radio_default_size.setChecked(True)
                self.compress_slider.setEnabled(False)
                self.compress_quality.setEnabled(False)
                self.input_height.setEnabled(False)
                self.input_width.setEnabled(False)
                self.display_img_cnt.clear()
                self.display_target_path.setText(default_target_dir[0])
                self.tabWidget.setCurrentIndex(0)

                # Clearing actual data
                filters.clear()
                enhancements.clear()
                size[0] = size[1] = size[2] = None
                file_format.clear()
                compress_flag[0] = False
                self.compress_slider.setValue(0)

                src_dir.clear()
                target_dir[0] = default_target_dir[0]
                selected_images.clear()
                img_count.clear()

        else:
            global stop_flag
            if self.btn_reset_stop.text() == 'STOP':
                stop_flag[0] = True
