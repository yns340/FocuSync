import numpy as np
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QFrame, QDialog, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QImage, QPixmap

from head_tracker import HeadTracker 

# Ses çalmak için güvenli import (Mac/Linux çökmesini engeller)
try:
    import winsound
except ImportError:
    class DummySound:
        def Beep(self, freq, duration): pass
        def PlaySound(self, sound, flags): pass
        def MessageBeep(self, type): pass
        SND_ALIAS = 0
        SND_ASYNC = 0
        MB_ICONEXCLAMATION = 0
    winsound = DummySound()

# ==========================================
#  DİKKAT DAĞILDI POP-UP PENCERESİ (YENİ)
# ==========================================
class DistractionAlertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dikkat Dağıldı!")
        self.setModal(False) # Uygulamayı kilitlemesin
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint # HER ZAMAN EN ÜSTTE KALIR
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.Tool
        )
        self.resize(350, 150)
        self.setStyleSheet("""
            QDialog {
                background: #111318;
                border: 2px solid #ff6b35;
                border-radius: 12px;
            }
            QLabel {
                color: #ff6b35;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout(self)
        lbl = QLabel("🔴 DİKKAT DAĞILDI!\n\nLütfen ekrana geri dönün\nveya seansı bitirin.")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)


class FocusCircle(QWidget):
    def __init__(self, size=120, parent=None):
        super().__init__(parent)
        self.value = 0
        self.color = "#00e5a0"
        self.setFixedSize(size, size)

    def set_value(self, v, color=None):
        self.value = max(0, min(100, v))
        if color: self.color = color
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().adjusted(10,10,-10,-10)
        pen = QPen(QColor("#1e2130"), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        p.drawArc(r, 0, 360*16)
        if self.value > 0:
            pen.setColor(QColor(self.color))
            p.setPen(pen)
            p.drawArc(r, 90*16, -int(self.value/100*360*16))
        p.setPen(QColor("#e4e6ed"))
        p.setFont(QFont("Segoe UI",16,QFont.Weight.Bold))
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self.value}%")

class NotificationBanner(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(42)
        self.setVisible(False)
        l = QHBoxLayout(self)
        l.setContentsMargins(16,6,16,6)
        self.icon_lbl = QLabel()
        self.msg_lbl  = QLabel()
        self.msg_lbl.setStyleSheet("font-weight:600;background:transparent;border:none;")
        l.addWidget(self.icon_lbl)
        l.addWidget(self.msg_lbl)
        l.addStretch()
        self._timer = QTimer(); self._timer.setSingleShot(True)
        self._timer.timeout.connect(lambda: self.setVisible(False))

    def show_warning(self, icon, msg, color="#ff6b35", duration=5000):
        self.setStyleSheet(f"background:rgba(255,107,53,0.10);border:1px solid rgba(255,107,53,0.25);border-radius:8px;")
        if "yüz" in msg.lower() or "kamera" in msg.lower():
            self.setStyleSheet(f"background:rgba(245,158,11,0.10);border:1px solid rgba(245,158,11,0.25);border-radius:8px;")
            color = "#f59e0b"
        self.icon_lbl.setText(icon)
        self.icon_lbl.setStyleSheet(f"font-size:16px;background:transparent;border:none;")
        self.msg_lbl.setText(msg)
        self.msg_lbl.setStyleSheet(f"font-weight:600;color:{color};background:transparent;border:none;")
        self.setVisible(True)
        self._timer.start(duration)

class FocusPage(QWidget):
    violation_signal = pyqtSignal(str)

    def __init__(self, user_id: int, db_manager, parent=None):
        super().__init__(parent)
        self.user_id = str(user_id) # Garanti string yapalım
        self.db_manager = db_manager
        
        self._session_active = False
        self._elapsed = 0
        
        self.tracker = None
        self.is_user_focused = True 
        
        self._distraction_dialog = None # Pop-up için
        
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28,24,28,24)
        root.setSpacing(16)

        hdr = QHBoxLayout()
        title = QLabel("Odak Modu")
        title.setFont(QFont("Segoe UI",20,QFont.Weight.Bold))
        title.setStyleSheet("color:#e4e6ed;")
        hdr.addWidget(title); hdr.addStretch()
        root.addLayout(hdr)
        
        self.notif = NotificationBanner()
        root.addWidget(self.notif)

        main_row = QHBoxLayout(); main_row.setSpacing(16)
        left = QVBoxLayout(); left.setSpacing(14)

        # --- KAMERA KARTI ---
        cam_card = QFrame()
        cam_card.setStyleSheet("background:#111318;border:1px solid #1e2130;border-radius:14px;")
        cl = QVBoxLayout(cam_card); cl.setContentsMargins(16,14,16,14); cl.setSpacing(10)
        ch = QHBoxLayout()
        ch.addWidget(self._sec("Kamera Durumu"))
        self.cam_status_lbl = QLabel("⬤  Kapalı")
        self.cam_status_lbl.setStyleSheet("color:#6b7280;font-size:11px;background:transparent;border:none;")
        ch.addStretch(); ch.addWidget(self.cam_status_lbl)
        cl.addLayout(ch)

        cam_frame = QFrame()
        cam_frame.setStyleSheet("background:#0a0c10;border:1px dashed #1e2130;border-radius:10px;")
        cfl = QVBoxLayout(cam_frame); cfl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.cam_placeholder = QLabel("📷\nOturum Başladığında Aktif Olacak")
        self.cam_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cam_placeholder.setStyleSheet("color:#2e3248;font-size:14px;background:transparent;border:none;")
        self.cam_placeholder.setMinimumSize(480, 320)
        self.cam_placeholder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        cfl.addWidget(self.cam_placeholder)
        cl.addWidget(cam_frame)
        left.addWidget(cam_card, 2) 

        # --- ZAMANLAYICI KARTI ---
        timer_card = QFrame()
        timer_card.setStyleSheet("background:#111318;border:1px solid #1e2130;border-radius:14px;")
        tl = QHBoxLayout(timer_card); 
        tl.setContentsMargins(30,20,30,20); 
        tl.setSpacing(20)

        timer_info = QVBoxLayout()
        timer_info.addWidget(self._sec("⏱️ Seans Süresi"))
        self.timer_lbl = QLabel("00:00:00")
        self.timer_lbl.setFont(QFont("Segoe UI",48,QFont.Weight.Bold)) 
        self.timer_lbl.setStyleSheet("color:#00e5a0;letter-spacing:4px;background:transparent;border:none;")
        timer_info.addWidget(self.timer_lbl)
        tl.addLayout(timer_info); 
        
        tl.addStretch()

        #  DERS SEÇİMİ VE BAŞLATMA BUTONU
        btn_col = QVBoxLayout()
        btn_col.setAlignment(Qt.AlignmentFlag.AlignVCenter) 
        
        # Course dropdown
        course_lbl = QLabel("Ders Seçimi:")
        course_lbl.setStyleSheet("color:#a1a1aa; font-weight:bold; font-size:12px;")
        btn_col.addWidget(course_lbl)
        
        self.course_combo = QComboBox()
        self.course_combo.setFixedHeight(36)
        self.course_combo.setStyleSheet("""
            QComboBox { background:#1e2130; color:#f3f4f6; border:1px solid #2a3042; border-radius:6px; padding:4px 10px; }
            QComboBox::drop-down { border:none; }
        """)
        self._load_courses() # Veritabanından dersleri çek
        btn_col.addWidget(self.course_combo)
        
        btn_col.addSpacing(10)

        self.start_btn = QPushButton("▶  Seansı Başlat")
        self.start_btn.setObjectName("primary_btn")
        self.start_btn.setFixedSize(220, 50) 
        font = self.start_btn.font(); font.setPointSize(14); self.start_btn.setFont(font)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #00e5a0; border: 2px solid #00e5a0; border-radius: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #00e5a0; color: #111318; }
            QPushButton:pressed { background-color: #00e5a0; color: #111318; }
        """)

        self.start_btn.clicked.connect(self._toggle_session)
        btn_col.addWidget(self.start_btn)
        tl.addLayout(btn_col)
        left.addWidget(timer_card, 1)
        main_row.addLayout(left, 3)

        # --- SAĞ PANEL (SKOR) ---
        right = QVBoxLayout(); right.setSpacing(14)
        score_card = QFrame()
        score_card.setStyleSheet("background:#111318;border:1px solid #1e2130;border-radius:14px;")
        scl = QVBoxLayout(score_card); scl.setContentsMargins(18,14,18,14); scl.setSpacing(12)
        scl.addWidget(self._sec("Anlık Odak Skoru"))

        cring_row = QHBoxLayout(); cring_row.addStretch()
        self.focus_ring = FocusCircle(140); 
        cring_row.addWidget(self.focus_ring); cring_row.addStretch()
        scl.addLayout(cring_row)
        right.addWidget(score_card)
        right.addStretch()
        main_row.addLayout(right, 2)
        root.addLayout(main_row, 1)

    def _sec(self, text):
        l = QLabel(text); l.setFont(QFont("Segoe UI",13,QFont.Weight.Bold))
        l.setStyleSheet("color:#e4e6ed;background:transparent;border:none;")
        return l

    def _load_courses(self):
        """Veritabanından kullanıcının derslerini çeker ve ComboBox'a ekler"""
        self.course_combo.clear() # 🔥 YENİ: Listeyi yeniden doldurmadan önce eskilere bir temizlik çek!
        
        try:
            success, courses = self.db_manager.get_courses(self.user_id)
            if success and courses:
                for c in courses:
                    if c.get("is_active", True):
                        self.course_combo.addItem(c.get("course_name", "İsimsiz Ders"), c.get("course_id"))
            
            if self.course_combo.count() == 0:
                self.course_combo.addItem("Genel Çalışma", "genel_calisma")
        except Exception as e:
            self.course_combo.addItem("Genel Çalışma", "genel_calisma")

    def _toggle_session(self):
        if not self._session_active:
            self._start_session()
        else:
            self._end_session()

    def _start_session(self):
        self._session_active = True
        self._elapsed = 0
        self.is_user_focused = True

        self.tracker = HeadTracker()
        self.tracker.focus_status_changed.connect(self._on_focus_changed)
        self.tracker.face_missing.connect(self._on_face_missing)
        self.tracker.error_occurred.connect(self._on_error)
        self.tracker.session_completed.connect(self._on_session_completed)
        self.tracker.frame_processed.connect(self._on_frame_processed)
        
        # UI Kilitleri
        self.course_combo.setEnabled(False) 
        
        self.tracker.start()

        self.cam_status_lbl.setText("⬤  Aktif")
        self.cam_status_lbl.setStyleSheet("color:#00e5a0;font-size:11px;background:transparent;border:none;")
        self.cam_placeholder.setText("Kamera Yükleniyor...")

        self.focus_ring.set_value(100, "#00e5a0")
        self._timer.start(1000)
        
        self.start_btn.setText("⏹  Seansı Bitir")
        self.start_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #ff6b35; border: 2px solid #ff6b35; border-radius: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #ff6b35; color: #111318; }
        """)
        self.notif.show_warning("▶","Odak seansı ve Kamera Takibi başladı!","#00e5a0",3000)

    def _end_session(self):
        self._session_active = False
        self._timer.stop()
        
        if self.tracker:
            self.tracker.stop()

        # Açık kalmış olabilecek uyarı pop-up'ını kapat
        self._hide_distraction_popup()

        self.cam_status_lbl.setText("⬤  Kapalı")
        self.cam_status_lbl.setStyleSheet("color:#6b7280;font-size:11px;background:transparent;border:none;")
        self.cam_placeholder.clear()
        self.cam_placeholder.setText("📷\nKamera Beklemede")

        self.course_combo.setEnabled(True)
        
        self.start_btn.setText("▶  Seansı Başlat")
        self.start_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #00e5a0; border: 2px solid #00e5a0; border-radius: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #00e5a0; color: #111318; }
        """)
        
        self._elapsed = 0
        self.timer_lbl.setText("00:00:00")

    # ==========================================
    #  POP-UP SES VE GÖRÜNTÜ YÖNETİMİ
    # ==========================================
    def _show_distraction_popup(self):
        if not self._distraction_dialog:
            self._distraction_dialog = DistractionAlertDialog(self)
        
        if not self._distraction_dialog.isVisible():
            self._distraction_dialog.show()
            # Sistemin varsayılan hata/uyarı sesini çal
            try:
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except Exception:
                pass

    def _hide_distraction_popup(self):
        if self._distraction_dialog and self._distraction_dialog.isVisible():
            self._distraction_dialog.hide()

    # ==========================================
    #  HEAD TRACKER SİNYAL YAKALAYICILARI
    # ==========================================
    def _on_frame_processed(self, frame):
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(
            self.cam_placeholder.size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        self.cam_placeholder.setPixmap(scaled_pixmap)

    def _on_focus_changed(self, is_focused):
        self.is_user_focused = is_focused
        if not is_focused:
            self.notif.show_warning("🔴", "Dikkat Dağıldı! Lütfen ekrana odaklanın.", "#ff6b35", 3000)
            self._show_distraction_popup() # YENİ: Sesli Popup Göster
        else:
            self._hide_distraction_popup() # YENİ: Ekrana bakınca popup'ı kapat

    def _on_face_missing(self, is_missing):
        if is_missing:
            self.is_user_focused = False
            self.notif.show_warning("⚠️", "Yüz bulunamadı! Lütfen kameraya görünün.", "#f59e0b", 3000)
            self._show_distraction_popup()
        else:
            self.is_user_focused = True
            self._hide_distraction_popup()

    def _on_error(self, msg):
        QMessageBox.critical(self, "Kamera Hatası", f"Beklenmeyen bir donanım hatası oluştu:\n{msg}")
        self._end_session()

    def _on_session_completed(self, session_data):
        actual_focus_time = session_data["actual_focus_time"] 
        score = session_data["focus_score"] 
        head_tilt = session_data["head_tilt_degree"] 
        
        #Seçilen dersin ID'sini al
        selected_course_id = self.course_combo.currentData()

        try:
            success, msg = self.db_manager.add_focus_session(
                self.user_id,             
                "manuel_plan",            
                selected_course_id, # Artık rastgele string değil, Combobox'tan seçilen ders ID'si gidiyor 
                actual_focus_time,        
                head_tilt,                
                score,                    
                "Completed"               
            )
            self.notif.show_warning("✅",f"Seans tamamlandı! Veritabanına kaydedildi. Skor: %{score}", "#00e5a0", 6000)
        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası", f"Veritabanına bağlanılamadı! İnternet bağlantınızı kontrol edin.\n\nDetay: {str(e)}")

    def _tick(self):
        self._elapsed += 1
            
        h = self._elapsed // 3600; m = (self._elapsed % 3600) // 60; s = self._elapsed % 60
        self.timer_lbl.setText(f"{h:02d}:{m:02d}:{s:02d}")

        
        # Tracker'ın gönderdiği salise bazlı gerçek veriyi ekrana yansıt
        if self.tracker and self.tracker.total_session_time > 0:
            current_score = int((self.tracker.total_focus_time / self.tracker.total_session_time) * 100)
            
            color = "#00e5a0"
            if current_score < 50: color = "#ff6b35"
            elif current_score < 80: color = "#f59e0b"
            self.focus_ring.set_value(current_score, color)

    # ==========================================
    # 🔥 YENİ: SAYFA HER AÇILDIĞINDA ÇALIŞAN TETİKLEYİCİ
    # ==========================================
    def showEvent(self, event):
        """Kullanıcı bu sayfaya her tıkladığında/gördüğünde otomatik çalışır."""
        super().showEvent(event)
        
        # Sayfaya her girildiğinde ders listesini sessizce güncelle
        # (Böylece kullanıcı programı kapat-aç yapmak zorunda kalmaz)
        self._load_courses()

    def cleanup(self):
        self._timer.stop()
        self._hide_distraction_popup()
        if self.tracker:
            self.tracker.stop()

    