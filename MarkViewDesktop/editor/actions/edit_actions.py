from PySide6.QtWidgets import QMessageBox, QMenu, QInputDialog, QTextEdit, QWidget, QVBoxLayout
from PySide6.QtCore import Qt 
from PySide6.QtGui import QAction
from PySide6 import QtGui
import markdown

class EditActionsMixin:

    def init_ui(self):
        self.ui.menu = self.create_file_menu()
        # self.ui.splitter.setStyleSheet("QSplitter::handle {background-color:#dfe2e5; height: 30px;}")
        self.ui.editArea.setFocus()
        # self.ui.previewArea.setZoomFactor(0.8)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('DocViewer')
        self.ui.file_btn.clicked.connect(self.show_menu)
        self.ui.tab_widget.tabCloseRequested.connect(self.close_tab)
        # self.ui.tab_widget.currentChanged.connect(self.onTabChange)
        self.ui.tab_widget.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tab_widget.tabBar().customContextMenuRequested.connect(self.onTabRightClick)
        self.new_file()

    def create_file_menu(self):
        menu = QMenu()
        new_file_act = QAction("Novo arquivo", self)
        new_file_act.setShortcut("Ctrl+N")
        new_file_act.triggered.connect(self.new_file)
        menu.addAction(new_file_act)

        open_file_act = QAction("Abrir Arquivo", self)
        open_file_act.setShortcut("Ctrl+O")
        open_file_act.triggered.connect(self.showDialogAndOpenFile)
        menu.addAction(open_file_act)

        save_file_act = QAction("Salvar Arquivo", self)
        save_file_act.setShortcut("Ctrl+S")
        save_file_act.triggered.connect(self.saveFile)
        menu.addAction(save_file_act)

        # menu.setFixedWidth(180)
        return menu

    def show_menu(self):
        if not self.ui.has_open_menu:
            self.ui.menu.exec(self.ui.file_btn.mapToGlobal(self.ui.file_btn.rect().bottomLeft()))
            self.ui.has_open_menu = True
        else:
            self.ui.menu.close()
            self.ui.has_open_menu = False

    def onTabRightClick(self, position):
        """Exibe um diálogo para renomear arquivo ao clicar com o botão direito em cima da aba"""
        tab_index = self.ui.tab_widget.tabBar().tabAt(position)
        tab_widget = self.ui.tab_widget.widget(tab_index)
        if tab_index != -1:
                    # Cria o menu de contexto
            menu = QMenu(self)

            rename_action = QAction("Renomear arquivo", self)
            rename_action.triggered.connect(lambda: self.renameTab(tab_index, tab_widget))

            open_action = QAction("Abrir aqui", self)
            open_action.triggered.connect(lambda: self.open_here(tab_index))

            save_action = QAction("Salvar arquivo", self)
            save_action.triggered.connect(lambda: self.saveFile())

            # Adiciona as ações ao menu
            menu.addAction(rename_action)
            menu.addAction(open_action)
            menu.addAction(save_action)
            #menu.addSeparator()  # Adiciona um separador visual
            

            # Exibe o menu de contexto na posição do cursor
            menu.exec_(self.ui.tab_widget.tabBar().mapToGlobal(position))
    # ... incluir updatePreview, inteliComplete, updateCompleteHtml, getMarkdownText, scroll_to_bottom etc
    def eventFilter(self, obj, event):
        if obj == self.actual_text_edit and event.type() == QtCore.QEvent.KeyRelease and event.key() == QtCore.Qt.Key_Return:
            self.inteliComplete()
        return super().eventFilter(obj, event)
    
    def inteliComplete(self):
        cursor = self.actual_text_edit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.EndOfLine)  # Move o cursor para o final da linha atual
        
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
        self.actual_text_edit.setTextCursor(cursor)
    
    def getMarkdownText(self, input_text):
        mkd_text = markdown.markdown(input_text, extensions=['extra', 'tables','fenced_code', 'codehilite'])
        mkd_text = mkd_text.replace('[ ]', '<input type="checkbox" disabled>')       # Necessário!
        mkd_text = mkd_text.replace('[x]', '<input type="checkbox" disabled checked>')  # Necessário!
        return mkd_text
    
    def updatePreview(self, text_edit):
        """Atualiza a visualização com base no conteúdo do QTextEdit fornecido"""
        markdown_text = text_edit.toPlainText()
        self.verifyChangesAndSetTabName()
        
        self.html_text_ = self.getMarkdownText(markdown_text)
        print(self.html_text_)
        self.updateCompleteHtml()
        self.ui.previewArea2.setHtml(self.complete_html)
        ### TODO: Permitir ativar e desativar esta funcionalidade
        ##self.ui.previewArea.loadFinished.connect(self.scroll_to_bottom)

    def updateCompleteHtml(self):
        """Atualiza e redefine o conteúdo de complete_html"""
        self.complete_html = f"""
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
                    border: 1px solid #3399FF;
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
                ol {{
                    padding-left: 20px;           /* Recuo inicial da lista */
                    list-style-type: decimal;     /* Números padrão para a lista */
                    font-family: Arial, sans-serif; /* Fonte padrão */
                    line-height: 1.6;             /* Altura da linha para melhor legibilidade */
                }}
                ol ol {{
                    padding-left: 20px;           /* Recuo adicional para listas aninhadas */
                    list-style-type: lower-alpha; /* Letras minúsculas para segundo nível */
                           
                }}

                ol ol ol {{
                    padding-left: 20px;           /* Recuo adicional para listas de terceiro nível */
                    list-style-type: lower-roman; /* Números romanos minúsculos para terceiro nível */
                       
                }}
                code {{
                    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, "Liberation Mono", monospace;
                    padding: .2em .4em;
                    margin: 0;
                    font-size: 85%;
                    white-space: pre-wrap;
                    background-color: #afb8c133;
                    border-radius: 6px;
                    display: inline-block;
                }}
                pre code {{
                    background-color: #30363d;
                    padding: 0;
                    font-size: 100%;
                }}
                .codehilite
                pre {{
                    overflow: auto;
                    overflow-x: auto;
                    overflow-y: auto;
                    display: block;
                    background-color: #30363d;
                    /*padding: 1em;*/
                    overflow: auto;
                }}
                .codehilite .k {{ color: #f92672; }}  /* Palavras-chave em rosa */
                .codehilite .c {{ color: #75715e; font-style: italic; }}  /* Comentários em cinza */
                .codehilite .n {{ color: #a6e22e; }}  /* Nomes de variáveis em verde */
                .codehilite .s {{ color: #e6db74; }}
                /* Palavras-chave (e.g., public, final, class) */
                .codehilite .kd {{ color: #f92672; font-weight: bold; }}  /* Palavras-chave em rosa */

                /* Nome de classes (e.g., SaberToothedCat) */
                .codehilite .nc {{ color: #a6e22e; font-weight: bold; }}  /* Nome de classes em verde claro */

                /* Nomes de variáveis ou tipos (e.g., Animal, System) */
                .codehilite .n {{ color: #66d9ef; }}  /* Nomes de variáveis em azul claro */

                /* Anotações (e.g., @Override) */
                .codehilite .nd {{ color: #ae81ff; font-style: italic; }}  /* Anotações em roxo claro */

                /* Tipos de retorno (e.g., void) */
                .codehilite .kt {{ color: #fd971f; }}  /* Tipos de retorno em laranja */

                /* Nomes de métodos ou funções (e.g., makeSound) */
                .codehilite .nf {{ color: #a6e22e; font-weight: bold; }}  /* Nomes de métodos em verde claro */

                /* Comentários */
                .codehilite .c1 {{ color: #75715e; font-style: italic; }}  /* Comentários em cinza */

                /* Atributos ou membros (e.g., out, println) */
                .codehilite .na {{ color: #f8f8f2; }}  /* Atributos em branco */

                .codehilite .p {{ color: #f8f8f2; }}  /* Pontuação em branco */

                /* Strings */
                .codehilite .s {{ color: #e6db74; }}  /* Strings em amarelo */

                /* Espaçamento (não precisa de estilização, mas está incluído para clareza) */
                .codehilite .w {{ color: inherit; }}  
                table {{
                    /*border-collapse: collapse;*/
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
            {self.html_text_}
        </body>
        </html>
        """
    
    def verifyChangesAndSetTabName(self):
        current_index = self.ui.tab_widget.currentIndex()
        current_tab = self.ui.tab_widget.widget(current_index)
        if current_tab in self.ui.open_files:
            # Atualiza o estado de isModified para True
            file_path = self.ui.open_files[current_tab][0]
            isModified = self.ui.open_files[current_tab][1]
            if not file_path.endswith('*') and not isModified:
                file_name = file_path.split('/')[-1]  # Pega o último componente do caminho
                self.ui.tab_widget.setTabText(current_index, f"{file_name}*")
                self.ui.open_files[current_tab][1] = True
