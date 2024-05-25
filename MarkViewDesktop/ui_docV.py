from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QSplitter, QLabel, QSpinBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QTextCursor
from PyQt5.QtSvg import QSvgRenderer


def loadSvgIcon(file_path, width=80, height=80):
    svg_renderer = QSvgRenderer(file_path)
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)
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
        
        border-radius: 4px; /* Borda arredondada */
    """

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
        MainWindow.resize(539, 307)
        MainWindow.setStyleSheet("background-color: rgb(117, 117, 117); border-radius:12px;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Create the input frame with buttons
        self.frame_input = QtWidgets.QFrame(self.centralwidget)
        self.frame_input.setStyleSheet("background-color: rgb(117, 117, 117);")
        self.frame_input.setObjectName("frame_input")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_input)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSpacing(10)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        # ============================================
        self.fontSize_sp = QSpinBox(self.frame_input)
        self.fontSize_sp.setStyleSheet(self.style_utils)
        self.fontSize_sp.setToolTip("Tamanho do texto")
        self.fontSize_sp.setRange(8, 72)  # Define o intervalo do tamanho da fonte
        self.fontSize_sp.setValue(16)  # Define o valor padrão
        self.fontSize_sp.valueChanged.connect(self.update_font_size)  # Conecta a mudança de valor ao método

        self.fontStyle_cb = QComboBox(self.frame_input)
        self.fontStyle_cb.setToolTip("Tamanho do texto")
        self.fontStyle_cb.setStyleSheet(self.style_utils)
        self.fontStyle_cb.addItems(["Arial", "Courier New", "Times New Roman"])
        self.fontStyle_cb.currentIndexChanged.connect(self.update_font_style)
        self.horizontalLayout.addWidget(self.fontStyle_cb)
        self.horizontalLayout.addWidget(self.fontSize_sp)
        # ====================================================
        
        self.heading_btn = QtWidgets.QPushButton(self.frame_input)
        self.heading_btn.setObjectName("heading_btn")
        self.heading_btn.setStyleSheet(self.style_button)
        self.heading_btn.setMinimumHeight(25)
        self.horizontalLayout.addWidget(self.heading_btn)
        self.heading_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+"bx-heading.svg")))
        self.heading_btn.setToolTip("Header text")
        
        self.bold_btn = QtWidgets.QPushButton(self.frame_input)
        self.bold_btn.setObjectName("bold_btn")
        self.bold_btn.setMinimumHeight(25)
        self.bold_btn.setStyleSheet(self.style_button)
        self.bold_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+"bold.svg")))
        self.bold_btn.setToolTip("Bold text")
        self.horizontalLayout.addWidget(self.bold_btn)
        
        self.italic_btn = QtWidgets.QPushButton(self.frame_input)
        self.italic_btn.setObjectName("italic_btn")
        self.italic_btn.setStyleSheet(self.style_button)
        self.italic_btn.setMinimumHeight(25)
        self.italic_btn.setMinimumWidth(15)
        self.italic_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+"bx-italic.svg")))
        self.italic_btn.setToolTip("Italic Text")
        self.horizontalLayout.addWidget(self.italic_btn)
        
        self.quote_btn = QtWidgets.QPushButton(self.frame_input)
        self.quote_btn.setObjectName("quote_btn")
        self.quote_btn.setStyleSheet(self.style_button)
        self.quote_btn.setMinimumHeight(25)
        self.quote_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+"bxs-quote-right.svg")))
        self.quote_btn.setToolTip("Block Quote")
        self.horizontalLayout.addWidget(self.quote_btn)
        
        self.link_btn = QtWidgets.QPushButton(self.frame_input)
        self.link_btn.setObjectName("link_btn")
        self.link_btn.setStyleSheet(self.style_button)
        self.link_btn.setMinimumHeight(25)
        self.link_btn.setIcon(QIcon(loadSvgIcon(self.iconspath+"bx-link.svg")))
        self.link_btn.setToolTip("refer a link")
        self.horizontalLayout.addWidget(self.link_btn)
        
        self.unList_btn = QtWidgets.QPushButton(self.frame_input)
        self.unList_btn.setObjectName("unList_btn")
        self.unList_btn.setStyleSheet(self.style_button)
        self.unList_btn.setMinimumHeight(25)
        icon = QtGui.QIcon(self.iconspath+"menu.png")
        pixmap = icon.pixmap(QtCore.QSize(100, 100))
        pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) # Redimensiona a imagem
        self.unList_btn.setIcon(QtGui.QIcon(pixmap))
        self.unList_btn.setToolTip("Unordered List")
        self.horizontalLayout.addWidget(self.unList_btn)
        
        self.nList_btn = QtWidgets.QPushButton(self.frame_input)
        self.nList_btn.setObjectName("nList_btn")
        self.nList_btn.setStyleSheet(self.style_button)
        self.nList_btn.setMinimumHeight(25)
        icon = QtGui.QIcon(self.iconspath+"number.png")
        pixmap = icon.pixmap(QtCore.QSize(100, 100))
        pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) # Redimensiona a imagem
        self.nList_btn.setIcon(QtGui.QIcon(pixmap))
        self.nList_btn.setText("")
        self.nList_btn.setToolTip("Numbered List")
        self.horizontalLayout.addWidget(self.nList_btn)
        
        self.taskList_btn = QtWidgets.QPushButton(self.frame_input)
        self.taskList_btn.setObjectName("taskList_btn")
        self.taskList_btn.setStyleSheet(self.style_button)
        self.taskList_btn.setMinimumHeight(25)
        icon = QtGui.QIcon(self.iconspath+"check_2.png")
        pixmap = icon.pixmap(QtCore.QSize(100, 100))
        pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.taskList_btn.setIcon(QtGui.QIcon(pixmap))
        self.taskList_btn.setToolTip("Task List")
        self.horizontalLayout.addWidget(self.taskList_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Add the input frame with buttons to the main layout
        self.verticalLayout_2.addWidget(self.frame_input)

        # Create the edit area and add it to the splitter
        self.splitter = QSplitter(Qt.Vertical)
        self.editArea = QtWidgets.QTextEdit(self.centralwidget)
        self.editArea.setStyleSheet("background-color: #DCDCDC;")
        self.editArea.setObjectName("editArea")
        font = QFont()
        font.setPointSize(16)
        self.editArea.setFont(font)
        self.splitter.addWidget(self.editArea)

        # Add the splitter to the main layout
        self.verticalLayout_2.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 539, 22))
        self.menubar.setStyleSheet("background-color: #dfe2e5;")
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        self.statusbar.setStyleSheet("background-color: #dfe2e5;")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

        self.heading_btn.clicked.connect(self.addHeader)
        self.bold_btn.clicked.connect(self.addBold)
        self.italic_btn.clicked.connect(self.addItalic)
        self.quote_btn.clicked.connect(self.addQuote)
        self.link_btn.clicked.connect(self.addLink)
        self.unList_btn.clicked.connect(self.addUnList)
        self.nList_btn.clicked.connect(self.addNList)
        self.taskList_btn.clicked.connect(self.addTaskList)

    def statusBarMessage(self, texto:str):
        label = QLabel(texto)
        label.setAlignment(Qt.AlignCenter)  # Centralizar o texto no rótulo

        # Adicionar o rótulo à barra de status
        self.statusbar.addWidget(label)

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
