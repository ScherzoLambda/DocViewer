import os
import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import QApplication
from editor.editor_core import MarkdownEditor


def resource_path(relative_path: str) -> str:
    """Obtém o caminho absoluto do recurso, funciona no dev e no executável."""
    if hasattr(sys, "_MEIPASS"):
        # quando rodando no executável do PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


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
