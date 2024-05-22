from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MongoTask()
        self.ui.setupUi(self)
        self.setWindowTitle("Botão com SVG")
        self.setGeometry(100, 100, 300, 200)

        button = QPushButton(self)
        button.setGeometry(100, 70, 100, 50)
        button.setToolTip("Heading")
        # Carregar o arquivo SVG
        svg_renderer = QSvgRenderer("svg/bx-heading.svg")

        # Renderizar o SVG em um QPixmap
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)  # Tornar o fundo transparente
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()

        # Definir o ícone do botão
        button.setIcon(QIcon(pixmap))
        button.setIconSize(pixmap.rect().size())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
