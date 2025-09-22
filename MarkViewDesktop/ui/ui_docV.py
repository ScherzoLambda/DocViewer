import sys
import os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter, QSpinBox, QComboBox, QTextBrowser
from PySide6.QtGui import QIcon, QPixmap, QPainter, QFont, QTextCursor
from PySide6.QtSvg import QSvgRenderer
# from PySide6.QtWebEngineWidgets import QWebEngineView

from ui.ui_utils import *

def resource_path(relative_path: str) -> str:
    """Obtém o caminho absoluto do recurso, funciona no dev e no executável."""
    if hasattr(sys, "_MEIPASS"):
        # quando rodando no executável do PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def loadSvgIcon(file_path, width=80, height=80):
    svg_renderer = QSvgRenderer(file_path)
    pixmap = QPixmap(width, height)
    pixmap.fill(QtCore.Qt.transparent)
    painter = QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()
    return pixmap

class Ui_MainWindow(object):
    # iconspath = "_internal\\"+ "\\icons_svg" + "\\"
    iconspath = resource_path("resources/icons_svg/")
    print(iconspath)

    def setupUi(self, MainWindow):
        self.new_file_count = 0
        self.open_files = {}
        self.menu = None
        self.has_open_menu = False
        self.act_op_file = None
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(539, 307)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralVL = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralVL.setObjectName("centralVL")
        self.centralVL.setSpacing(0)
        self.centralVL.setContentsMargins(0, 0, 0, 0)

        # Frames for layouts
        # header_frame, buttons_frame
        self.header_frame = QtWidgets.QFrame(self.centralwidget)
        # self.header_frame.setStyleSheet(self.style_button)
        self.header_frame.setMinimumHeight(50)
        # self.header_frame.setObjectName("header_frame")
        self.buttons_frame = QtWidgets.QFrame(self.centralwidget)
        self.buttons_frame.setStyleSheet("background-color: rgb(117, 117, 117); border-top:none; border-bottom:none;")
        self.buttons_frame.setObjectName("buttons_frame")
        self.buttons_frame.setMaximumHeight(60)
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
        self.headerLayout.setSpacing(5)
        self.headerLayout.setContentsMargins(0, 0, 0, 0)
        # ICON label
        self.icon_label = QtWidgets.QLabel(self.header_frame)
        self.icon_label.setStyleSheet(style_button)
        self.icon_label.setPixmap(QPixmap(resource_path('resources/icons_svg/docV_icon.png')).scaled(35, 35, QtCore.Qt.KeepAspectRatio))
        self.icon_label.setMaximumHeight(30)
        self.icon_label.setMaximumWidth(45)
        self.icon_label.setContentsMargins(8,0,0,0)
        # FILE button
        self.file_btn = QtWidgets.QPushButton(self.header_frame)
        self.file_btn.setContentsMargins(0,0,0,0)
        self.file_btn.setText("File")
        self.file_btn.setMaximumHeight(30)
        self.file_btn.setMaximumWidth(50)
        # SETTINGS button
        self.settings_btn = QtWidgets.QPushButton(self.header_frame)
        self.settings_btn.setContentsMargins(8,0,0,8)
        self.settings_btn.setText("Configurações")
        self.settings_btn.setMaximumHeight(30)

        right_spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        spacer = QtWidgets.QSpacerItem(50, 35, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # CLOSE WINDOW button
        self.close_btn = QtWidgets.QPushButton(self.header_frame)
        self.close_btn.setIcon(QIcon(
            loadSvgIconColored(self.iconspath+'close-new.svg')))
        self.close_btn.setObjectName("close_btn")
        # self.close_btn.setStyleSheet(style_closeBTN)
        self.close_btn.setMaximumHeight(30)
        self.close_btn.setMaximumWidth(45)
        self.close_btn.setContentsMargins(0,0,10,0)
        #self.close_btn.setToolTip("Close Window")
        # MINIMIZE WINDOW button
        self.minimize_btn = QtWidgets.QPushButton(self.header_frame)
        self.minimize_btn.setIcon(QIcon(
            loadSvgIconColored(self.iconspath+'mini-new.svg')))
        self.minimize_btn.setObjectName("close_btn")
        self.minimize_btn.setStyleSheet(style_m_M)
        self.minimize_btn.setMaximumHeight(30)
        self.minimize_btn.setMaximumWidth(45)
        #self.minimize_btn.setToolTip("Minimize Window")
        # MAXIMIZE WINDOW button
        self.maxmize_btn = QtWidgets.QPushButton(self.header_frame)
        self.maxmize_btn.setIcon(QIcon(
            loadSvgIconColored(self.iconspath+'maxi-new.svg',color='#ffffff')))
        self.maxmize_btn.setObjectName("maxmize_btn")
        self.maxmize_btn.setStyleSheet(style_m_M)
        self.maxmize_btn.setMaximumHeight(30)
        self.maxmize_btn.setMaximumWidth(45)
        #self.maxmize_btn.setToolTip("Maxmize Window")
        # Adjusting size and alignment
        self.file_btn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_btn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.minimize_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.maxmize_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.close_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.headerLayout.setAlignment(self.file_btn, QtCore.Qt.AlignLeft)
        self.headerLayout.setAlignment(self.settings_btn, QtCore.Qt.AlignLeft)
        self.headerLayout.setAlignment(self.minimize_btn, QtCore.Qt.AlignRight)
        self.headerLayout.setAlignment(self.maxmize_btn, QtCore.Qt.AlignRight)
        self.headerLayout.setAlignment(self.close_btn, QtCore.Qt.AlignRight)
        # adding widgets to layout
        self.headerLayout.addWidget(self.icon_label)
        self.headerLayout.addWidget(self.file_btn)
        self.headerLayout.addWidget(self.settings_btn)
        self.headerLayout.addItem(spacer)
        self.headerLayout.addWidget(self.minimize_btn)
        self.headerLayout.addWidget(self.maxmize_btn)
        self.headerLayout.addWidget(self.close_btn)
        self.headerLayout.addItem(right_spacer)

        self.headerVL.addLayout(self.headerLayout)
        self.centralVL.addWidget(self.header_frame)
        MainWindow.title_bar = self.header_frame
        # ================= Fonte style and Size ===================
        self.fontSize_sp = QSpinBox(self.buttons_frame)
        # self.fontSize_sp.setStyleSheet(self.style_utils)
        self.fontSize_sp.setToolTip("Tamanho do texto")
        self.fontSize_sp.setRange(8, 72)  # Define o intervalo do tamanho da fonte
        self.fontSize_sp.setValue(16)  # Define o valor padrão
        self.fontSize_sp.valueChanged.connect(self.update_font_size)  # Conecta a mudança de valor ao método

        self.fontStyle_cb = QComboBox(self.buttons_frame)
        self.fontStyle_cb.setToolTip("Fonte do texto")
        self.fontStyle_cb.setMaximumWidth(130)
        self.fontStyle_cb.setMaximumHeight(30)
        self.fontStyle_cb.setStyleSheet(style_utils)
        self.fontStyle_cb.addItems(["Arial", "Courier New", "Times New Roman"])
        self.fontStyle_cb.currentIndexChanged.connect(self.update_font_style)
        
        self.editButtonsHL.addWidget(self.fontStyle_cb)
        self.editButtonsHL.addWidget(self.fontSize_sp)
        
        # ================= Markdown Utilities ========================
        self.heading_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.heading_btn.setObjectName(mark_btn_id)
        # self.heading_btn.setStyleSheet(self.style_button)
        self.heading_btn.setMinimumHeight(25)
        self.editButtonsHL.addWidget(self.heading_btn)
        self.heading_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+'/bx-heading.svg')))
        self.heading_btn.setToolTip("Header text")
        
        self.bold_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.bold_btn.setObjectName(mark_btn_id)
        self.bold_btn.setMinimumHeight(25)
        # self.bold_btn.setStyleSheet(self.style_button)
        self.bold_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+'/bold.svg')))
        self.bold_btn.setToolTip("Bold text")
        self.editButtonsHL.addWidget(self.bold_btn)
        
        self.italic_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.italic_btn.setObjectName(mark_btn_id)
        # self.italic_btn.setStyleSheet(self.style_button)
        self.italic_btn.setMinimumHeight(25)
        self.italic_btn.setMinimumWidth(15)
        self.italic_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+'/bx-italic.svg')))
        self.italic_btn.setToolTip("Italic Text")
        self.editButtonsHL.addWidget(self.italic_btn)
        
        self.quote_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.quote_btn.setObjectName(mark_btn_id)
        self.quote_btn.setStyleSheet("QPushButton{border-top: 1px solid black;border-bottom: 1px solid black;}QPushButton#mark-btn:hover{	border-top: 1px solid white;border-bottom: 1px solid white;}")
        self.quote_btn.setMinimumHeight(25)
        self.quote_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+'/bxs-quote-right.svg')))
        self.quote_btn.setToolTip("Block Quote")
        self.editButtonsHL.addWidget(self.quote_btn)
        
        self.link_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.link_btn.setObjectName(mark_btn_id)
        # self.link_btn.setStyleSheet(self.style_button)
        self.link_btn.setMinimumHeight(25)
        self.link_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+'/bx-link.svg')))
        self.link_btn.setToolTip("refer a link")
        self.editButtonsHL.addWidget(self.link_btn)
        
        self.unList_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.unList_btn.setObjectName(mark_btn_id)
        # self.unList_btn.setStyleSheet(self.style_button)
        self.unList_btn.setMinimumHeight(25)
        icon = QtGui.QIcon(resource_path('resources/icons_svg/menu.png'))
        pixmap = icon.pixmap(QtCore.QSize(100, 100))
        pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) # Redimensiona a imagem
        self.unList_btn.setIcon(QtGui.QIcon(pixmap))
        self.unList_btn.setToolTip("Unordered List")
        self.editButtonsHL.addWidget(self.unList_btn)

        self.nList_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.nList_btn.setObjectName(mark_btn_id)
        # self.nList_btn.setStyleSheet(self.style_button)
        self.nList_btn.setMinimumHeight(25)
        icon = QtGui.QIcon(resource_path('resources/icons_svg/number.png'))
        pixmap = icon.pixmap(QtCore.QSize(100, 100))
        pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) # Redimensiona a imagem
        self.nList_btn.setIcon(QtGui.QIcon(pixmap))
        self.nList_btn.setText("")
        self.nList_btn.setToolTip("Numbered List")
        self.editButtonsHL.addWidget(self.nList_btn)
        
        self.taskList_btn = QtWidgets.QPushButton(self.buttons_frame)
        self.taskList_btn.setObjectName(mark_btn_id)
        # self.taskList_btn.setStyleSheet(self.style_button)
        self.taskList_btn.setMinimumHeight(25)
        icon = QtGui.QIcon(resource_path('resources/icons_svg/check_2.png'))
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
        self.tab_widget.setMinimumHeight(200)
        self.tab_widget.setMaximumHeight(350)
        self.splitter = QSplitter(QtCore.Qt.Vertical)
        self.splitter.setObjectName("mainSplitter")
        self.splitter.setStyleSheet(style_splitter)
        self.editArea = QtWidgets.QTextEdit() #TextEditWithLineNumbers()
        # self.editArea.setStyleSheet("background-color: #DCDCDC; color: #000000;")
        # self.editArea.setObjectName("editArea")
        font = QFont()
        font.setPointSize(16)
        self.splitter.addWidget(self.tab_widget)

        #========================================= adding splitter to centralVL
        self.centralVL.addWidget(self.splitter)
        
        # self.previewArea = QWebEngineView()
        self.previewArea2 = QTextBrowser()
        self.previewArea2.setMinimumHeight(150)
        self.previewArea2.setMaximumHeight(350)
        self.previewArea2.setStyleSheet(style_text_browse)
        self.previewArea2.setObjectName("previewArea2")
        self.previewArea2.setObjectName("previewArea2")
        # self.previewArea.setContentsMargins(5,5,5,5)
        # self.previewArea.setFocusPolicy(Qt.StrongFocus)
        # self.previewArea.setStyleSheet(self.style_preview)
        # self.previewArea.setContextMenuPolicy(QtCore.Qt.NoContextMenu) # Desabilita menu de contexto. 0=Qt.NoContextMenu
        #self.previewArea.loadFinished.connect(self.scroll_to_bottom)
        #========================================= adding previewArea to splitter
        # self.splitter.addWidget(self.previewArea)
        self.splitter.addWidget(self.previewArea2)
        self.centralwidget.installEventFilter(MainWindow)
        # self.previewArea.installEventFilter(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.content_widget = self.splitter

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        # self.statusbar.setStyleSheet("background-color: #dfe2e5;")
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
    
    #================ Dinamicidade UI
    def swapWidgetOnSplitter(self):
        # Obtém os índices atuais dos widgets no splitter
        index_tabWidget = self.splitter.indexOf(self.tab_widget)
        index_preview_area = self.splitter.indexOf(self.previewArea2)
        # print(index_tabWidget, "wid_1", sep="|")
        # print(index_preview_area, "wid_2", sep="|")
        if index_tabWidget < index_preview_area:
            # Remove os widgets temporariamente
            self.splitter.widget(index_tabWidget).setParent(None)
            self.splitter.widget(index_preview_area-1).setParent(None)
            # Adiciona os widgets de volta em ordem trocada
            self.splitter.insertWidget(index_tabWidget, self.previewArea2)
            self.splitter.insertWidget(index_preview_area, self.tab_widget)
        else:
            self.splitter.widget(index_tabWidget-1).setParent(None)
            self.splitter.widget(index_preview_area).setParent(None)  
            # Adiciona os widgets de volta em ordem trocada
            self.splitter.insertWidget(index_tabWidget, self.previewArea2)
            self.splitter.insertWidget(index_preview_area, self.tab_widget)
    
    def toggle_splitter_orientation(self):
            # Alterna a orientação do splitter entre horizontal e vertical
            if self.splitter.orientation() == QtCore.Qt.Horizontal:
                self.splitter.setOrientation(QtCore.Qt.Vertical)
            else:
                self.splitter.setOrientation(QtCore.Qt.Horizontal)
                self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

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
