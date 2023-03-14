from gui import Ui_MainWindow


class SwitchSelection(Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def switch(self):
        '''Function handles disabling the controls during ongoing operation and enabling the controls once the operation is finished'''
        filter_list = [self.check_blur, self.check_contour, self.check_detail, self.check_edge_enhance, self.check_edge_enhance_more,
                       self.check_emboss, self.check_find_edges, self.check_sharpen, self.check_smooth, self.check_smooth_more]

        enhancment_list = [self.input_color, self.input_contrast,
                           self.input_sharpness, self.input_brightness]

        size_list = [self.radio_custom_size,
                     self.radio_default_size, self.radio_thumbnail]

        format_list = [self.radio_jpg, self.radio_jpeg,
                       self.radio_jfif, self.radio_png, self.radio_default_format]

        if self.btn_reset_stop.text() == 'STOP':
            flag = False
        else:
            flag = True

        for sfilter in filter_list:
            sfilter.setEnabled(flag)

        for enhancement in enhancment_list:
            enhancement.setEnabled(flag)

        for size in size_list:
            size.setEnabled(flag)

        for sformat in format_list:
            sformat.setEnabled(flag)

        self.btn_browse_src.setEnabled(flag)
        self.btn_browse_target.setEnabled(flag)
        self.check_compress.setEnabled(flag)
        self.compress_slider.setEnabled(flag)
        self.btn_apply_edits.setEnabled(flag)
