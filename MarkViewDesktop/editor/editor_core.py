from PySide6.QtWidgets import QMainWindow, QTextEdit
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QIcon, QTextCursor
from ui.ui_docV import Ui_MainWindow

from editor.actions.edit_actions import EditActionsMixin
from editor.actions.file_actions import FileActionsMixin

class MarkdownEditor(QMainWindow, EditActionsMixin, FileActionsMixin):
    
    def __init__(self, file_to_open=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.html_text_ = ""
        self.complete_html = ""
        self.actual_text_edit = None
        self.openSyntaxFileFlag = False
        self._mousePressPos = None

        self.init_ui()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon("doc_icon.ico"))

        self.connect_buttons()
        if file_to_open:
            self.open_file(file_to_open)
        self.setFocus()

    def connect_buttons(self):
        self.ui.close_btn.clicked.connect(lambda: self.close())
        self.ui.minimize_btn.clicked.connect(lambda: self.showMinimized())
        self.ui.maxmize_btn.clicked.connect(lambda: self.restore_or_maximize())

    def restore_or_maximize(self):
        self.showNormal() if self.isMaximized() else self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._mousePressPos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self._mousePressPos is not None:
            self.move(self.geometry().topLeft() + event.position().toPoint() - self._mousePressPos)

    def mouseReleaseEvent(self, event):
        self._mousePressPos = None
    
    def keyPressEvent(self, event):
        if event.type() == QEvent.KeyPress:
            match (event.key(), event.modifiers()):
                case (Qt.Key_N, Qt.ControlModifier): self.new_file()
                case (Qt.Key_O, Qt.ControlModifier): self.showDialogAndOpenFile()
                case (Qt.Key_S, Qt.ControlModifier): self.saveFile()
                case (Qt.Key_R, Qt.ControlModifier): self.updatePreview(self.actual_text_edit)
                case (Qt.Key_Backslash, Qt.ControlModifier): self.ui.swapWidgetOnSplitter()
                case (Qt.Key_Q, Qt.ControlModifier): self.ui.toggle_splitter_orientation()
                case (Qt.Key_H, Qt.ControlModifier): self.syntaxHelpAndHints()
                case (Qt.Key_J, Qt.ControlModifier): self.removeSyntaxAndHint()
        super().keyPressEvent(event)


    def onTabChange(self, index):
        self.ui.editArea = self.getCurrentTextEdit(index)
        if(self.ui.editArea is not None):
            self.updateAfterTabChange(self.ui.editArea)
            self.ui.editArea.installEventFilter(self)
        #print(f"Aba mudada: {index}")
    
    def updateAfterTabChange(self, textEdit):
        plain_text = textEdit.toPlainText()
        self.html_text_ = self.getMarkdownText(plain_text)
        self.updateCompleteHtml()
        self.ui.previewArea.setHtml(self.complete_html)
            
    def inteliComplete(self):
        cursor = self.ui.editArea.textCursor()
        cursor.movePosition(QTextCursor.EndOfLine)  # Move o cursor para o final da linha atual
        
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
        # Obtém o índice da aba atualmente selecionada
        #current_index = self.ui.tab_widget.currentIndex()
        
        if current_index == -1:
            # Nenhuma aba selecionada
            return None
        
        # Obtém o widget da aba selecionada
        current_tab = self.ui.tab_widget.widget(current_index)
        
        if current_tab is not None:
            # Procura pelo QTextEdit dentro do layout da aba
            layout = current_tab.layout()
            if layout is not None and layout.count() > 0:
                # Assume que o QTextEdit é o primeiro widget no layout
                text_edit = layout.itemAt(0).widget()
                if isinstance(text_edit, QTextEdit):
                    return text_edit
        
        return None   