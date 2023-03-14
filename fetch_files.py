import os
from PyQt6.QtWidgets import QFileDialog

from gui import Ui_MainWindow

selected_images, src_dir, target_dir, temp, img_count = [], [], [], [], []
img_extensions = ('.jpg', '.jpeg', '.jfif', '.png',
                  'JPG', 'JPEG', 'JFIF', '.PNG',)


class FetchFiles(Ui_MainWindow):
    '''Class inherited from gui.py to access GUI elements'''

    def __init__(self) -> None:
        super().__init__()

    def assignValues(self):
        try:
            self.display_src_path.setText(src_dir[0])
            self.display_img_cnt.setText(str(img_count[0]))
            self.display_selected_images.clear()
            for image in selected_images[:20]:
                self.display_selected_images.insertPlainText(image)
                if not selected_images.index(image) == len(selected_images) - 1:
                    self.display_selected_images.insertPlainText(', ')
        except:
            pass

    def updateImageList(self, content, flag):
        '''Function handles fetching images as files or selecting an entire directory of images depending on the flag'''

        if flag == 'dir':
            for files in os.listdir(content):
                if files.endswith(img_extensions):
                    temp.append(files)
        else:
            content = content[0]
            for file in content:
                fileName = file.split('/')[-1]
                temp.append(fileName)
            content = '/'.join(file.split('/')[:-1])

        if len(temp) != 0:
            src_dir.clear()
            selected_images.clear()
            img_count.clear()
            src_dir.append(content)
            selected_images.extend(temp)
            img_count.append(str(len(selected_images)))
            temp.clear()
            FetchFiles.assignValues(self)

    def select_src(self, flag):
        '''Function handles fetching and updating source image directory using check_src_btn_status method in main.py'''
        if flag == 'dir':
            content = QFileDialog.getExistingDirectory(caption="Select Folder")
            if len(content) != 0:
                FetchFiles.updateImageList(self, content, flag)

        elif flag == 'files':
            content = QFileDialog.getOpenFileNames(
                directory="./", filter="Image Files, *.jpg *.jpeg *.jfif *.png", caption="Select Images")
            if len(content[0]) != 0:
                FetchFiles.updateImageList(self, content, flag)
                src_dir.append('/'.join(content[0][0]).split('/')[:-1])

    def selectTargetDirectoryPath(self):
        '''Function handles fetching and updating target image directory using select_manual_target_dir method in main.py'''
        content = QFileDialog.getExistingDirectory()
        if content:
            target_dir.clear()
            target_dir.append(content)
            self.display_target_path.setText(content)
