import sys

from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow
)


# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 600, 450)
        self.border_size = 6

        self.installEventFilter(self)

    def update_title(self, new_title: str):
        """
        Atualiza o texto do título na barra de título.

        @param new_title: Novo texto para o título da janela.
        """
        self.title_label.setText(new_title)

    def set_content_layout(self, new_layout):
        """
        Substitui o layout do content_widget pelo novo_layout.
        """
        self.content_layout = new_layout
        current_layout = self.content_widget.layout()
        if current_layout is not None:
            current_layout.deleteLater()

        self.content_widget.setLayout(new_layout)

        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(0)

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def get_edge(self, pos: QPoint):
        rect = self.rect()
        left = pos.x() < self.border_size
        top = pos.y() < self.border_size
        right = pos.x() > rect.width() - self.border_size
        bottom = pos.y() > rect.height() - self.border_size

        # if top and left: return Qt.TopEdge | Qt.LeftEdge
        if top and right: return Qt.TopEdge | Qt.RightEdge
        if bottom and left: return Qt.BottomEdge | Qt.LeftEdge
        if bottom and right: return Qt.BottomEdge | Qt.RightEdge
        if left: return Qt.LeftEdge
        # if top: return Qt.TopEdge
        if right: return Qt.RightEdge
        if bottom: return Qt.BottomEdge
        return None

    def eventFilter(self, watched_object, event):
        obj_name = watched_object.objectName() or "QMainWindow"

        if event.type() == QEvent.Type.MouseMove:
            global_pos = event.globalPosition().toPoint()
            pos_na_janela = self.mapFromGlobal(global_pos)

            edge = self.get_edge(pos_na_janela)
            if edge:
                if edge == (Qt.TopEdge | Qt.LeftEdge) or edge == (Qt.BottomEdge | Qt.RightEdge):
                    self.setCursor(Qt.SizeFDiagCursor)
                elif edge == (Qt.TopEdge | Qt.RightEdge) or edge == (Qt.BottomEdge | Qt.LeftEdge):
                    self.setCursor(Qt.SizeBDiagCursor)
                elif edge == Qt.LeftEdge or edge == Qt.RightEdge:
                    self.setCursor(Qt.SizeHorCursor)
                else:
                    self.setCursor(Qt.SizeVerCursor)
            else:
                self.unsetCursor()

        elif event.type() == QEvent.Type.Leave:
            # logging.info(f"Mouse saiu do widget {obj_name}. Restaurando cursor.")
            self.unsetCursor()

        elif event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                global_pos = event.globalPosition().toPoint()
                pos_na_janela = self.mapFromGlobal(global_pos)
                edge = self.get_edge(pos_na_janela)

                if edge:
                    self.windowHandle().startSystemResize(edge)
                elif self.title_bar.rect().contains(self.title_bar.mapFromGlobal(global_pos)):
                    self.windowHandle().startSystemMove()

        return super().eventFilter(watched_object, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MainWindow()
    janela.show()
    sys.exit(app.exec())