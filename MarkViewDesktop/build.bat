@echo off
echo Starting Build mk.py with PyInstaller...
pyinstaller --noconsole --name DocViewer --icon="doc_icon.ico" --add-data "ui_docV.py;." --add-data "icons_svg/*;icons"  mk.py
echo Build complete. Press any key to exit.

