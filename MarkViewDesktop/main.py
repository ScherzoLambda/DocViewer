import os
import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import QApplication
from editor.editor_core import MarkdownEditor
from ui.ui_docV import resource_path

def main():
    app = QApplication(sys.argv)
    style_file = resource_path("ui/dark-high-v0.qss")
    style_sheet_file = QFile(style_file)
    print(style_sheet_file)
    if style_sheet_file.open(QIODevice.ReadOnly):
        styleSheet = str(style_sheet_file.readAll(), encoding="utf-8")
        app.setStyleSheet(styleSheet)
        style_sheet_file.close()
    else:
        print(f"Falha ao abrir o arquivo de stylesheet: {style_file}")

    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
## TODO: ajustar icones
## TODO: ajustar temas dark-high para ficar dinamico
## TODO: ajustar tema padrão dark-night
