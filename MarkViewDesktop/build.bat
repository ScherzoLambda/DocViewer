@echo off
echo Starting Build DocViewer with PyInstaller...
pyinstaller --noconsole --name DocViewer --icon="doc_icon.ico" --add-data "ui_docV.py;." --add-data "icons_svg/*;icons"  main.py
echo Build complete. Press any key to exit.

