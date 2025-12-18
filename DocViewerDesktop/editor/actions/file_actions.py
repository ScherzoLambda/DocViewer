from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QFileDialog, QMessageBox, QInputDialog, QTextEdit, QWidget, QVBoxLayout, QDialog, QLabel, QHBoxLayout, QPushButton
)
import os

from ui.ui_styles import style_text_edit


class FileActionsMixin:

    def new_file(self):
        new_tab = QWidget()
        self.ui.tab_widget.setStyleSheet("border-left: none;border-right: none;")
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setStyleSheet(style_text_edit)
        text_edit.setAcceptRichText(False)
        self.actual_text_edit = text_edit
        text_edit.setTabStopDistance(32)
        layout.addWidget(text_edit)
        layout.setContentsMargins(4, 4, 4, 4)
        new_tab.setLayout(layout)

        new_file_name = self.generate_new_file_name()
        tab_index = self.ui.tab_widget.addTab(new_tab, new_file_name)
        self.ui.tab_widget.setCurrentIndex(tab_index)
        text_edit.setFocus()
        text_edit.textChanged.connect(self.verifyChangesAndSetTabName)

        self.ui.open_files[new_tab] = [new_file_name, False, True]
        #self.checkIfAnyItemHidden()

    def generate_new_file_name(self):
        self.ui.new_file_count += 1
        base_name = "Novo Arquivo"
        file_name = f"{base_name} ({self.ui.new_file_count})"
        existing_tabs = [self.ui.tab_widget.tabText(i) for i in range(self.ui.tab_widget.count())]
        while file_name in existing_tabs:
            self.ui.new_file_count += 1
            file_name = f"{base_name} ({self.ui.new_file_count})"
        return file_name

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

    def renameTab(self, tab_index, tab_widget):
        """Renomeia a aba especificada e o arquivo associado"""
        # Obtém o nome atual da aba e o caminho completo do arquivo
        current_name = self.ui.tab_widget.tabText(tab_index)
        file_path = self.ui.open_files[tab_widget][0]  # Caminho atual do arquivo
        current_dir = os.path.dirname(file_path)  # Diretório atual do arquivo

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
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                # Usa o método existente saveFile (camelCase) e continua
                self.saveFile()
                return False
            elif reply == QMessageBox.Cancel:
                return True  # Cancela a ação
        return False

    def saveFileDialog(self):
        filter = "Markdown Files (*.md);;All Files (*)"
        fname, _ = QFileDialog.getSaveFileName(self, 'Save file', '', filter)
        current_index = self.ui.tab_widget.currentIndex()
        current_tab = self.ui.tab_widget.widget(current_index)
        if fname and fname != '':
            if not fname.endswith('.md'):
                fname += '.md'
            with open(fname, 'w', encoding='utf-8') as file:
                file.write(self.ui.editArea.toPlainText())

            self.ui.open_files[current_tab][0] = fname
            self.ui.open_files[current_tab][1] = False
            self.ui.open_files[current_tab][2] = False
            file_name = fname.split('/')[-1]  # Extrai o nome do arquivo do caminho
            self.ui.tab_widget.setTabText(current_index, file_name)
            self.ui.tab_widget.setTabToolTip(current_index, fname)
        else:
            return

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
                    # print(f"Arquivo {file_path} salvo com sucesso.")
        else:
            # Caso não haja um caminho, abre um diálogo para salvar como um novo arquivo
            self.saveFileDialog()

    # ============== Abertura de um arquivo/Novo Arquivo
    def open_here(self, tab_index):
        """Abre um arquivo na aba selecionada, substituindo o conteúdo atual"""
        options = QFileDialog.Options()
        file_path, full_path = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "",
                                                   "Todos os Arquivos (*);;Arquivos de Texto (*.txt);;Markdown Files (*.md)",
                                                   options=options)
        # print(self.current_file_path)
        # Só adiciona o watcher se o caminho for válido e existir
        if file_path:
            try:
                if os.path.exists(file_path):
                    # Evita adicionar duplicatas: verifica se já está sendo monitorado
                    try:
                        watched_files = self.file_watcher.files()
                    except Exception:
                        watched_files = []

                    if file_path not in watched_files:
                        try:
                            self.file_watcher.addPath(file_path)
                        except Exception as e:
                            print(f"Erro ao adicionar path ao file_watcher: {e}")
                else:
                    print(f"Caminho selecionado não existe: {file_path}")
            except Exception as e:
                print(f"Erro ao verificar/adicionar watcher: {e}")
        # print(file_path)
        # print(full_path)
        if file_path:
            try:

                # Carrega o conteúdo do arquivo selecionado
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Obtém o widget da aba selecionada
                current_tab = self.ui.tab_widget.widget(tab_index)
                if current_tab:
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

                            # print(f"Arquivo {file_name} aberto na aba {tab_index} com sucesso.")
            except Exception as e:
                print(f"Erro ao abrir o arquivo: {e}")

    def showDialogAndOpenFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filter = "Markdown Files (*.md);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", filter, options=options)

        if file_path:
            file_name = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                # content = file.read()
                # self.ui.previewArea.setPlainText(content)
                self.open_file(file, file_name, file_path)

    def open_file(self, file_, file_name, file_path=None):
        """Cria uma nova aba com um QTextEdit para abrir arquivo selecionado"""
        new_tab = QWidget()
        layout = QVBoxLayout()

        # Criando uma área de texto
        text_edit = QTextEdit()  # TextEditWithLineNumbers()
        text_edit.setTabStopDistance(32)
        text_edit.setAcceptRichText(False)
        layout.addWidget(text_edit)
        layout.setContentsMargins(4, 4, 4, 4)
        new_tab.setLayout(layout)
        text_edit.textChanged.connect(lambda: self.updatePreview(text_edit))
        text_edit.setPlainText(file_.read())

        # Adiciona uma nova aba com o editor de texto e o nome do arquivo como título da aba
        tab_index = self.ui.tab_widget.addTab(new_tab, file_name)
        self.ui.tab_widget.setCurrentIndex(tab_index)
        if (file_path):
            self.ui.tab_widget.setTabToolTip(tab_index, file_path)
        text_edit.setFocus()

        # Armazena o caminho do arquivo no widget da aba como chave
        self.ui.open_files[new_tab] = [file_.name, False, False]
        # self.checkIfAnyItemHidden()

    def open_initial_File(self, file_path_str=None):
        """
        Abre um arquivo.
        Se 'file_path_str' for fornecido, abre o arquivo diretamente.
        Caso contrário, abre uma caixa de diálogo para o usuário selecionar...
        """

        file_path = file_path_str
        #
        # # 1. Se o caminho do arquivo NÃO foi fornecido (ou é None), abre a caixa de diálogo.
        # if not file_path:
        #     options = QFileDialog.Options()
        #     options |= QFileDialog.ReadOnly
        #     filter = "Markdown Files (*.md);;All Files (*)"
        #     # A caixa de diálogo retorna o caminho e um filtro (que ignoramos com o _)
        #     file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", filter, options=options)
        #
        # 2. Se um caminho válido foi obtido (seja via parâmetro ou diálogo)
        if file_path and os.path.exists(file_path):
            try:
                # Garante que o nome do arquivo seja extraído corretamente
                file_name = os.path.basename(file_path)

                # Abre o arquivo para passá-lo para open_file
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Chama a sua função existente 'open_file'
                    self.open_file(file, file_name, file_path)

            except Exception as e:
                # Adicione tratamento de erro apropriado aqui (ex: mostrar mensagem de erro)
                print(f"Erro ao abrir o arquivo {file_path}: {e}")
                # Opcional: self.show_error_message("Erro de Leitura", f"Não foi possível ler o arquivo: {e}")


    def load_file_content(self):
        """
        Recarrega o conteúdo do arquivo monitorado no editor. chamado quando o arquivo é modificado externamente.
        """
        current_index = self.ui.tab_widget.currentIndex()
        current_tab = self.ui.tab_widget.widget(current_index)

        if current_tab in self.ui.open_files:
            file_info = self.ui.open_files[current_tab]
            file_path = file_info[0]

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Atualiza o conteúdo do QTextEdit
                layout = current_tab.layout()
                if layout is not None and layout.count() > 0:
                    text_edit = layout.itemAt(0).widget()
                    if isinstance(text_edit, QTextEdit):
                        text_edit.setPlainText(content)
                        self.ui.open_files[current_tab][1] = False  # Marca como não modificado

                print(f"Arquivo {file_path} recarregado com sucesso.")
            except Exception as e:
                print(f"Erro ao recarregar o arquivo: {e}")


class CustomConfirmDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle('DocViewer - Arquivo Modificado')
        self.setMinimumSize(600, 300)  # <<< Agora funciona!
        # self.setSizeGripEnabled(True)  # Permite redimensionar

        # Layout Principal
        main_layout = QVBoxLayout(self)

        # Rótulo da Mensagem (pode usar QLabel em vez de QMessageBox.setText)
        label = QLabel(message)
        label.setWordWrap(True)  # Para quebras de linha
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        # Layout dos Botões
        button_layout = QHBoxLayout()

        # Botões
        btn_yes = QPushButton('Sim')
        btn_no = QPushButton('Não')

        # Conexões
        btn_yes.clicked.connect(lambda: self.done(QMessageBox.StandardButton.Yes))
        btn_no.clicked.connect(lambda: self.done(QMessageBox.StandardButton.No))

        button_layout.addWidget(btn_yes)
        button_layout.addWidget(btn_no)

        main_layout.addLayout(button_layout)

        # Configurar o botão padrão (para pressionar Enter)
        btn_yes.setDefault(True)
        self.setResult(QMessageBox.StandardButton.No)  # Valor padrão de retorno caso feche a janela