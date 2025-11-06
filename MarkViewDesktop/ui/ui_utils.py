from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer

# Importa as novas classes de estilo (mantém compatibilidade com nomes antigos abaixo)
from .styles import ButtonStyles, ComboStyles, CloseButtonStyles, MiscStyles


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

# Expor identificador de botão (compatibilidade)
mark_btn_id = ButtonStyles.mark_btn_id

# Mapear as antigas variáveis de estilo para as novas classes
style_button2 = ButtonStyles.style_button2
style_button = ButtonStyles.style_button
style_utils = ComboStyles.style_utils
style_closeBTN = CloseButtonStyles.style_closeBTN
style_m_M = MiscStyles.btn_max_min
style_splitter = MiscStyles.style_splitter
style_preview = MiscStyles.style_preview
style_text_edit = MiscStyles.style_text_edit
style_text_browse = MiscStyles.style_text_browse
style_combo_box = MiscStyles.combo_box
style_spin_box = MiscStyles.spin_box
