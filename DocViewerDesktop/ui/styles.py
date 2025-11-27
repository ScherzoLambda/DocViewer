from .ui_utils import resource_path

class ButtonStyles:
    """Estilos relacionados a botões"""
    mark_btn_id = "mark-btn"

    style_button2 = """
    QPushButton{
    border: 1px solid white;border-bottom: 1px solid white;}
    QPushButton#mark-btn:hover{\tborder: 1px solid black;border-bottom: 1px solid black;}
    """

    style_button = """
    QToolTip,QPushButton {
         /* Cor de fundo padrão */
        border: 2px solid #161b22; /* Borda */
        color: white; /* Cor do texto */
    
        /* border-radius: 4px; Borda arredondada */
    }

    QFrame, QLabel {
    border: 1px solid transparent;
    }
    """

class ComboStyles:
    """Estilos relacionados a QComboBox / listas"""
    style_utils = """
    QComboBox
    {
        background-color: #1C1C1C;
        color: #FFFFFF;
        border: 1px solid white;
    }
    QComboBox:hover
    {
        border: 1px solid #3399FF;
    }
    QComboBox QAbstractItemView::item:hover {
        border: 1px solid #3399FF;
        background-color: #8C8C8C;
    }
    QComboBox QAbstractItemView {
        border: 1px solid #3399FF;
        border-radius: 6px;
        background-color: #2b2b2b;
        selection-background-color: #3399ff;
        selection-color: #3399ff;
        padding: 5px; /* Espaçamento interno da lista */
    }
    """

class CloseButtonStyles:
    """Estilos para o botão de fechar"""
    style_closeBTN = """
    QPushButton {
        border: none;
        background-color: transparent;
        border: 1px solid #f4696b;
    }
    QPushButton:hover {
        background-color: #f4696b;  /* cor de fundo*/
        border: 1px solid #f4696b;
    }
    """

class MiscStyles:
    """Outros estilos (splitter, preview, text edits, etc.)"""
    icons_path = resource_path("resources/icons_svg/")

    btn_max_min = """
    QPushButton {
        font-size: 18px;
        color: #000000;
        border: 1px solid #007BFF;
        border-radius: 4px;
        font-weight: bold;
        background-color: transparent;
    }
    QPushButton:hover {
        
        border-color: white;
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
    combo_box = """
    QComboBox {
        border: 1px solid white;
        border-radius: 4px;
    }
    """
    spin_box = f"""
    QSpinBox, 
    QDoubleSpinBox,
    QDateTimeEdit
    {{
        background-color: #000000;
        color: white;
        font-weight: bold;
        border: 1px solid #FFFFFF;
        padding : 4px;

    }}


    QSpinBox::disabled, 
    QDoubleSpinBox::disabled,
    QDateTimeEdit::disabled
    {{
        background-color: #404040;
        color: #656565;
        border-color: #051a39;

    }}


    QSpinBox:hover, 
    QDoubleSpinBox::hover,
    QDateTimeEdit::hover
    {{
        border: 1px solid #3399FF;

    }}


    QSpinBox::up-button, QSpinBox::down-button,
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button,
    QDateTimeEdit::up-button, QDateTimeEdit::down-button
    {{
        background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(135, 135, 135, 255),stop:1 rgba(170, 170, 170, 255));
        border: 0px solid #333333;
        color: #FFFFFF;

    }}


    QSpinBox::disabled, 
    QDoubleSpinBox::disabled,
    QDateTimeEdit::disabled
    {{
        background-color: #404040;
        color: #656565;
        border-color: #051a39;

    }}


    QSpinBox::up-button:hover, QSpinBox::down-button:hover,
    QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover,
    QDateTimeEdit::up-button:hover, QDateTimeEdit::down-button:hover
    {{
        background-color: #646464;
        border: 1px solid #333333;


    }}


    QSpinBox::up-button:disabled, QSpinBox::down-button:disabled,
    QDoubleSpinBox::up-button:disabled, QDoubleSpinBox::down-button:disabled,
    QDateTimeEdit::up-button:disabled, QDateTimeEdit::down-button:disabled
    {{
        background-color: #404040;
        color: #656565;
        border-color: #051a39;

    }}


    QSpinBox::up-button:pressed, QSpinBox::down-button:pressed,
    QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button::pressed,
    QDateTimeEdit::up-button:pressed, QDateTimeEdit::down-button::pressed
    {{
        background-color: #979796;
        border: 1px solid #444444;

    }}


    QSpinBox::down-arrow,
    QDoubleSpinBox::down-arrow,
    QDateTimeEdit::down-arrow
    {{
        image: url({icons_path}/down-arrow.svg);
        width: 7px;

    }}


    QSpinBox::up-arrow,
    QDoubleSpinBox::up-arrow,
    QDateTimeEdit::up-arrow
    {{
        image: url({icons_path}/up-arrow.svg);
        width: 7px;
        color: #3F75A8;
    }}

    """

__all__ = [
    "ButtonStyles",
    "ComboStyles",
    "CloseButtonStyles",
    "MiscStyles",
]

