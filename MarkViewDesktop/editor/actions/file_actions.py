from PySide6.QtWidgets import (
    QFileDialog, QMessageBox, QInputDialog, QTextEdit, QWidget, QVBoxLayout
    )
import os

class FileActionsMixin:

    def new_file(self):
        new_tab = QWidget()
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        self.actual_text_edit = text_edit
        text_edit.setStyleSheet("background-color: #DCDCDC; color:black")
        text_edit.setTabStopDistance(32)
        layout.addWidget(text_edit)
        layout.setContentsMargins(4, 4, 4, 4)
        new_tab.setLayout(layout)

        new_file_name = self.generate_new_file_name()
        tab_index = self.ui.tab_widget.addTab(new_tab, new_file_name)
        self.ui.tab_widget.setCurrentIndex(tab_index)
        text_edit.setFocus()

        self.ui.open_files[new_tab] = [new_file_name, False, True]
        #self.checkIfAnyItemHidden()

    def generate_new_file_name(self):
        self.ui.new_file_count += 1
        base_name = "Novo Arquivo"
        file_name = f"{base_name} ({self.ui.new_file_count})"
        existing_tabs = [self.ui.tab_widget.tabText(i) for i in range(self.ui.tab_widget.count())]
        while file_name in existing_tabs:
            self.ui.new_file_count += 1
            file_name = f"{base_name} ({self.ui.new_file_count})"
        return file_name

    def saveFile(self):
        # lógica como no original
        pass

    def showDialogAndOpenFile(self):
        # lógica como no original
        pass

    def open_file(self, file_, file_name, file_path=None):
        # lógica como no original
        pass

    def close_tab(self, index):
        # lógica como no original
        pass

    def renameTab(self, tab_index, tab_widget):
        # lógica como no original
        pass

    def check_unsaved_changes(self, tab_index):
        # lógica como no original
        pass
