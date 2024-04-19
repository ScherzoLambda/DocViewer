import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QAction, QFileDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.previewArea = QWebEngineView()

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.previewArea)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Barra de Menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        # Abrir
        openFile = QAction('Open', self)
        openFile.triggered.connect(self.showDialog)
        fileMenu.addAction(openFile)

        # Salvar
        saveFile = QAction('Save', self)
        saveFile.triggered.connect(self.saveDialog)
        fileMenu.addAction(saveFile)

        # Fechar
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Atualizar a visualização ao vivo durante a edição
        self.textEdit.textChanged.connect(self.updatePreview)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Markdown Editor')

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            with open(fname[0], 'r') as file:
                self.textEdit.setPlainText(file.read())

    def saveDialog(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', '/home')

        if fname[0]:
            with open(fname[0], 'w') as file:
                file.write(self.textEdit.toPlainText())

    def updatePreview(self):
        markdown_text = self.textEdit.toPlainText()
        html_text = markdown.markdown(markdown_text)
        self.previewArea.setHtml(html_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MarkdownEditor()
    ex.show()
    sys.exit(app.exec_())
