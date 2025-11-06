pyinstaller --noconsole --name DocViewer \
  --icon="resources/icons_svg/favicon.ico" \
  --add-data "MarkViewDesktop/ui/dark-high-v0.qss:ui" \
  --add-data "MarkViewDesktop/resources/icons_svg/*:resources/icons_svg" \
  --hidden-import="ui.ui_utils" \
  --hidden-import="editor.editor_core" \
  --hidden-import="editor.actions.file_actions" \
  --hidden-import="editor.actions.edit_actions" \
  --exclude-module PySide6.Qt3DCore \
  --exclude-module PySide6.Qt3DRender \
  --exclude-module PySide6.Qt3DExtras \
  --exclude-module PySide6.QtDataVisualization \
  --exclude-module PySide6.QtCharts \
  --exclude-module PySide6.QtWebEngineWidgets \
  --strip \
  MarkViewDesktop/main.py