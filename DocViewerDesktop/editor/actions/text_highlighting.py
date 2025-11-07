# from PySide6.QtWidgets import QTextEdit, QApplication
# from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
# from PySide6.QtCore import QRegularExpression
# import re
# import sys
#
#
# class MarkdownHighlighter(QSyntaxHighlighter):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         self.highlighting_rules = []
#
#         # Formatos
#         bold_format = QTextCharFormat()
#         bold_format.setFontWeight(QFont.Bold)
#         bold_format.setForeground(QColor("#070dc9"))
#
#         italic_format = QTextCharFormat()
#         italic_format.setFontItalic(True)
#         italic_format.setForeground(QColor("#32cd32"))
#
#         header_format = QTextCharFormat()
#         header_format.setFontWeight(QFont.Bold)
#         header_format.setForeground(QColor("#070dc9"))
#         header_format.setFontPointSize(14)
#
#         code_format = QTextCharFormat()
#         code_format.setBackground(QColor("#c6acac"))
#         code_format.setForeground(QColor("#333333"))
#         code_format.setFont(QFont("Consolas", 10))
#
#         link_format = QTextCharFormat()
#         link_format.setForeground(QColor("#0000ee"))
#         link_format.setFontUnderline(True)
#
#         list_format = QTextCharFormat()
#         list_format.setForeground(QColor("#8a2be2"))
#
#         blockquote_format = QTextCharFormat()
#         blockquote_format.setForeground(QColor("#000000"))
#         blockquote_format.setFontItalic(True)
#
#         # Regras de destaque
#         # Cabeçalhos (#, ##, ###)
#         header_pattern = QRegularExpression("^#{1,6}\\s.+")
#         self.highlighting_rules.append((header_pattern, header_format))
#
#         # Negrito (**texto** ou __texto__)
#         bold_pattern1 = QRegularExpression("\\*\\*(.*?)\\*\\*")
#         bold_pattern2 = QRegularExpression("__(.*?)__")
#         self.highlighting_rules.extend([
#             (bold_pattern1, bold_format),
#             (bold_pattern2, bold_format),
#         ])
#
#         # Itálico (*texto* ou _texto_)
#         italic_pattern1 = QRegularExpression("(^|[^\\*])\\*(?![\\*\\s])(.+?)(?<![\\*\\s])\\*($|[^\\*])")
#         italic_pattern2 = QRegularExpression("(^|[^_])_(?!_[\\s])(.+?)(?<![_\\s])_($|[^_])")
#         self.highlighting_rules.extend([
#             (italic_pattern1, italic_format),
#             (italic_pattern2, italic_format),
#         ])
#
#         # Código inline (`codigo`)
#         code_pattern = QRegularExpression("`(.*?)`")
#         self.highlighting_rules.append((code_pattern, code_format))
#
#         # Links [texto](url)
#         link_pattern = QRegularExpression("\\[([^\\]]+)\\]\\(([^)]+)\\)")
#         self.highlighting_rules.append((link_pattern, link_format))
#
#         # Listas (- item ou * item ou 1. item)
#         list_pattern = QRegularExpression("^\\s*[\\*\\-\\+]\\s|^\\s*\\d+\\.\\s")
#         self.highlighting_rules.append((list_pattern, list_format))
#
#         # Blockquote (> texto)
#         blockquote_pattern = QRegularExpression("^>\\s?.+")
#         self.highlighting_rules.append((blockquote_pattern, blockquote_format))
#
#     def highlightBlock(self, text):
#         for pattern, format in self.highlighting_rules:
#             expression = pattern
#             match_iterator = expression.globalMatch(text)
#             while match_iterator.hasNext():
#                 match = match_iterator.next()
#                 self.setFormat(match.capturedStart(), match.capturedLength(), format)
#
#         # Blocos de código com ``` (multi-linha)
#         self.highlight_code_blocks(text)
#
#     def highlight_code_blocks(self, text):
#         code_block_pattern = QRegularExpression("```[\\s\\S]*?```")
#         match_iterator = code_block_pattern.globalMatch(text)
#         code_format = QTextCharFormat()
#         code_format.setBackground(QColor("#f4f4f4"))
#         code_format.setForeground(QColor("#333333"))
#         code_format.setFont(QFont("Consolas", 10))
#
#         while match_iterator.hasNext():
#             match = match_iterator.next()
#             self.setFormat(match.capturedStart(), match.capturedLength(), code_format)
#
#
# # Exemplo de uso
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#
#     editor = QTextEdit()
#     editor.setPlainText("""# Título Principal
#
# ## Subtítulo
#
# Este é um texto com **negrito** e *itálico*.
#
# - Item da lista
# - Outro item
#   - Subitem
#
# > Esta é uma citação.
#
# Link: [Google](https://google.com)
#
# Código inline: `print("Olá")`
#
# ```python
# def exemplo():
#     return "Bloco de código"
# ```
# """)
#
#     highlighter = MarkdownHighlighter(editor.document())
#     editor.resize(600, 400)
#     editor.show()
#
#     sys.exit(app.exec())

from PySide6.QtWidgets import QTextEdit, QApplication
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PySide6.QtCore import QRegularExpression, Qt
import sys


class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlighting_rules = []
        self.code_block_rules = {}  # Dicionário para regras por linguagem

        # === Formatos gerais do Markdown ===
        self.setup_markdown_formats()
        self.setup_markdown_rules()

        # === Regras para código dentro de blocos ```
        self.setup_python_highlighting()

    def setup_markdown_formats(self):
        # Negrito
        self.bold_format = QTextCharFormat()
        self.bold_format.setFontWeight(QFont.Bold)
        self.bold_format.setForeground(QColor("#1e90ff"))

        # Itálico
        self.italic_format = QTextCharFormat()
        self.italic_format.setFontItalic(True)
        self.italic_format.setForeground(QColor("#32cd32"))

        # Cabeçalhos
        self.header_format = QTextCharFormat()
        self.header_format.setFontWeight(QFont.Bold)
        self.header_format.setForeground(QColor("#ff6347"))
        self.header_format.setFontPointSize(14)

        # Código inline
        self.code_format = QTextCharFormat()
        self.code_format.setBackground(QColor("#f0f0f0"))
        self.code_format.setForeground(QColor("#333333"))
        self.code_format.setFont(QFont("Consolas", 10))

        # Link
        self.link_format = QTextCharFormat()
        self.link_format.setForeground(QColor("#0000ee"))
        self.link_format.setFontUnderline(True)

        # Lista
        self.list_format = QTextCharFormat()
        self.list_format.setForeground(QColor("#8a2be2"))

        # Blockquote
        self.blockquote_format = QTextCharFormat()
        self.blockquote_format.setForeground(QColor("#666666"))
        self.blockquote_format.setFontItalic(True)

        # Fundo do bloco de código
        self.code_block_bg = QTextCharFormat()
        self.code_block_bg.setBackground(QColor("#f4f4f4"))
        self.code_block_bg.setForeground(QColor("#333333"))
        self.code_block_bg.setFont(QFont("Consolas", 10))

    def setup_markdown_rules(self):
        # Cabeçalhos
        self.highlighting_rules.append((QRegularExpression("^#{1,6}\\s.+"), self.header_format))

        # Negrito
        self.highlighting_rules.extend([
            (QRegularExpression("\\*\\*(.*?)\\*\\*"), self.bold_format),
            (QRegularExpression("__(.*?)__"), self.bold_format),
        ])

        # Itálico (evita conflito com *)
        self.highlighting_rules.extend([
            (QRegularExpression("(^|[^\\*])\\*(?![\\*\\s])(.+?)(?<![\\*\\s])\\*($|[^\\*])"), self.italic_format),
            (QRegularExpression("(^|[^_])_(?!_[\\s])(.+?)(?<![_\\s])_($|[^_])"), self.italic_format),
        ])

        # Código inline
        self.highlighting_rules.append((QRegularExpression("`(.*?)`"), self.code_format))

        # Links
        self.highlighting_rules.append((QRegularExpression("\\[([^\\]]+)\\]\\(([^)]+)\\)"), self.link_format))

        # Listas
        self.highlighting_rules.append((QRegularExpression("^\\s*[\\*\\-\\+]\\s|^\\s*\\d+\\.\\s"), self.list_format))

        # Blockquote
        self.highlighting_rules.append((QRegularExpression("^>\\s?.+"), self.blockquote_format))

    def setup_python_highlighting(self):
        # Palavras-chave do Python
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000ff"))
        keyword_format.setFontWeight(QFont.Bold)

        keywords = [
            "def", "class", "return", "if", "else", "elif", "for", "while",
            "try", "except", "finally", "with", "import", "from", "as",
            "lambda", "and", "or", "not", "in", "is", "None", "True", "False"
        ]

        self.code_block_rules["python"] = []
        for word in keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            self.code_block_rules["python"].append((pattern, keyword_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#008000"))
        self.code_block_rules["python"].extend([
            (QRegularExpression('".*?"'), string_format),
            (QRegularExpression("'.*?'"), string_format),
            (QRegularExpression('"""[\s\S]*?"""'), string_format),
            (QRegularExpression("'''[\s\S]*?'''"), string_format),
        ])

        # Números
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#ff4500"))
        self.code_block_rules["python"].append((QRegularExpression("\\b\\d+\\.?\\d*\\b"), number_format))

        # Comentários
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#808080"))
        self.code_block_rules["python"].append((QRegularExpression("#.*"), comment_format))

    def highlightBlock(self, text):
        # Aplica regras gerais do Markdown
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

        # Detecta e destaca blocos de código com linguagem
        self.highlight_fenced_code_blocks(text)

    def highlight_fenced_code_blocks(self, text):
        # Padrão para ```language ... ```
        fenced_pattern = QRegularExpression("```(\\w*)\\n([\\s\\S]*?)```")
        match_iterator = fenced_pattern.globalMatch(text)

        while match_iterator.hasNext():
            match = match_iterator.next()
            lang = match.captured(1).strip().lower()
            code_start = match.capturedStart(2)
            code_length = match.capturedLength(2)

            # Aplica fundo ao bloco inteiro
            self.setFormat(match.capturedStart(), match.capturedLength(), self.code_block_bg)

            # Se for Python, aplica destaque interno
            if lang == "python" and lang in self.code_block_rules:
                code_text = match.captured(2)
                # Reaplica o fundo no código (por segurança)
                self.setFormat(code_start, code_length, self.code_block_bg)

                # Aplica regras de Python
                for pattern, fmt in self.code_block_rules["python"]:
                    code_match_iterator = pattern.globalMatch(code_text)
                    while code_match_iterator.hasNext():
                        code_match = code_match_iterator.next()
                        start = code_start + code_match.capturedStart()
                        length = code_match.capturedLength()
                        self.setFormat(start, length, fmt)


# === Exemplo de uso ===
if __name__ == "__main__":
    app = QApplication(sys.argv)

    editor = QTextEdit()
    editor.setPlainText("""# Exemplo com Python

Aqui um bloco de código:

```python
def exemplo():
    nome = "Mundo"
    return f"Olá, {nome}!"

print(exemplo())  # Comentário
                        ```
                        """)

