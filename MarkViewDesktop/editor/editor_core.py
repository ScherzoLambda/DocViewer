
class EditorCore:
    def __init__(self, ui):
        self.ui = ui
        self._init_editor()

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
    