import sys
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QSplitter, QLabel, QSpinBox, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QTextCursor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWebEngineWidgets import QWebEngineView

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)

def loadSvgIcon(file_path, width=80, height=80):
    svg_renderer = QSvgRenderer(file_path)
    pixmap = QPixmap(width, height)
    pixmap.fill(QtCore.Qt.transparent)
    painter = QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()
    return pixmap

class Ui_MainWindow(object):
    iconspath = "_internal\\"+ "\\icons" + "\\"
    style_button = """
    QToolTip,
    QPushButton {
         /* Cor de fundo padrão */
        border: 2px solid #161b22; /* Borda */
        color: white; /* Cor do texto */
        
        border-radius: 4px; /* Borda arredondada */
    }
    QPushButton:hover {
        background-color: #DCDCDC; /* Cor de fundo quando o mouse está sobre o botão */
    }
    """
    style_utils = """
         /* Cor de fundo padrão */
        border: 2px solid #161b22; /* Borda */
        color: white; /* Cor do texto */
        font-size: 16px;
        border-radius: 4px; /* Borda arredondada */
    """
    style_closeBTN = """
    QPushButton {
        border: none;
        background-color: transparent;
    }
    QPushButton:hover {
        background-color: #f4696b;  /* cor de fundo*/
    }
    """
    style_m_M = """
    QPushButton {
        font-size: 18px;
        border: none;
        background-color: transparent;
    }
    QPushButton:hover {
        background-color: #DCDCDC;  
    }
"""
    style = f"""
        QTabWidget::pane {{
            background-image: url({iconspath+"docV_icon.png"});
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        }}
    """
    def setupUi(self, MainWindow):
        self.new_file_count = 0
        self.open_files = {}
        self.menu = None
        self.has_op_menu = False
        self.act_op_file = None
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(539, 307)
        MainWindow.setStyleSheet("background-color: rgb(117, 117, 117);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralVL = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralVL.setObjectName("centralVL")
        #self.centralVL.setSpacing(0)
        self.centralVL.setContentsMargins(0, 0, 0, 0)

        # Frames for layouts
        # header_frame, buttons_frame
        self.header_frame = QtWidgets.QFrame(self.centralwidget)
        self.header_frame.setStyleSheet("background-color: rgb(117, 117, 117);")
        self.header_frame.setObjectName("header_frame")
        self.buttons_frame = QtWidgets.QFrame(self.centralwidget)
        self.buttons_frame.setStyleSheet("background-color: rgb(117, 117, 117);")
        self.buttons_frame.setObjectName("buttons_frame")
        # Layouts for components
        # editButtonsHL, headerVL, headerLayout
        self.headerVL = QtWidgets.QVBoxLayout(self.header_frame)
        self.headerVL.setObjectName("headerVL")
        self.editButtonsHL = QtWidgets.QHBoxLayout(self.buttons_frame)
        self.editButtonsHL.setObjectName("editButtonsHL")
        self.editButtonsHL.setSpacing(10)

        self.headerVL.setContentsMargins(0, 0, 0, 0)
        #self.editButtonsHL.setContentsMargins(0, 0, 0, 0)

        # ===================== Header for headerVL
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.headerLayout.setObjectName("headerLayout")
        self.headerLayout.setSpacing(0)
        self.headerLayout.setContentsMargins(0, 0, 0, 0)
        # ICON label
        self.icon_label = QtWidgets.QLabel(self.header_frame)
        self.icon_label.setPixmap(QPixmap(resource_path('icons/docV_icon.png')).scaled(35, 35, aspectRatioMode=QtCore.Qt.KeepAspectRatio))
        self.icon_label.setMaximumHeight(30)
        self.icon_label.setMaximumWidth(45)
        self.icon_label.setContentsMargins(8,0,0,0)
        # FILE button
        self.file_btn = QtWidgets.QPushButton(self.header_frame)
        self.file_btn.setStyleSheet(self.style_m_M)
        self.file_btn.setObjectName("file_btn")
        self.file_btn.setText("File")
        self.file_btn.setMaximumHeight(30)
        self.file_btn.setMaximumWidth(45)

        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # CLOSE WINDOW button
        self.close_btn = QtWidgets.QPushButton(self.header_frame)
        self.close_btn.setIcon(QIcon(resource_path('icons/close.png')))
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setStyleSheet(self.style_closeBTN)
        self.close_btn.setMaximumHeight(30)
        self.close_btn.setMaximumWidth(45)
        #self.close_btn.setToolTip("Close Window")
        # MINIMIZE WINDOW button
        self.minimize_btn = QtWidgets.QPushButton(self.header_frame)
        self.minimize_btn.setIcon(QIcon(resource_path('icons/mini2.png')))
        self.minimize_btn.setObjectName("close_btn")
        self.minimize_btn.setStyleSheet(self.style_m_M)
        self.minimize_btn.setMaximumHeight(30)
        self.minimize_btn.setMaximumWidth(45)
        #self.minimize_btn.setToolTip("Minimize Window")
        # MAXIMIZE WINDOW button
        self.maxmize_btn = QtWidgets.QPushButton(self.header_frame)
        self.maxmize_btn.setIcon(QIcon(resource_path('icons/maximizar.png')))
        self.maxmize_btn.setObjectName("maxmize_btn")
        self.maxmize_btn.setStyleSheet(self.style_m_M)
        self.maxmize_btn.setMaximumHeight(30)
        self.maxmize_btn.setMaximumWidth(45)
        #self.maxmize_btn.setToolTip("Maxmize Window")
        # Adjusting size and alignment
        self.file_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.minimize_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maxmize_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.close_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        self.headerLayout.setAlignment(self.file_btn, QtCore.Qt.AlignLeft)
        self.headerLayout.setAlignment(self.minimize_btn, QtCore.Qt.AlignRight)
        self.headerLayout.setAlignment(self.maxmize_btn, QtCore.Qt.AlignRight)
        self.headerLayout.setAlignment(self.close_btn, QtCore.Qt.AlignRight) 
        # adding widgets to layout
        self.headerLayout.addWidget(self.icon_label)
        self.headerLayout.addWidget(self.file_btn)
        self.headerLayout.addItem(spacer)
        self.headerLayout.addWidget(self.minimize_btn)
        self.headerLayout.addWidget(self.maxmize_btn)
        self.headerLayout.addWidget(self.close_btn)
        
        self.headerVL.addLayout(self.headerLayout)
        self.centralVL.addWidget(self.header_frame)

        # ================= Fonte style and Size ===================
        self.fontSize_sp = QSpinBox(self.buttons_frame)
        self.fontSize_sp.setStyleSheet(self.style_utils)
        self.fontSize_sp.setToolTip("Tamanho do texto")
        self.fontSize_sp.setRange(8, 72)  # Define o intervalo do tamanho da fonte
        self.fontSize_sp.setValue(16)  # Define o valor padrão
        self.fontSize_sp.valueChanged.connect(self.update_font_size)  # Conecta a mudança de valor ao método

        self.fontStyle_cb = QComboBox(self.buttons_frame)
        self.fontStyle_cb.setToolTip("Fonte do texto")
        self.fontStyle_cb.setMaximumWidth(110)
        self.fontStyle_cb.setStyleSheet(self.style_utils)
        self.fontStyle_cb.addItems(["Arial", "Courier New", "Times New Roman"])
        self.fontStyle_cb.currentIndexChanged.connect(self.update_font_style)
        
        self.editButtonsHL.addWidget(self.fontStyle_cb)
        self.editButtonsHL.addWidget(self.fontSize_sp)
        
        # ================= Markdown Utilities ========================
        self.heading_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.heading_btn.setObjectName("heading_btn")
        self.heading_btn.setStyleSheet(self.style_button)
        self.heading_btn.setMinimumHeight(25)
        self.editButtonsHL.addWidget(self.heading_btn)
        self.heading_btn.setIcon(QIcon(loadSvgIcon(resource_path('icons/bx-heading.svg'))))
        self.heading_btn.setToolTip("Header text")
        
        self.bold_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.bold_btn.setObjectName("bold_btn")
        self.bold_btn.setMinimumHeight(25)
        self.bold_btn.setStyleSheet(self.style_button)
        self.bold_btn.setIcon(QIcon(loadSvgIcon(resource_path('icons/bold.svg'))))
        self.bold_btn.setToolTip("Bold text")
        self.editButtonsHL.addWidget(self.bold_btn)
        
        self.italic_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.italic_btn.setObjectName("italic_btn")
        self.italic_btn.setStyleSheet(self.style_button)
        self.italic_btn.setMinimumHeight(25)
        self.italic_btn.setMinimumWidth(15)
        self.italic_btn.setIcon(QIcon(loadSvgIcon(resource_path('icons/bx-italic.svg'))))
        self.italic_btn.setToolTip("Italic Text")
        self.editButtonsHL.addWidget(self.italic_btn)
        
        self.quote_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.quote_btn.setObjectName("quote_btn")
        self.quote_btn.setStyleSheet(self.style_button)
        self.quote_btn.setMinimumHeight(25)
        self.quote_btn.setIcon(QIcon(loadSvgIcon(resource_path('icons/bxs-quote-right.svg'))))
        self.quote_btn.setToolTip("Block Quote")
        self.editButtonsHL.addWidget(self.quote_btn)
        
        self.link_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.link_btn.setObjectName("link_btn")
        self.link_btn.setStyleSheet(self.style_button)
        self.link_btn.setMinimumHeight(25)
        self.link_btn.setIcon(QIcon(loadSvgIcon(resource_path('icons/bx-link.svg'))))
        self.link_btn.setToolTip("refer a link")
        self.editButtonsHL.addWidget(self.link_btn)
        
        self.unList_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.unList_btn.setObjectName("unList_btn")
        self.unList_btn.setStyleSheet(self.style_button)
        self.unList_btn.setMinimumHeight(25)
        icon = QtGui.QIcon(resource_path('icons/menu.png'))
        pixmap = icon.pixmap(QtCore.QSize(100, 100))
        pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) # Redimensiona a imagem
        self.unList_btn.setIcon(QtGui.QIcon(pixmap))
        self.unList_btn.setToolTip("Unordered List")
        self.editButtonsHL.addWidget(self.unList_btn)
        
        self.nList_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.nList_btn.setObjectName("nList_btn")
        self.nList_btn.setStyleSheet(self.style_button)
        self.nList_btn.setMinimumHeight(25)
        icon = QtGui.QIcon(resource_path('icons/number.png'))
        pixmap = icon.pixmap(QtCore.QSize(100, 100))
        pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) # Redimensiona a imagem
        self.nList_btn.setIcon(QtGui.QIcon(pixmap))
        self.nList_btn.setText("")
        self.nList_btn.setToolTip("Numbered List")
        self.editButtonsHL.addWidget(self.nList_btn)
        
        self.taskList_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.taskList_btn.setObjectName("taskList_btn")
        self.taskList_btn.setStyleSheet(self.style_button)
        self.taskList_btn.setMinimumHeight(25)
        icon = QtGui.QIcon(resource_path('icons/check_2.png'))
        pixmap = icon.pixmap(QtCore.QSize(100, 100))
        pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.taskList_btn.setIcon(QtGui.QIcon(pixmap))
        self.taskList_btn.setToolTip("Task List")
        self.editButtonsHL.addWidget(self.taskList_btn)
        
        #========================================= adding input_frame to centralVL
        self.centralVL.addWidget(self.buttons_frame)

        # ================= Spliter, InputArea(EditArea), tab_widget
        # editArea is for a tab on tab_widget, added on call of function new_file() defined in main.py
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.splitter = QSplitter(QtCore.Qt.Vertical)
        self.editArea = QtWidgets.QTextEdit() #TextEditWithLineNumbers()
        self.editArea.setStyleSheet("background-color: #DCDCDC;")
        self.editArea.setObjectName("editArea")
        font = QFont()
        font.setPointSize(16)
        self.editArea.setFont(font)
        self.splitter.addWidget(self.tab_widget)

        #========================================= adding splitter to centralVL
        self.centralVL.addWidget(self.splitter)
        
        self.previewArea = QWebEngineView()
        self.previewArea.setContextMenuPolicy(0) # Desabilita menu de contexto. 0=Qt.NoContextMenu
        #========================================= adding previewArea to splitter
        self.splitter.addWidget(self.previewArea)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("background-color: #dfe2e5;")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Conecta ações auxilio markdown aos  respectivos botoes
        self.heading_btn.clicked.connect(self.addHeader)
        self.bold_btn.clicked.connect(self.addBold)
        self.italic_btn.clicked.connect(self.addItalic)
        self.quote_btn.clicked.connect(self.addQuote)
        self.link_btn.clicked.connect(self.addLink)
        self.unList_btn.clicked.connect(self.addUnList)
        self.nList_btn.clicked.connect(self.addNList)
        self.taskList_btn.clicked.connect(self.addTaskList)

    
    def statusBarMessage(self):
        self.init_status_bar()
    def init_status_bar(self):

        # Adicionando um rótulo à barra de status
        # self.status_label = QLabel("\t\t Bem Vindo(a)!!")
        # self.status_label.setStyleSheet("color: black;")
        # self.statusbar.addWidget(self.status_label)  # Use addWidget para garantir visibilidade

        # Personalizando a barra de status com estilo
        self.statusbar.setStyleSheet("""
            QStatusBar {{
                background-color: #2b2b2b;
                color: black;
                font-size: 12px;
            }}
            QLabel {{
                font-weight: bold;
                color: black;
            }}
            QProgressBar {{
                border: 1px solid #3a3f44;
                background-color: #1c1c1c;
                color: #d4d4d4;
                text-align: center;
            }}
            QPushButton {{
                border: 1px solid #5a5a5a;
                padding: 3px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: #4a4a4a;
            }}
        """)
    
    #================Funções para os botoes de auxilio do Markdown
    def update_font_size(self):
        font = self.editArea.font()
        font.setPointSize(self.fontSize_sp.value())
        self.editArea.setFont(font)

    def update_font_style(self):
        font = self.editArea.font()
        font.setFamily(self.fontStyle_cb.currentText())
        self.editArea.setFont(font)
        
    def addHeader(self):
        cursor = self.editArea.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.insertText(f"# {selected_text}")
            self.editArea.setFocus()
        else:
            current_line = cursor.block().text().strip()
            if current_line.startswith("#"):
                new_line = current_line.replace("#", "## ",1)
                cursor.select(QTextCursor.BlockUnderCursor)
                cursor.removeSelectedText()
                cursor.insertText(new_line)
                cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, 1)
                self.editArea.setTextCursor(cursor)
                self.editArea.setFocus()                
            else:
                cursor.insertText("# ")
                cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, 1)
                self.editArea.setTextCursor(cursor)
                self.editArea.setFocus()
    
    def addBold(self):
        cursor = self.editArea.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.insertText(f"**{selected_text}**")
            self.editArea.setFocus()
        else:
            cursor.insertText("**")
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.MoveAnchor, 2)
            cursor.insertText("**")
            self.editArea.setTextCursor(cursor)
            self.editArea.setFocus()
    
    def addItalic(self):
        cursor = self.editArea.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.insertText(f"_{selected_text}_")
            self.editArea.setFocus()
        else:
            cursor.insertText("_")
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.MoveAnchor, 1)
            cursor.insertText("_")
            self.editArea.setTextCursor(cursor)
            self.editArea.setFocus()
        
    def addLink(self):
        cursor = self.editArea.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.insertText(f"[{selected_text}](url)")
            self.editArea.setFocus()
        else:
            cursor.insertText("[nome_link](url) ")
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.MoveAnchor, 7)
            self.editArea.setTextCursor(cursor)
            self.editArea.setFocus()    
    
    def addQuote(self):
        cursor = self.editArea.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.insertText(f"> {selected_text}")
            self.editArea.setFocus()
        else:
            cursor.insertText(">")
            self.editArea.setTextCursor(cursor)
            self.editArea.setFocus()    
    
    def addUnList(self):
        cursor = self.editArea.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.insertText(f"- {selected_text}")
            self.editArea.setFocus()
        else:
            cursor.insertText("- ")
            self.editArea.setTextCursor(cursor)
            self.editArea.setFocus()    
    
    def addNList(self):
        cursor = self.editArea.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.insertText(f"1. {selected_text}")
            self.editArea.setFocus()
        else:
            cursor.insertText("1.")
            self.editArea.setTextCursor(cursor)
            self.editArea.setFocus()    
    
    def addTaskList(self):
        cursor = self.editArea.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.insertText(f"- [ ] {selected_text}")
            self.editArea.setFocus()
        else:
            cursor.insertText("- [ ] ")
            self.editArea.setTextCursor(cursor)
            self.editArea.setFocus()

    #================ Função que traduz a UI
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DocViewer"))
        self.heading_btn.setText("")
        self.bold_btn.setText("")
        self.italic_btn.setText("")
        self.quote_btn.setText("")
        self.link_btn.setText("")
        self.unList_btn.setText("")
        self.nList_btn.setText("")
        self.taskList_btn.setText("")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
