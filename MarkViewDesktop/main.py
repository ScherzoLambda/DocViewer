import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown
from ui_docV import Ui_MainWindow
from pathlib import Path

class MarkdownEditor(QMainWindow):
    file_path = ""
    def __init__(self):
        global file_path
        super().__init__()
        file_path = Path('mark_css.html')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
    # ================================== Inicializa UI Main
    def initUI(self):
        self.ui.statusBarMessage("[ ============================================= Powered by SherzoLambda =============================================]")
        self.previewArea = QWebEngineView()
        self.previewArea.setStyleSheet("border-radius:12px;")
        self.ui.splitter.addWidget(self.previewArea)
        self.ui.splitter.setStyleSheet("QSplitter::handle {background-color:#dfe2e5 ; border: 8px ridge  qlineargradient(spread:pad, x1:0.982591, y1:0.035, x2:0.273, y2:0.238636, stop:0.119318 rgba(199, 207, 255, 255), stop:1 rgba(139, 98, 155, 255)); }")
        self.ui.editArea.setFocus()
        style_preview = """
                QWebEngineView {
                    border-radius: 10px; /* Raio de borda para arredondar */
                }
                """

        self.previewArea.setStyleSheet(style_preview)
        # ======================================= Barra de Menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        # ============ Abrir
        openFile = QAction('Open', self)
        openFile.triggered.connect(self.showDialog)
        fileMenu.addAction(openFile)

        # ============ Salvar
        saveFile = QAction('Save', self)
        saveFile.triggered.connect(self.saveDialog)
        fileMenu.addAction(saveFile)

        # ============ Fechar
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # ============ Atualizar a visualização ao vivo durante a edição
        self.ui.editArea.textChanged.connect(self.updatePreview)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('DocViewer Palace')

        # Inicializar a visualização
        self.updatePreview()

        self.ui.editArea.setAcceptRichText(False)  # Desabilita a formatação rica de texto
        self.ui.editArea.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.ui.editArea and event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Return:
            self.inteliComplete()
        return super().eventFilter(obj, event)

    def inteliComplete(self):
        cursor = self.ui.editArea.textCursor()
        cursor.movePosition(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.MoveAnchor)  # Move o cursor para o início do documento
        if cursor.position() == 0:  # Verifica se o cursor está no início do documento
            print("Auto completar: Início do documento")
            previous_line = cursor.block().text().strip()  # Obtém o texto da linha anterior
            print("Cursor position:", cursor.position())
            print("Previous line:", previous_line)
            return
        else:
            cursor.movePosition(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.MoveAnchor)
            #cursor.movePosition(QtGui.QTextCursor.PreviousBlock, QtGui.QTextCursor.MoveAnchor)
            previous_line = cursor.block().text().strip()  # Obtém o texto da linha anterior
            print("Cursor position:", cursor.position())
            print("Previous line:", previous_line)
            if previous_line.startswith("#"):
                cursor.insertText("#")
            elif previous_line.startswith("-"):
                cursor.insertText("-")
            elif previous_line.startswith(">"):
                cursor.insertText(">")
            elif previous_line.startswith("_"):
                cursor.insertText("_")
            elif previous_line.startswith("*"):
                cursor.insertText("*")
            elif previous_line.startswith("1."):
                cursor.insertText("1.")
            elif previous_line.startswith("- [ ]"):
                cursor.insertText("- [ ]")
                print("Auto completar: Nenhuma ação necessária")
            return  # Retorna sem fazer nada
        if cursor.positionInBlock() == 0:  # Verifica se o cursor está no início de uma linha
            print("Auto completar: Início da linha")
            cursor.movePosition(QtGui.QTextCursor.PreviousBlock, QtGui.QTextCursor.MoveAnchor)
            previous_line = cursor.block().text().strip()  # Obtém o texto da linha anterior
            print("Cursor position:", cursor.position())
            print("Previous line:", previous_line)
            if previous_line.startswith("#"):
                print("Auto completar: Cabeçalho detectado")
            else:
                print("Auto completar: Nenhuma ação necessária")
            return  # Retorna sem fazer nada

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '')

        if fname[0]:
            with open(fname[0], 'r') as file:
                self.textEdit.setPlainText(file.read())

    def saveDialog(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', '')

        if fname[0]:
            with open(fname[0], 'w') as file:
                file.write(self.textEdit.toPlainText())

    def updatePreview(self):
        markdown_text = self.ui.editArea.toPlainText()
        html_text = markdown.markdown(markdown_text, extensions=['extra', 'tables'])
        #print(html_text)
        html_text = html_text.replace('[ ]', '<input type="checkbox" disabled>')
        html_text = html_text.replace('[x]', '<input type="checkbox" disabled checked>')
        html_content = file_path.read_text(encoding='utf-8')
        complete_html = html_content.format(html_text=html_text)
        print(complete_html)
        self.previewArea.setHtml(complete_html)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MarkdownEditor()
    ex.show()
    sys.exit(app.exec_())
