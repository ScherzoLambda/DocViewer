import sys
from PySide6.QtWidgets import QApplication
from editor.editor_core import MarkdownEditor

def main():

    app = QApplication(sys.argv)
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
