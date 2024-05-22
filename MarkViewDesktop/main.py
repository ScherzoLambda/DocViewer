import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown
from ui_docV import Ui_MainWindow

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
       
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

        complete_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
                    line-height: 1.6;
                    padding: 20px;
                    color: #E6edf3;
                    background-color: #161b22;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    border-bottom: 1px solid #eaecef;
                    padding-bottom: 0.3em;
                }}
                h1 {{ font-size: 2em; }}
                h2 {{ font-size: 1.5em; }}
                h3 {{ font-size: 1.25em; }}
                blockquote {{
                    color: #848d97;
                    border-left: 0.25em solid #30363d;
                    padding: 0.5em 1em;
                }}
                code {{
                    background-color: rgba(27,31,35,0.05);
                    padding: 0.2em 0.4em;
                    margin: 0;
                    font-size: 85%;
                    border-radius: 3px;
                }}
                pre code {{
                    background-color: #30363d;
                    padding: 0;
                    font-size: 100%;
                }}
                pre {{
                    background-color: #30363d;
                    padding: 1em;
                    overflow: auto;
                }}
                table {{
                    border-collapse: collapse;
                    border-spacing: 0;
                    max-width: 100%;
                    display: block;
                    overflow: auto;
                }}
                table th, table td {{
                    border: 1px solid #dfe2e5;
                    padding: 6px 13px;
                }}
                table tr {{
                    background-color: #161b22;
                    border-top: 1px solid #c6cbd1;
                }}
                table tr:nth-child(2n) {{
                    background-color: #30363d;
                }}
                input[type="checkbox"] {{
                    width: 1em;
                    height: 1em;
                    margin-right: 0.5em;
                    vertical-align: middle;
                    position: relative;
                    top: -0.1em;
                }}
            </style>
        </head>
        <body>
            {html_text}
        </body>
        </html>
        """
        self.previewArea.setHtml(complete_html)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MarkdownEditor()
    ex.show()
    sys.exit(app.exec_())
