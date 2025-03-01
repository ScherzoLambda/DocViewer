import sys
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QMessageBox, QMenu, QFileDialog, QInputDialog,
                             QVBoxLayout, QWidget, QAction)
import markdown # necessario para as tabelas
from ui_docV import Ui_MainWindow

class MarkdownEditor(QMainWindow):

    def __init__(self, file_to_open=None):
        super().__init__()
        self.html_text_ = ""
    
        self.complete_html = ""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        #==================================================== Connect window funtcions to buttons
        self.ui.close_btn.clicked.connect(lambda: self.close())
        self.ui.minimize_btn.clicked.connect(lambda: self.showMinimized())
        self.ui.maxmize_btn.clicked.connect(lambda: self.restore_or_maximize())
        self._mousePressPos = None
        # Verify thats app has initialized by and open_file request
        if file_to_open:
            self.open_file(file_to_open)
        self.setFocus()

        #self.ui.splitter.splitterMoved.connect(self.checkSplitterSizes)

    def showEvent(self, event):
        super().showEvent(event)
        """Função chamada quando os componentes visuais ja foram carregados,
            apos a chamada de show()       
        """
        # Agora a janela está completamente carregada e podemos verificar o splitter
        #self.checkIfAnyItemHidden() 
    
    def initUI(self):
        self.ui.statusBarMessage()
        self.ui.menu = self.create_menu()
        self.ui.splitter.setStyleSheet("QSplitter::handle {background-color:#dfe2e5 ; border: 8px ridge  qlineargradient(spread:pad, x1:0.982591, y1:0.035, x2:0.273, y2:0.238636, stop:0.119318 rgba(199, 207, 255, 255), stop:1 rgba(139, 98, 155, 255)); }")
        self.ui.editArea.setFocus()
        self.ui.previewArea.setZoomFactor(0.8)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('DocViewer')

        self.ui.file_btn.clicked.connect(self.show_menu)
        self.ui.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.ui.tab_widget.currentChanged.connect(self.onTabChange)
        self.ui.tab_widget.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tab_widget.tabBar().customContextMenuRequested.connect(self.onTabRightClick)
    
    def create_menu(self):
        menu = QMenu()
        menu.setStyleSheet("QMenu { font-size: 12px; }")  # Aumentando o tamanho da fonte

        # Adicionando ações ao menu com atalhos
        new_file_act = menu.addAction("Novo arquivo")
        new_file_act.setShortcut("Ctrl+N")  # Atalho 
        new_file_act.triggered.connect(self.new_file)
        menu.addAction(new_file_act)

        op_file_act = menu.addAction("Abrir Arquivo")
        op_file_act.setShortcut("Ctrl+O")  # Atalho
        op_file_act.triggered.connect(self.showDialogAndOpenFile)
        menu.addAction(op_file_act)

        save_file_act = menu.addAction("Salvar Arquivo")
        save_file_act.setShortcut("Ctrl+S")
        save_file_act.triggered.connect(self.saveFile)
        menu.addAction(save_file_act)
        # Ajustando a largura do menu
        menu.setFixedWidth(210)  # Definindo uma largura fixa para o menu

        return menu
    
    def show_menu(self):
        if not self.ui.has_op_menu:
            self.ui.menu.exec_(self.ui.file_btn.mapToGlobal(self.ui.file_btn.rect().bottomLeft()))  # Exibir o menu abaixo do botão
            self.ui.has_op_menu = True
        else:
            # Se o menu está aberto, fecha-o
            #print("Fechando o menu...")
            self.ui.menu.close()
            #self.menu = None
            self.ui.has_op_menu = False    
    #======================================== Gerencia uso dos atalhos
    def keyPressEvent(self, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_N and event.modifiers() == Qt.ControlModifier:
                self.new_file()
            elif event.key() == Qt.Key_O and event.modifiers() == Qt.ControlModifier:
                self.showDialogAndOpenFile()
            elif event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
                self.saveFile()
            # elif event.key() == Qt.Key_Space and event.modifiers() == Qt.ControlModifier:
            #     self.renderPreview()
        super().keyPressEvent(event)
    #======================================== Mouse events para tratar redimensionamentos e Reposicionamentos
    def mousePressEvent(self, event):
        # Armazena a posição do mouse quando pressionado
        if event.button() == Qt.LeftButton:
            self._mousePressPos = event.pos()

    def mouseMoveEvent(self, event):
        # Move a janela com base na posição do mouse
        if self._mousePressPos is not None:
            self.move(self.pos() + event.pos() - self._mousePressPos)

    def mouseReleaseEvent(self, event):
        # Reseta a posição do mouse ao soltar
        self._mousePressPos = None
    #======================================== Gerencia{ Maximizar, miniminizar, Fechar} janela
    def restore_or_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def closeEvent(self, event):
        current_index = self.ui.tab_widget.currentIndex()
        # Método para interceptar o fechamento da janela
        if self.getCurrentFileModifiedStatus(current_index):
            reply = QMessageBox.question(
                self, 'Alterações não salvas',
                "Você tem alterações não salvas. Deseja salvar antes de sair?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Yes:
                self.saveFile()
            elif reply == QMessageBox.Cancel:
                event.ignore()  # Cancela o fechamento da janela
                return
        event.accept()  # Fecha a janela
    #======================================== Atualização da vizualização
    def eventFilter(self, obj, event):
        if obj == self.ui.editArea and event.type() == QtCore.QEvent.KeyRelease and event.key() == QtCore.Qt.Key_Return:
            self.inteliComplete()
        return super().eventFilter(obj, event)
    
    def inteliComplete(self):
        cursor = self.ui.editArea.textCursor()
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
        self.ui.editArea.setTextCursor(cursor) 
    
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
        self.updateCompleteHtml()
        self.ui.previewArea.setHtml(self.complete_html)
        ### TODO: Permitir ativar e desativar esta funcionalidade
        ##self.ui.previewArea.loadFinished.connect(self.scroll_to_bottom)

    def scroll_to_bottom(self):
        # Executa um scroll até o final da área de visualização
        scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
        self.ui.previewArea.page().runJavaScript(scroll_script)
    def updateAfterTabChange(self, textEdit):
        plain_text = textEdit.toPlainText()
        self.html_text_ = self.getMarkdownText(plain_text)
        self.updateCompleteHtml()
        self.ui.previewArea.setHtml(self.complete_html)
    
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
                    white-space: break-spaces;
                    background-color: #afb8c133;
                    border-radius: 6px;
                }}
                pre code {{
                    background-color: #30363d;
                    padding: 0;
                    font-size: 100%;
                }}
                pre {{
                    overflow: auto;
                    overflow-x: auto;
                    overflow-y: auto;
                    background-color: #30363d;
                    padding: 1em;
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
            {self.html_text_}
        </body>
        </html>
        """
    
    #======================================== Mudança de Aba
    def verifyChangesAndSetTabName(self):
        current_index = self.ui.tab_widget.currentIndex()
        current_tab = self.ui.tab_widget.widget(current_index)
        if current_tab in self.ui.open_files:
            # Atualiza o estado de isModified para True
            file_name = self.ui.open_files[current_tab][0]
            isModified = self.ui.open_files[current_tab][1]
            if not file_name.endswith('*') and not isModified:
                self.ui.tab_widget.setTabText(current_index, f"{os.path.basename(file_name)}*")
                self.ui.open_files[current_tab][1] = True

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

    def onTabChange(self, index):
        self.ui.editArea = self.getCurrentTextEdit(index)
        if(self.ui.editArea is not None):
            self.updateAfterTabChange(self.ui.editArea)
            self.ui.editArea.installEventFilter(self)
        #print(f"Aba mudada: {index}")
    
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
   
    def renameTab(self, tab_index, tab_widget):
        """Renomeia a aba especificada e o arquivo associado"""
        # Obtém o nome atual da aba e o caminho completo do arquivo
        current_name = self.ui.tab_widget.tabText(tab_index)
        file_path = self.ui.open_files[tab_widget][0]  # Caminho atual do arquivo
        current_dir = os.path.dirname(file_path)       # Diretório atual do arquivo

        # Solicita um novo nome para o arquivo
        new_name, ok = QInputDialog.getText(self, "Renomear arquivo", 
                                            "Novo nome para o arquivo:", 
                                            text=os.path.basename(current_name))
        if ok and new_name.strip():
            # Gera o novo caminho completo do arquivo
            new_file_path = os.path.join(current_dir, new_name.strip())

            try:
                # Renomeia o arquivo no sistema de arquivos
                os.rename(file_path, new_file_path)

                # Atualiza o nome da aba
                self.ui.tab_widget.setTabText(tab_index, new_name.strip())

                # Atualiza o nome no dicionário de arquivos abertos
                self.ui.open_files[tab_widget][0] = new_file_path

                print(f"Arquivo renomeado com sucesso para: {new_file_path}")
            except Exception as e:
                print(f"Erro ao renomear o arquivo: {e}")
        
    def getCurrentFileModifiedStatus(self, current_index):
        """Recupera apenas o status de modificação da aba atualmente selecionada"""
        if current_index == -1:
            # Nenhuma aba selecionada
            return None
        
        # Obtém o widget da aba selecionada
        current_tab = self.ui.tab_widget.widget(current_index)
        
        if current_tab is not None:
            # Verifica se a aba atual está no dicionário de arquivos abertos
            if current_tab in self.ui.open_files:
                file_info = self.ui.open_files[current_tab]
                is_modified = file_info[1]  # Status de modificação
                return is_modified

        return None
    
    def checkIfAnyItemHidden(self):
        """Verifica se algum item no QSplitter tem altura 0 (não está visível) e ajusta sua altura"""
        sizes = self.ui.splitter.sizes()  # Obtém as alturas dos widgets no QSplitter
        updated = False
        # Define as alturas específicas para os itens
        if len(sizes) >= 2:
            sizes[0] = 186  # Define a altura do primeiro widget para 186
            sizes[1] = 288  # Define a altura do segundo widget para 288
        
            # Atualiza os tamanhos no QSplitter
            self.ui.splitter.setSizes(sizes)
            #print("Alturas ajustadas: Item 0 = 186, Item 1 = 288")
        else:
            #print("O QSplitter não possui widgets suficientes para ajustar as alturas.")
            updated = True

        if updated:
            # Atualiza os tamanhos no QSplitter com os novos valores
            self.ui.splitter.setSizes(sizes)
            #print("Altura ajustada para itens escondidos.")

    def close_tab(self, index):
        """Fecha a aba na posição fornecida, verificando se há alterações não salvas"""
        widget = self.ui.tab_widget.widget(index)

        if self.check_unsaved_changes(index):
            return  # Se o usuário cancelar, não fecha a aba

        # Remove a aba
        self.ui.tab_widget.removeTab(index)

        # Remove o widget da lista de arquivos abertos
        if widget in self.ui.open_files:
            del self.ui.open_files[widget]    
    #======================================== Lida com arquivos {Abertura, escrita}
    #============== Salvamento de arquivos
    def check_unsaved_changes(self, tab_index):
        """Verifica se a aba atual tem alterações não salvas e oferece para salvar"""
        widget = self.ui.tab_widget.widget(tab_index)
        if not widget:
            return False

        text_edit = widget.findChild(QTextEdit)

        if text_edit and text_edit.document().isModified():
            # Pergunta ao usuário se ele quer salvar as alterações
            reply = QMessageBox.question(self, "Arquivo Modificado",
                                            "O arquivo foi modificado. Deseja salvar as alterações?",
                                            QMessageBox.Yes | QMessageBox.No |QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                return self.save_file(tab_index)
            elif reply == QMessageBox.Cancel:
                return True  # Cancela a ação
        return False
    
    def saveFileDialog(self):
        # Define o filtro para apenas arquivos .md
        filter = "Markdown Files (*.md);;All Files (*)"
        fname, _ = QFileDialog.getSaveFileName(self, 'Save file', '', filter)
        current_index = self.ui.tab_widget.currentIndex()
        current_tab = self.ui.tab_widget.widget(current_index)
        if fname:
            # Adiciona a extensão .md se não estiver presente
            if not fname.endswith('.md'):
                fname += '.md'
            with open(fname, 'w', encoding='utf-8') as file:
                file.write(self.ui.editArea.toPlainText())    
        # Atualiza o nome da aba atual para o nome do arquivo salvo
        self.ui.open_files[current_tab][1] = False
        self.ui.open_files[current_tab][2] = False
        file_name = fname.split('/')[-1]  # Extrai o nome do arquivo do caminho
        self.ui.tab_widget.setTabText(current_index, file_name)
        self.ui.tab_widget.setTabToolTip(current_index, fname)
    
    def saveFile(self):
        """Salva as mudanças no arquivo atual"""
        # Obtém a aba atual e o caminho do arquivo associado a ela
        current_index = self.ui.tab_widget.currentIndex()
        current_tab = self.ui.tab_widget.widget(current_index)
        
        file_info = self.ui.open_files[current_tab]
        file_path = file_info[0]
        isNewFile = file_info[2] 

        if not isNewFile:
            
            if file_path:
                # Sobrescreve o arquivo atual com o conteúdo do QTextEdit
                text_edit = current_tab.layout().itemAt(0).widget()
                if isinstance(text_edit, QTextEdit):
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(text_edit.toPlainText())
                        self.ui.open_files[current_tab][1] = False

                        # Remove o '*' do nome da aba
                        clean_file_name = os.path.basename(file_path)  # Apenas o nome do arquivo sem o caminho
                        self.ui.tab_widget.setTabText(current_index, clean_file_name)
                    #print(f"Arquivo {file_path} salvo com sucesso.")
        else:
            # Caso não haja um caminho, abre um diálogo para salvar como um novo arquivo
            self.saveFileDialog()
    #============== Abertura de um arquivo/Novo Arquivo
    def open_here(self, tab_index):
        """Abre um arquivo na aba selecionada, substituindo o conteúdo atual"""
        # Abre um diálogo para selecionar o arquivo
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Todos os Arquivos (*);;Arquivos de Texto (*.txt);;Markdown Files (*.md)", options=options)
        
        if file_path:
            try:
                # Carrega o conteúdo do arquivo selecionado
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Obtém o widget da aba selecionada
                current_tab = self.ui.tab_widget.widget(tab_index)
                if current_tab:
                    # Procura pelo QTextEdit dentro do layout da aba
                    layout = current_tab.layout()
                    if layout is not None and layout.count() > 0:
                        # Assume que o QTextEdit é o primeiro widget no layout
                        text_edit = layout.itemAt(0).widget()
                        if isinstance(text_edit, QTextEdit):
                            # Substitui o conteúdo do QTextEdit pelo conteúdo do arquivo
                            text_edit.setPlainText(content)
                            
                            # Atualiza o nome da aba com o nome do arquivo aberto
                            file_name = os.path.basename(file_path)
                            self.ui.tab_widget.setTabText(tab_index, file_name)
                            self.ui.tab_widget.setTabToolTip(tab_index, file_path)
                            
                            # Atualiza o dicionário de arquivos abertos
                            self.ui.open_files[current_tab] = [file_name, False, False]
                            
                            print(f"Arquivo {file_name} aberto na aba {tab_index} com sucesso.")
            except Exception as e:
                print(f"Erro ao abrir o arquivo: {e}")
    
    def showDialogAndOpenFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Abre o arquivo em modo somente leitura
        filter = "Markdown Files (*.md);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "",filter,options=options)

        file_name = ""
        if file_path:
            file_name = os.path.basename(file_path)
            # Carregar o conteúdo do arquivo ou realizar alguma ação com ele
            with open(file_path, 'r',encoding='utf-8') as file:
                # content = file.read()
                # self.ui.previewArea.setPlainText(content)
                self.open_file(file, file_name, file_path)
    
    def open_file(self, file_, file_name, file_path=None):
        """Cria uma nova aba com um QTextEdit para abrir arquivo selecionado"""
        new_tab = QWidget()
        layout = QVBoxLayout()

        # Criando uma área de texto
        text_edit = QTextEdit()  # TextEditWithLineNumbers()
        text_edit.setStyleSheet("background-color: #DCDCDC;")
        text_edit.setTabStopDistance(32)
        layout.addWidget(text_edit)
        layout.setContentsMargins(4, 4, 4, 4)
        new_tab.setLayout(layout)
        text_edit.textChanged.connect(lambda: self.updatePreview(text_edit))
        text_edit.setPlainText(file_.read())

        # Adiciona uma nova aba com o editor de texto e o nome do arquivo como título da aba
        tab_index = self.ui.tab_widget.addTab(new_tab, file_name)
        self.ui.tab_widget.setCurrentIndex(tab_index)
        if(file_path):
            self.ui.tab_widget.setTabToolTip(tab_index,file_path)
        text_edit.setFocus()

        # Armazena o caminho do arquivo no widget da aba como chave
        self.ui.open_files[new_tab] = [file_.name, False, False]
        self.checkIfAnyItemHidden()
    
    def new_file(self):
        """Cria uma nova aba com um QTextEdit para um novo arquivo"""
        new_tab = QWidget()
        layout = QVBoxLayout()

        # Criando uma área de texto
        text_edit = QTextEdit() #TextEditWithLineNumbers()
        text_edit.setStyleSheet("background-color: #DCDCDC;")
        text_edit.setTabStopDistance(32)
        layout.addWidget(text_edit)
        layout.setContentsMargins(4, 4, 4, 4)
        new_tab.setLayout(layout)
        text_edit.textChanged.connect(lambda: self.updatePreview(text_edit))
        # Gera um nome único para o novo arquivo
        new_file_name = self.generate_new_file_name()
        # Adiciona uma nova aba com o editor de texto
        tab_index = self.ui.tab_widget.addTab(new_tab, new_file_name)
        self.ui.tab_widget.setCurrentIndex(tab_index)
        text_edit.setFocus()
        #============================= [, isModified, isNewFile]
        self.ui.open_files[new_tab] = [new_file_name, False, True]
        self.checkIfAnyItemHidden()

    def generate_new_file_name(self):
        """Gera um nome de arquivo novo único com base no número de arquivos novos"""
        self.ui.new_file_count += 1
        base_name = "Novo Arquivo"
        file_name = f"{base_name} ({self.ui.new_file_count})"

        # Garante que o nome é único entre as abas
        existing_tabs = [self.ui.tab_widget.tabText(i) for i in range(self.ui.tab_widget.count())]
        while file_name in existing_tabs:
            self.ui.new_file_count += 1
            file_name = f"{base_name} ({self.ui.new_file_count})"

        return file_name
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #styleSheetFile = QFile("./docV.qss")
    #if styleSheetFile.open(QFile.ReadOnly):
    #    styleSheet = str(styleSheetFile.readAll(), encoding='utf-8')  # Leitura e conversão para string
    #    app.setStyleSheet(styleSheet)
    #    styleSheetFile.close()
    window = MarkdownEditor()
    window.show()
    sys.exit(app.exec_())
