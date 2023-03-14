from PIL import ImageFilter, ImageEnhance

from gui import Ui_MainWindow
from fetch_files import selected_images

filters = set()
enhancements = {}
size = [None, None, None]
file_format = []
compress_flag = [False]


class FetchEdits(Ui_MainWindow):
    '''Class inherited from gui.py to access GUI elements'''

    def __init__(self):
        super().__init__()

    def getFilters(self):
        '''Function handles fetching selected filters from getFilters method in main.py'''
        filters_obj_dict = {ImageFilter.BLUR: self.check_blur, ImageFilter.CONTOUR: self.check_contour, ImageFilter.DETAIL: self.check_detail, ImageFilter.EDGE_ENHANCE: self.check_edge_enhance, ImageFilter.EDGE_ENHANCE_MORE: self.check_edge_enhance_more,
                            ImageFilter.EMBOSS: self.check_emboss, ImageFilter.FIND_EDGES: self.check_find_edges, ImageFilter.SHARPEN: self.check_sharpen, ImageFilter.SMOOTH: self.check_smooth, ImageFilter.SMOOTH_MORE: self.check_smooth_more}
        for filter_property, value in filters_obj_dict.items():
            if value.isChecked():
                filters.add(filter_property)
            else:
                filters.discard(filter_property)

    def getEnhancements(self):
        '''Function handles fetching selected enhancements from getEnhancements method in main.py'''
        enhancement_obj_dict = {ImageEnhance.Color: self.input_color, ImageEnhance.Contrast: self.input_contrast,
                                ImageEnhance.Sharpness: self.input_sharpness, ImageEnhance.Brightness: self.input_brightness}

        for enh_property, value in enhancement_obj_dict.items():
            if value.text() != '':
                try:
                    if 0 <= float(value.text()) <= 8:
                        enhancements[enh_property] = float(
                            value.text())
                    else:
                        value.setText(value.text()[:-1])
                except:
                    value.setText(value.text()[:-1])
            else:
                try:
                    del enhancements[enh_property]
                except:
                    pass

    def getSize(self):
        '''Function handles fetching selected size from getSize method in main.py'''
        if self.radio_thumbnail.isChecked() or self.radio_custom_size.isChecked():
            self.input_height.setEnabled(True)
            self.input_width.setEnabled(True)
        else:
            self.input_height.setEnabled(False)
            self.input_width.setEnabled(False)

        if self.radio_custom_size.isChecked() == True:
            size[2] = 'custom'
        elif self.radio_thumbnail.isChecked() == True:
            size[2] = 'thumbnail'
        else:
            size[2] = None

        if self.input_height.text() == '' or not self.input_height.text().isnumeric():
            self.input_height.setText(self.input_height.text()[:-1])
            if self.input_height.text() == '':
                size[0] = None
        else:
            size[0] = int(self.input_height.text())

        if self.input_width.text() == '' or not self.input_width.text().isnumeric():
            self.input_width.setText(self.input_width.text()[:-1])
            if self.input_width.text() == '':
                size[1] = None
        else:
            size[1] = int(self.input_width.text())

    def getFormat(self):
        '''Function handles fetching selected file format from getFormat method in main.py'''

        file_format.clear()
        if self.radio_jfif.isChecked() == True:
            extension_flag = 'jfif'
        elif self.radio_jpeg.isChecked() == True:
            extension_flag = 'jpeg'
        elif self.radio_jpg.isChecked() == True:
            extension_flag = 'jpg'
        elif self.radio_png.isChecked() == True:
            extension_flag = 'png'
        elif self.radio_default_format.isChecked() == True:
            if not len(selected_images) == 0:
                for image in selected_images:
                    file_format.append(str(image).split('.')[-1])
        try:
            if extension_flag != 'Default':
                file_format.append(extension_flag)
        except:
            pass

    def compressImage(self):
        '''Function handles setting compress_flag accordingly to the condition which will be fetched at the beginning of the operation'''
        if self.check_compress.isChecked():
            compress_flag[0] = True
            self.compress_slider.setEnabled(True)
            self.compress_quality.setEnabled(True)
        else:
            compress_flag[0] = False
            self.compress_slider.setEnabled(False)
            self.compress_quality.setEnabled(False)
