from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QEvent, QFileSystemWatcher
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QTextEdit
from notifypy import Notify

from editor.actions.edit_actions import EditActionsMixin
from editor.actions.file_actions import FileActionsMixin
from ui.main_window import MainWindow
from ui.ui_docV import Ui_MainWindow


class MarkdownEditor(MainWindow, EditActionsMixin, FileActionsMixin):
    
    def __init__(self, file_to_open=None):
        super().__init__()
        self.tray_icon = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.file_watcher = QFileSystemWatcher(self)
        # self.file_watcher.addPath(self.current_file_path)
        self._file_change_timers = {}
        self.file_watcher.fileChanged.connect(self._on_file_changed)


        self.html_text_ = ""
        self.complete_html = ""
        self.actual_text_edit = QTextEdit()
        self.openSyntaxFileFlag = False
        self._mousePressPos = None

        self.init_ui()
        # self.init_tray_icon()

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

    def _on_file_changed(self, path):
        """Internal slot connected to QFileSystemWatcher.fileChanged.
        Coalesces rapid multiple events for the same path using a single-shot QTimer.
        After the timer times out, the real handler `handle_file_change` is invoked once.
        """
        try:
            # If a timer already exists for this path, restart it (coalesce events)
            timer = self._file_change_timers.get(path)
            if timer is None:
                timer = QtCore.QTimer(self)
                timer.setSingleShot(True)
                # Capture `path` default argument to avoid late-binding in lambda
                timer.timeout.connect(lambda p=path: self._on_file_change_timeout(p))
                self._file_change_timers[path] = timer
            else:
                timer.stop()
            # Start or restart the timer (300ms debounce)
            timer.setInterval(300)
            timer.start()
        except Exception as e:
            print(f"Erro ao agendar debounce de fileChanged: {e}")

    def _on_file_change_timeout(self, path):
        """Called after debounce timeout for a given path; invokes the public handler."""
        # Remove timer reference
        timer = self._file_change_timers.pop(path, None)
        if timer:
            timer.stop()
            timer.deleteLater()
        try:
            self.handle_file_change2(path)
        except Exception as e:
            print(f"Erro ao tratar mudança de arquivo ({path}): {e}")

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

    # def init_tray_icon(self):
    #     """Inicializa o ícone da bandeja do sistema."""
    #
    #     # 1. Cria a instância do QSystemTrayIcon
    #     # Você deve fornecer um ícone real para a sua aplicação aqui.
    #     # Exemplo: QIcon('caminho/para/seu/icone.png')
    #     app_icon = QIcon('/home/ernesto-dev/Documentos/labs/python_lab/DocViewer/DocViewerDesktop/resources/icons_svg/doc_icon.ico')
    #     self.tray_icon = QSystemTrayIcon(app_icon, self)
    #
    #     self.tray_icon.messageClicked.connect(self.load_file_content)
    #
    #     # 3. Torna o ícone visível para habilitar as notificações
    #     self.tray_icon.show()

    # def handle_file_change(self):
    #     """
    #     Lança uma notificação nativa do SO em vez de um diálogo modal.
    #     """
    #     self.load_file_content()
    #     # if not hasattr(self, 'tray_icon'):
    #     # Você pode usar um ícone embutido do Qt ou um arquivo PNG/ICO
    #
    #     title = 'Arquivo Modificado'
    #     message = 'O arquivo foi modificado no disco por um programa externo. Clique aqui para recarregar (perdendo as alterações não salvas).'
    #     # 3. Lançar a notificação
    #     self.tray_icon.showMessage(
    #         title,
    #         message,
    #         QSystemTrayIcon.Information,  # Ou QSystemTrayIcon.Warning, QSystemTrayIcon.Critical
    #         5000  # Tempo de exibição em ms (5 segundos)
    #     )


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


    def handle_file_change2(self, path):
        """
        Lança uma notificação usando o serviço D-Bus 'org.freedesktop.Notifications'.
        """
        title = 'DocViewer - Arquivo Modificado'
        message = (
            f"O arquivo {path} foi modificado no disco por um programa externo. "
            "Alterações carregadas automaticamente."
        )

        # 1. Cria a instância de notificação
        notifier = Notify()

        # 2. Configura a notificação
        notifier.application_name = "Markdown Editor"
        notifier.icon = "/home/ernesto-dev/Documentos/labs/python_lab/DocViewer/DocViewerDesktop/resources/icons_svg/not_icon.png"  # Caminho para o ícone do app
        notifier.audio = "/home/ernesto-dev/Músicas/doc-notify-sound2.wav"
        notifier.title = title
        notifier.message = message

        # 3. Envia a notificação
        notifier.send(block=False)