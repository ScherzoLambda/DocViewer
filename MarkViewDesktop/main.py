import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import QApplication
from editor.editor_core import MarkdownEditor

def main():

    app = QApplication(sys.argv)
    sytyle_sheet_file = QFile("./ui/dark-high-v0.qss")
    if sytyle_sheet_file.open(QIODevice.ReadOnly):
       styleSheet = str(sytyle_sheet_file.readAll(), encoding='utf-8')  # Leitura e conversão para string
       app.setStyleSheet(styleSheet)
       sytyle_sheet_file.close()
    else:
        print("Falha ao abrir o arquivo de stylesheet.")
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
