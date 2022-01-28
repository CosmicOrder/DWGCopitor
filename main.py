import shutil
import os
import sys
from typing import List

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog

import design
import re


# 745000_187 731864_111 781951_444

# 741138_090   741138_174   741164_006   741244_013   741334_004   745212_044   745212_073  745212_179   745222_305 745232_016   745232_037   745232_037-01

# 745322_110   745322_203   745322_316   745322_440   745352_014   745352_179   745422_043   745482_004   745482_004-01
# 745512_002   745512_002-01   745512_078   745512_078-01   745512_082   745512_083   745512_085   745512_085-01
# 745512_130   745512_194   745512_194-01   745512_307   745512_308   745512_590   745512_597   745522_293   745532_051
# 745532_053   745532_054
class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnBrowse.clicked.connect(self.browse_folder)
        self.btnBrowse_2.clicked.connect(self.target_folder)
        self.pushButton.clicked.connect(self.start_programm)
        self.pushButton_2.clicked.connect(self.input_data)
        self.pushButton_3.clicked.connect(self.clear_ListWidget)
        self.pushButton_4.clicked.connect(self.clear_statusWidget)

    def input_data(self):
        text, ok = QInputDialog.getText(self, 'Диалоговое окно', 'Введите номенклатурный номер')

        if ok:
            self.listWidget.addItem(str(text))
            self.list_of_nomenclatures = re.split(r'\s+', text)

    def browse_folder(self):
        self.FILES_PATH = QtWidgets.QFileDialog.getExistingDirectory(self)

    def target_folder(self):
        self.TARGET_PATH = QtWidgets.QFileDialog.getExistingDirectory(self)

    def start_programm(self):
        c = DWGCopitor()
        self.listWidget_2.addItem(c.copy(self.list_of_nomenclatures, os.path.abspath(self.FILES_PATH), os.path.abspath(
            self.TARGET_PATH)))
        # self.listWidget_2.addItem(', '.join(self.list_of_nomenclatures))

    def clear_ListWidget(self):
        self.listWidget.clear()

    def clear_statusWidget(self):
        self.listWidget_2.clear()


class DWGCopitor:
    def copy(self, list_of_nomenclatures: List[str], folder_to_search: str, target_folder: str):

        list_for_copy = self._find_match_dwg(list_of_nomenclatures, folder_to_search)
        return self._copy_match_dwg(list_for_copy, target_folder)

    def _find_match_dwg(self, list_of_nomenclatures: List[str], folder_to_search: str) -> List[str]:
        target_files = {}
        for root, dirs, files in os.walk(folder_to_search):
            for file in files:
                file_path = os.path.join(root, file)

                for pattern in list_of_nomenclatures:
                    if file.startswith(pattern) and file.endswith(('.dwg', '.DWG')):
                        target_files.setdefault(pattern, []).append(file_path)
                    if re.fullmatch(pattern + r'-\d+', file[:13]) and file.endswith(('.dwg', '.DWG')):
                        target_files.setdefault(file, []).append(file_path)

        return [max(i, key=os.path.getmtime) for i in
                target_files.values()] if target_files else 'Требуемых файлов в данной директории не найдено\n'

    def _copy_match_dwg(self, list_for_copy: List[str], target_folder: str):
        i = 0
        j = 0
        if list_for_copy == 'Требуемых файлов в данной директории не найдено\n':
            return list_for_copy
        else:
            for file_name in list_for_copy:
                try:
                    shutil.copy(file_name, target_folder)
                    i += 1
                except shutil.SameFileError:
                    j += 1
            if i == 1 and j == 1:
                return f'{i} файл успешно скопирован, \n{j} файл уже существует в папке назначения!\n'
            if i in [2, 3, 4] and j == [2, 3, 4]:
                return f'{i} файла успешно скопирован, \n{j} файла уже существует в папке назначения!\n'
            if i not in [1, 2, 3, 4] and j not in [1, 2, 3, 4]:
                return f'{i} файлов успешно скопировано, \n{j} файлов уже существует в папке назначения!\n'
            if i not in [1, 2, 3, 4] and j == 1:
                return f'{i} файлов успешно скопировано, \n{j} файл уже существует в папке назначения!\n'
            if i == 1 and j not in [1, 2, 3, 4]:
                return f'{i} файл успешно скопирован, \n{j} файлов уже существует в папке назначения!\n'
            if i == 1 and j in [2, 3, 4]:
                return f'{i} файл успешно скопирован, \n{j} файла уже существует в папке назначения!\n'
            if i not in [1, 2, 3, 4] and j in [2, 3, 4]:
                return f'{i} файлов успешно скопировано, \n{j} файла уже существует в папке назначения!\n'
            if i in [2, 3, 4] and j not in [1, 2, 3, 4]:
                return f'{i} файла успешно скопировано, \n{j} файлов уже существует в папке назначения!\n'
            if i in [2, 3, 4] and j in [2, 3, 4]:
                return f'{i} файла успешно скопировано, \n{j} файлов уже существует в папке назначения!\n'
            if i in [2, 3, 4] and j == 1:
                return f'{i} файла успешно скопировано, \n{j} файл уже существует в папке назначения!\n'
            else:
                return f'{i} файл успешно скопирован, \n{j} файла уже существует в папке назначения!\n'


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec()
