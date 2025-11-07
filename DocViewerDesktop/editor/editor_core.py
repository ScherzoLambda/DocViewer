from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QEvent, QFileSystemWatcher
from PySide6.QtGui import QIcon, QTextCursor
from PySide6.QtWidgets import QTextEdit

from editor.actions.edit_actions import EditActionsMixin
from editor.actions.file_actions import FileActionsMixin
from ui.main_window import MainWindow
from ui.ui_docV import Ui_MainWindow


class MarkdownEditor(MainWindow, EditActionsMixin, FileActionsMixin):
    
    def __init__(self, file_to_open=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_file_path = ""  # O caminho do arquivo que você abriu

        # 1. Inicializa o File System Watcher
        self.file_watcher = QFileSystemWatcher(self)

        # 2. Adiciona o arquivo para monitorar
        self.file_watcher.addPath(self.current_file_path)

        # 3. Conecta o sinal 'fileChanged' ao seu método de tratamento
        self.file_watcher.fileChanged.connect(self.handle_file_change)
        self.html_text_ = ""
        self.complete_html = ""
        self.actual_text_edit = None
        self.openSyntaxFileFlag = False
        self._mousePressPos = None

        self.init_ui()

        self.connect_buttons()
        if file_to_open:
            self.open_initial_File(file_path_str=file_to_open)
        self.setFocus()
        self.ui.header_frame.installEventFilter(self)
        self.ui.tab_widget.installEventFilter(self)
        self.ui.splitter.installEventFilter(self)
        self.ui.previewArea2.installEventFilter(self)
        self.ui.tab_widget.installEventFilter(self)
        self.ui.editArea.installEventFilter(self)

    def connect_buttons(self):
        self.ui.close_btn.clicked.connect(lambda: self.close())
        self.ui.minimize_btn.clicked.connect(lambda: self.showMinimized())
        self.ui.maxmize_btn.clicked.connect(lambda: self.toggle_maximize_restore())

    def keyPressEvent(self, event):
        if event.type() == QEvent.KeyPress:
            match (event.key(), event.modifiers()):
                case (Qt.Key_N, Qt.ControlModifier): self.new_file()
                case (Qt.Key_O, Qt.ControlModifier): self.showDialogAndOpenFile()
                case (Qt.Key_S, Qt.ControlModifier): self.saveFile()
                case (Qt.Key_R, Qt.ControlModifier): self.updatePreview(self.actual_text_edit)
                case (Qt.Key_Backslash, Qt.ControlModifier): self.swapWidgetOnSplitter()
                case (Qt.Key_Q, Qt.ControlModifier): self.toggle_splitter_orientation()
                # case (Qt.Key_H, Qt.ControlModifier): self.syntaxHelpAndHints()
                # case (Qt.Key_J, Qt.ControlModifier): self.removeSyntaxAndHint()
        super().keyPressEvent(event)

    def updateAfterTabChange(self, textEdit):
        plain_text = textEdit.toPlainText()
        self.html_text_ = self.getMarkdownText(plain_text)
        self.updateCompleteHtml()
        self.ui.previewArea2.setHtml(self.complete_html)
            
    def inteliComplete(self):
        cursor = self.ui.editArea.textCursor()
        cursor.movePosition(QTextCursor.EndOfLine)
        
        actual_line = cursor.block().text().strip()
        previous_line = cursor.block().previous().text().strip()  # Obtém o texto da linha anterior
        #next_line = cursor.block().next().text().strip()
        #print("actual line", actual_line)
        if previous_line.startswith("-"):
            if(len(previous_line) > 2 and previous_line[2] == '['):
                cursor.insertText("- [ ] ")
            else:
                if(actual_line.startswith("-")):
                    cursor.movePosition(QtGui.QTextCursor.EndOfLine)
                else:
                    cursor.insertText("- ")
        elif previous_line.startswith(">"):
            cursor.insertText("> ")
        elif previous_line.startswith("_"):
            cursor.insertText("_ ")
        elif previous_line.startswith("*"):
            cursor.insertText("* ")
        elif previous_line.startswith("1."):
            cursor.insertText("1. ")
        elif previous_line.startswith("- "):
            cursor.insertText("- [ ] ")
        
        ##cursor.movePosition(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.MoveAnchor)
        self.ui.editArea.setTextCursor(cursor) 

    def getCurrentTextEdit(self, current_index):
        """Recupera o QTextEdit da aba atualmente selecionada"""
        if current_index == -1:
            return None
        # Obtém o widget da aba selecionada
        current_tab = self.ui.tab_widget.widget(current_index)
        
        if current_tab is not None:
            layout = current_tab.layout()
            if layout is not None and layout.count() > 0:
                text_edit = layout.itemAt(0).widget()
                if isinstance(text_edit, QTextEdit):
                    return text_edit
        
        return None

        # ================ Dinamicidade UI

    def swapWidgetOnSplitter(self):
        # Obtém os índices atuais dos widgets no splitter
        index_tabWidget = self.ui.splitter.indexOf(self.ui.tab_widget)
        index_preview_area = self.ui.splitter.indexOf(self.ui.previewArea2)
        # print(index_tabWidget, "wid_1", sep="|")
        # print(index_preview_area, "wid_2", sep="|")
        if index_tabWidget < index_preview_area:
            # Remove os widgets temporariamente
            self.ui.splitter.widget(index_tabWidget).setParent(None)
            self.ui.splitter.widget(index_preview_area - 1).setParent(None)
            # Adiciona os widgets de volta em ordem trocada
            self.ui.splitter.insertWidget(index_tabWidget, self.ui.previewArea2)
            self.ui.splitter.insertWidget(index_preview_area, self.ui.tab_widget)
        else:
            self.ui.splitter.widget(index_tabWidget - 1).setParent(None)
            self.ui.splitter.widget(index_preview_area).setParent(None)
            # Adiciona os widgets de volta em ordem trocada
            self.ui.splitter.insertWidget(index_tabWidget, self.ui.previewArea2)
            self.ui.splitter.insertWidget(index_preview_area, self.ui.tab_widget)

    def toggle_splitter_orientation(self):
        # Alterna a orientação do splitter entre horizontal e vertical
        if self.ui.splitter.orientation() == QtCore.Qt.Horizontal:
            self.ui.splitter.setOrientation(QtCore.Qt.Vertical)
        else:
            self.ui.splitter.setOrientation(QtCore.Qt.Horizontal)
            # self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    # def scroll_to_bottom(self, ok):
    #     """
    #     Executa JavaScript para scrollar a página para o final.
    #
    #     Args:
    #         ok (bool): True se o carregamento foi bem-sucedido, False caso contrário.
    #     """
    #     if ok:
    #         javascript_code = "window.scrollTo(0, document.body.scrollHeight);"
    #         self.previewArea.page().runJavaScript(javascript_code)
    #     else:
    #         print("Erro ao carregar a página.")
