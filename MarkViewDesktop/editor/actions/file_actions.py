"""Módulo para ações relacionadas a arquivos no editor"""
class FileActions:
    def __init__(self, ui):
        self.ui = ui
        self.ui.new_file_count = 0  # Contador para novos arquivos

    def new_file(self):
        """Cria uma nova aba de arquivo com um nome único"""
        file_name = generate_new_file_name(self.ui.tab_widget)
        new_tab = self.ui.create_new_tab(file_name)
        self.ui.tab_widget.addTab(new_tab, file_name)
        self.ui.tab_widget.setCurrentWidget(new_tab)

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
        text_edit.setStyleSheet("background-color: #DCDCDC; color:black")
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