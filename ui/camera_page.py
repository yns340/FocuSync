from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class CameraPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)

        header_row = QHBoxLayout()
        title = QLabel("Kamera Takibi (Arayüz)")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header_row.addWidget(title)
        header_row.addStretch()

        self.start_btn = QPushButton("▶  Kamerayı Başlat (UI)")
        self.start_btn.setFixedHeight(36)
        self.start_btn.clicked.connect(self._toggle_camera)
        header_row.addWidget(self.start_btn)
        root.addLayout(header_row)

        self.status_lbl = QLabel("⬤  Kamera kapalı")
        self.status_lbl.setStyleSheet(
            "background:#111318;border:1px solid #1e2130;border-radius:8px;"
            "padding:8px 14px;color:#6b7280;font-size:12px;"
        )
        root.addWidget(self.status_lbl)

        feed_frame = QFrame()
        feed_frame.setStyleSheet("background:#111318;border:1px solid #1e2130;border-radius:14px;")
        feed_layout = QVBoxLayout(feed_frame)
        self.placeholder = QLabel("📷\nKamera Modülü (Core) Kaldırıldı.\nSadece Arayüz Tepkileri Aktif.")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color:#2e3248;font-size:18px;")
        feed_layout.addWidget(self.placeholder)
        root.addWidget(feed_frame, stretch=1)

    def _toggle_camera(self):
        if "Başlat" in self.start_btn.text():
            self.start_btn.setText("⏹  Kamerayı Durdur (UI)")
            self.status_lbl.setText("⬤  Kamera aktif (Sanal)")
            self.status_lbl.setStyleSheet("background:rgba(0,229,160,0.08);color:#00e5a0;padding:8px;border-radius:8px;")
        else:
            self.start_btn.setText("▶  Kamerayı Başlat (UI)")
            self.status_lbl.setText("⬤  Kamera kapalı")
            self.status_lbl.setStyleSheet("background:#111318;color:#6b7280;padding:8px;border-radius:8px;")

    def cleanup(self):
        pass