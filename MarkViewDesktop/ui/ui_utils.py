from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer


def loadSvgIconColored(file_path, width=80, height=80, color=None):
    svg_renderer = QSvgRenderer(file_path)
    if not svg_renderer.isValid():
        raise ValueError(f"Arquivo SVG inválido: {file_path}")

    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)  # Fundo transparente
    painter = QPainter(pixmap)

    # Renderiza o SVG normalmente primeiro
    svg_renderer.render(painter)

    # Aplicar cor se fornecida
    if color is not None:
        if isinstance(color, str):
            color = QColor(color)  # Converte string (ex.: "#FF0000") para QColor
        elif not isinstance(color, QColor):
            raise ValueError("O parâmetro 'color' deve ser uma string (ex.: '#FF0000') ou um QColor")
        #
        # # Define o modo de composição para aplicar a cor apenas nas áreas preenchidas do SVG
        # painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        # painter.setBrush(QColor(color))  # Define a cor como pincel
        # painter.setPen(Qt.NoPen)  # Remove contornos para evitar linhas indesejadas
        # painter.drawRect(pixmap.rect())  # Aplica a cor às áreas do SVG
    else:
        color = QColor('#ffffff')
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.setBrush(QColor(color))
    painter.setPen(Qt.NoPen)
    painter.drawRect(pixmap.rect())
    painter.end()
    return pixmap