"""
ui/styles.py
FocuSync global QSS teması.
"""

APP_STYLE = """
/* ── Global ── */
QWidget {
    background-color: #0d0f14;
    color: #e4e6ed;
    font-family: 'Segoe UI', 'SF Pro Display', 'Ubuntu', sans-serif;
    font-size: 13px;
}

QMainWindow, QDialog {
    background-color: #0d0f14;
}

/* ── Sidebar ── */
#sidebar {
    background-color: #111318;
    border-right: 1px solid #1e2130;
    min-width: 210px;
    max-width: 210px;
}

#logo_label {
    font-size: 20px;
    font-weight: 700;
    color: #00e5a0;
    padding: 20px 20px 10px 20px;
    letter-spacing: -0.5px;
}

#nav_button {
    background: transparent;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    text-align: left;
    color: #6b7280;
    font-size: 13px;
    font-weight: 600;
    margin: 1px 8px;
}
#nav_button:hover {
    background-color: #1a1d26;
    color: #e4e6ed;
}
#nav_button[active="true"] {
    background-color: rgba(0, 229, 160, 0.10);
    color: #00e5a0;
    border: 1px solid rgba(0, 229, 160, 0.20);
}

/* ── Cards ── */
#card {
    background-color: #111318;
    border: 1px solid #1e2130;
    border-radius: 14px;
    padding: 20px;
}

/* ── Labels ── */
#page_title {
    font-size: 22px;
    font-weight: 700;
    color: #e4e6ed;
    letter-spacing: -0.5px;
}
#section_title {
    font-size: 13px;
    font-weight: 700;
    color: #e4e6ed;
    margin-bottom: 8px;
}
#muted_label {
    color: #6b7280;
    font-size: 11px;
}
#accent_label {
    color: #00e5a0;
    font-size: 11px;
    font-family: 'Consolas', 'Courier New', monospace;
}

/* ── Buttons ── */
QPushButton {
    background-color: #1a1d26;
    color: #e4e6ed;
    border: 1px solid #1e2130;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #222535;
    border-color: #2e3248;
}
QPushButton:pressed {
    background-color: #111318;
}

#primary_btn {
    background-color: #00e5a0;
    color: #000000;
    border: none;
    font-weight: 700;
}
#primary_btn:hover {
    background-color: #00ffb3;
}
#primary_btn:pressed {
    background-color: #00c282;
}

#danger_btn {
    background-color: rgba(255, 107, 53, 0.15);
    color: #ff6b35;
    border: 1px solid rgba(255, 107, 53, 0.30);
}
#danger_btn:hover {
    background-color: rgba(255, 107, 53, 0.25);
}

/* ── Inputs ── */
QLineEdit, QComboBox, QTimeEdit, QSpinBox, QDoubleSpinBox {
    background-color: #1a1d26;
    border: 1px solid #1e2130;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e4e6ed;
    font-size: 13px;
}
QLineEdit:focus, QComboBox:focus, QTimeEdit:focus {
    border-color: #00e5a0;
}
QLineEdit[echoMode="2"] {
    letter-spacing: 2px;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    background-color: #1a1d26;
    border: 1px solid #2e3248;
    border-radius: 8px;
    selection-background-color: rgba(0, 229, 160, 0.15);
    color: #e4e6ed;
    padding: 4px;
}

/* ── Tables ── */
QTableWidget {
    background-color: #111318;
    border: none;
    gridline-color: #1e2130;
    border-radius: 8px;
    font-size: 12px;
}
QTableWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid #1a1d26;
}
QTableWidget::item:selected {
    background-color: rgba(0, 229, 160, 0.12);
    color: #e4e6ed;
}
QHeaderView::section {
    background-color: #0d0f14;
    color: #6b7280;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 8px 12px;
    border: none;
    border-bottom: 1px solid #1e2130;
}

/* ── Scroll bars ── */
QScrollBar:vertical {
    background: #0d0f14;
    width: 6px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #2e3248;
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

/* ── Tab bar ── */
QTabWidget::pane { border: none; }
QTabBar::tab {
    background: transparent;
    color: #6b7280;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 12px;
    border: none;
    border-bottom: 2px solid transparent;
}
QTabBar::tab:selected {
    color: #00e5a0;
    border-bottom: 2px solid #00e5a0;
}
QTabBar::tab:hover { color: #e4e6ed; }

/* ── Check box ── */
QCheckBox {
    spacing: 8px;
    color: #e4e6ed;
}
QCheckBox::indicator {
    width: 18px; height: 18px;
    border-radius: 5px;
    border: 1px solid #2e3248;
    background: #1a1d26;
}
QCheckBox::indicator:checked {
    background-color: #00e5a0;
    border-color: #00e5a0;
    image: url(none);
}

/* ── ProgressBar ── */
QProgressBar {
    background-color: #1a1d26;
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00e5a0, stop:1 #0099ff);
    border-radius: 4px;
}

/* ── Message Box ── */
QMessageBox {
    background-color: #111318;
}
QMessageBox QPushButton {
    min-width: 80px;
}

/* ── Status bar ── */
QStatusBar {
    background-color: #0d0f14;
    color: #6b7280;
    font-size: 11px;
    border-top: 1px solid #1e2130;
    padding: 2px 8px;
}

/* ── Tooltips ── */
QToolTip {
    background-color: #1a1d26;
    color: #e4e6ed;
    border: 1px solid #2e3248;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 11px;
}
"""
