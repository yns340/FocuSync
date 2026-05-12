import sys
import signal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer 
from head_tracker import HeadTracker

def on_session_completed(data):
    print("\n🏁 OTURUM BİTTİ! VERİTABANINA GÖNDERİLECEK VERİLER:")
    print(f"   Odak Süresi: {data['actual_focus_time']} dakika")
    print(f"   Odak Skoru: % {data['focus_score']}")
    print(f"   Ortalama Kafa Eğimi: {data['head_tilt_degree']} derece")

def on_focus_changed(is_focused):
    if is_focused:
        print("🟢 ODAKLI: Ekrana bakıyorsun.")
    else:
        print("🔴 DİKKAT DAĞILDI: Kafanı çok çevirdin veya eğdin!")

def on_face_missing(is_missing):
    if is_missing:
        print("⚠️ YÜZ BULUNAMADI: Kameradan çıktın veya ışık yetersiz!")

def on_error(msg):
    print(f"❌ HATA: {msg}")

if __name__ == "__main__":
    # QThread'in çalışabilmesi için bir PyQt uygulaması başlatmamız şart
    app = QApplication(sys.argv)
    
    print("--- FocuSync Kafa Takibi Testi Başlıyor ---")
    print("Kameraya bakarak kafanızı sağa, sola, aşağı ve yukarı hareket ettirin.")
    print("Kapatmak için terminalde Ctrl + C yapabilirsiniz.\n")

    # Tracker'ı oluştur
    tracker = HeadTracker()

    def handle_exit(sig, frame):
        print("\nKapatılıyor...")
        tracker.stop()
        app.quit()

    signal.signal(signal.SIGINT, handle_exit)
    
    # Tracker'dan gelen sinyalleri yukarıdaki yazdığımız fonksiyonlara bağla
    tracker.focus_status_changed.connect(on_focus_changed)
    tracker.face_missing.connect(on_face_missing)
    tracker.error_occurred.connect(on_error)
    tracker.session_completed.connect(on_session_completed)
    
    # Arka plan iş parçacığını başlat
    tracker.start()

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)
    # Uygulamayı döngüye sok (kapanmaması için)
    sys.exit(app.exec())
