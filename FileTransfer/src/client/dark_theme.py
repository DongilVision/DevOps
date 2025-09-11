"""
다크 테마 스타일시트 정의
"""

DARK_STYLESHEET = """
/* 메인 윈도우 */
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

/* 중앙 위젯 */
QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9pt;
}

/* 그룹박스 */
QGroupBox {
    font-weight: bold;
    border: 2px solid #555555;
    border-radius: 8px;
    margin: 5px 0px;
    padding-top: 10px;
    background-color: #2d2d2d;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #ffffff;
    background-color: #2d2d2d;
}

/* 리스트 위젯 */
QListWidget {
    background-color: #252525;
    border: 1px solid #555555;
    border-radius: 4px;
    alternate-background-color: #2a2a2a;
    selection-background-color: #0078d4;
    selection-color: #ffffff;
    outline: none;
}

QListWidget::item {
    padding: 4px;
    border-bottom: 1px solid #333333;
    color: #ffffff;
}

QListWidget::item:selected {
    background-color: #0078d4;
    color: #ffffff;
}

QListWidget::item:hover {
    background-color: #404040;
}

/* 라벨 */
QLabel {
    color: #ffffff;
    background-color: transparent;
}

/* 버튼 */
QPushButton {
    background-color: #404040;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px 12px;
    color: #ffffff;
    font-weight: bold;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #505050;
    border-color: #777777;
}

QPushButton:pressed {
    background-color: #303030;
    border-color: #888888;
}

QPushButton:disabled {
    background-color: #2a2a2a;
    color: #666666;
    border-color: #444444;
}

/* 툴바 */
QToolBar {
    background-color: #2d2d2d;
    border: none;
    spacing: 4px;
    padding: 4px;
}

QToolBar QToolButton {
    background-color: #404040;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px 8px;
    color: #ffffff;
    margin: 1px;
}

QToolBar QToolButton:hover {
    background-color: #505050;
    border-color: #777777;
}

QToolBar QToolButton:pressed {
    background-color: #303030;
}

QToolBar QToolButton:disabled {
    background-color: #2a2a2a;
    color: #666666;
    border-color: #444444;
}

/* 메뉴바 */
QMenuBar {
    background-color: #2d2d2d;
    color: #ffffff;
    border-bottom: 1px solid #555555;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #404040;
    border-radius: 4px;
}

QMenu {
    background-color: #2d2d2d;
    border: 1px solid #555555;
    border-radius: 4px;
    color: #ffffff;
}

QMenu::item {
    padding: 4px 20px;
    border-radius: 4px;
    margin: 1px;
}

QMenu::item:selected {
    background-color: #0078d4;
}

QMenu::separator {
    height: 1px;
    background-color: #555555;
    margin: 4px 0px;
}

/* 상태바 */
QStatusBar {
    background-color: #2d2d2d;
    color: #ffffff;
    border-top: 1px solid #555555;
}

/* 스플리터 */
QSplitter::handle {
    background-color: #555555;
}

QSplitter::handle:horizontal {
    width: 3px;
}

QSplitter::handle:vertical {
    height: 3px;
}

/* 진행률 바 */
QProgressBar {
    border: 1px solid #555555;
    border-radius: 4px;
    background-color: #252525;
    text-align: center;
    color: #ffffff;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}

/* 스크롤바 */
QScrollBar:vertical {
    background-color: #2d2d2d;
    width: 16px;
    border-radius: 8px;
}

QScrollBar::handle:vertical {
    background-color: #555555;
    border-radius: 8px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #666666;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QScrollBar:horizontal {
    background-color: #2d2d2d;
    height: 16px;
    border-radius: 8px;
}

QScrollBar::handle:horizontal {
    background-color: #555555;
    border-radius: 8px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #666666;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
}

/* 체크박스와 라디오버튼 */
QCheckBox, QRadioButton {
    color: #ffffff;
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator {
    border: 2px solid #555555;
    border-radius: 3px;
    background-color: #252525;
}

QCheckBox::indicator:checked {
    background-color: #0078d4;
    border-color: #0078d4;
}

QRadioButton::indicator {
    border: 2px solid #555555;
    border-radius: 8px;
    background-color: #252525;
}

QRadioButton::indicator:checked {
    background-color: #0078d4;
    border-color: #0078d4;
}

/* 텍스트 입력 */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #252525;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px;
    color: #ffffff;
    selection-background-color: #0078d4;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #0078d4;
}

/* 스핀박스 */
QSpinBox, QDoubleSpinBox {
    background-color: #252525;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px;
    color: #ffffff;
}

QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #555555;
    background-color: #404040;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border-left: 1px solid #555555;
    background-color: #404040;
}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 4px solid #ffffff;
}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid #ffffff;
}

/* 콤보박스 */
QComboBox {
    background-color: #252525;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px;
    color: #ffffff;
    min-width: 6em;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #555555;
    background-color: #404040;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid #ffffff;
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    border: 1px solid #555555;
    selection-background-color: #0078d4;
    color: #ffffff;
}

/* 탭 위젯 */
QTabWidget::pane {
    border: 1px solid #555555;
    background-color: #2d2d2d;
}

QTabBar::tab {
    background-color: #404040;
    border: 1px solid #555555;
    padding: 6px 12px;
    color: #ffffff;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #0078d4;
    border-bottom: 1px solid #0078d4;
}

QTabBar::tab:hover {
    background-color: #505050;
}

/* 테이블 위젯 */
QTableWidget, QTreeWidget {
    background-color: #252525;
    alternate-background-color: #2a2a2a;
    gridline-color: #555555;
    selection-background-color: #0078d4;
    color: #ffffff;
    border: 1px solid #555555;
}

QHeaderView::section {
    background-color: #404040;
    color: #ffffff;
    padding: 4px;
    border: 1px solid #555555;
    font-weight: bold;
}

/* 다이얼로그 */
QDialog {
    background-color: #1e1e1e;
    color: #ffffff;
}

QDialogButtonBox QPushButton {
    min-width: 80px;
    padding: 6px 16px;
}

/* 메시지박스 */
QMessageBox {
    background-color: #1e1e1e;
    color: #ffffff;
}

QMessageBox QPushButton {
    min-width: 80px;
    padding: 6px 16px;
}

/* 툴팁 */
QToolTip {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px;
}
"""

def apply_dark_theme(app):
    """애플리케이션에 다크 테마 적용"""
    app.setStyleSheet(DARK_STYLESHEET)
    
    # 애플리케이션 팔레트도 다크로 설정
    from PySide6.QtGui import QPalette, QColor
    from PySide6.QtCore import Qt
    
    palette = QPalette()
    
    # 기본 색상
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(37, 37, 37))
    palette.setColor(QPalette.AlternateBase, QColor(42, 42, 42))
    palette.setColor(QPalette.ToolTipBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(64, 64, 64))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(0, 120, 212))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 212))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    # 비활성화 상태 색상
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(102, 102, 102))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(102, 102, 102))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(102, 102, 102))
    
    app.setPalette(palette)