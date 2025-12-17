import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer

def loadSvgIconColored(file_path, width=80, height=80, color=None):
    svg_renderer = QSvgRenderer(file_path)
    if not svg_renderer.isValid():
        raise ValueError(f"Arquivo SVG inválido: {file_path}")

    pixmap = QPixmap(width, height)
    # Usa QColor transparente explicitamente para evitar avisos estáticos sobre Qt.transparent
    pixmap.fill(QColor(0, 0, 0, 0))  # Fundo transparente
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

    # Resolver dinamicamente o modo de composição (evita referências estaticamente problemáticas)
    comp_mode = getattr(QPainter, 'CompositionMode_SourceIn', None)
    if comp_mode is None:
        comp_enum = getattr(QPainter, 'CompositionMode', None)
        if comp_enum is not None and hasattr(comp_enum, 'SourceIn'):
            comp_mode = getattr(comp_enum, 'SourceIn')

    if comp_mode is not None:
        painter.setCompositionMode(comp_mode)

    # Resolver dinamicamente NoPen (compatível com variações do Qt)
    no_pen = None
    pen_style = getattr(Qt, 'PenStyle', None)
    if pen_style is not None and hasattr(pen_style, 'NoPen'):
        no_pen = getattr(pen_style, 'NoPen')
    elif hasattr(Qt, 'NoPen'):
        no_pen = getattr(Qt, 'NoPen')

    if no_pen is not None:
        painter.setPen(no_pen)

    painter.setBrush(QColor(color))
    painter.drawRect(pixmap.rect())
    painter.end()
    return pixmap

def loadSvgIcon(file_path, width=80, height=80):
    svg_renderer = QSvgRenderer(file_path)
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()
    return pixmap

def resource_path(relative_path: str) -> str:
    """Obtém o caminho absoluto do recurso."""
    if hasattr(sys, "_MEIPASS"):
        # quando rodando no executável do PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

