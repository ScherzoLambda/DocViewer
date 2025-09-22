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

mark_btn_id = "mark-btn"
style_button = """
QToolTip,QPushButton {
     /* Cor de fundo padrão */
    border: 2px solid #161b22; /* Borda */
    color: white; /* Cor do texto */

    /* border-radius: 4px; Borda arredondada */
}
QPushButton:hover {
    background-color: #DCDCDC; /* Cor de fundo quando o mouse está sobre o botão */
}
QFrame, QLabel {
border: 1px solid transparent;
}
"""
style_utils = """
    QComboBox
    {
        background-color: #1C1C1C;
        color: #FFFFFF;
        border: 1px solid #666666;
    }
    QComboBox:hover
    {
        border: 1px solid #3399FF;
    }
    QComboBox QAbstractItemView::item:hover {
        border: 1px solid #3399FF;
        background-color: #8C8C8C;
    }
    /*QComboBox QAbstractItemView {
        border: 1px solid #3399FF;
        border-radius: 6px;
        background-color: #2b2b2b;
        selection-background-color: #3399ff;
        selection-color: #3399ff;
        padding: 5px; /* Espaçamento interno da lista */
    }*/
"""
style_closeBTN = """
QPushButton {
    border: none;
    background-color: transparent;
    border: 1px solid #f4696b;
}
QPushButton:hover {
    background-color: #f4696b;  /* cor de fundo*/
}
"""
style_m_M = """
QPushButton {
    font-size: 18px;
    color: #000000;
    border: 1px solid #007BFF;
    border-radius: 4px;
    font-weight: bold;
    background-color: transparent;
}
QPushButton:hover {
    background-color: #55AAFF; /* Lighter accent on hover */
    border-color: #3399FF;  
}
"""
style_splitter = """
QSplitter::handle {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #333333, stop: 1 #444444);
    border: 1px solid #666666;
    height: 15px;
    border-radius: 4px;
}

QSplitter::handle:hover {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #444444, stop: 1 #555555);
}
"""
style_preview = """
QWebEngineView {
    background-color: #2B2B2B;
    border: 1px solid #3399FF;
    border-radius: 4px;
}

QWebEngineView:focus {
    border: 1px solid #4F9EE3;
}
"""

style_text_edit = """
QTextEdit
{
	background-color: #1C1C1C;
	color: #FFFFFF;
	border: 1px solid #666666;
	border-radius: 4px;
}
QTextEdit:focus{ border: 1px solid #3399FF}
"""

style_text_browse = """
QTextBrowser {
    border-radius: 4px;
    border: 1px solid #555555;
    border-left: none;
	border-right: none;
}
"""