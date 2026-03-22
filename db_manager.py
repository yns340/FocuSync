import re
import firebase_admin
from firebase_admin import credentials, firestore

class DatabaseManager:
    def __init__(self, key_path="serviceAccountKey.json"):
        # Firebase uygulamasının birden fazla kez başlatılmasını engelle
        if not firebase_admin._apps:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()

    # ==========================================
    # KULLANICI PROFİLİ FONKSİYONLARI (WRITE & READ & UPDATE)
    # ==========================================

    def _is_valid_email(self, email):
        """E-posta formatının geçerli olup olmadığını RegEx ile kontrol eder."""
        # Standart e-posta formatı için Düzenli İfade (Regex)
        regex_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(regex_pattern, email) is not None

    def login_user(self, email, password):
        """Veritabanında email ve şifre eşleşmesini kontrol eder."""

        # 0. ADIM: Boşluk Kontrolü
        if not email.strip() or not password.strip():
            return False, "Hata: E-posta ve şifre alanları boş bırakılamaz!"

        # 1. ADIM: E-posta formatı geçerli mi?
        if not self._is_valid_email(email):
            return False, "Hata: Geçersiz e-posta formatı!"

        try:
            users_ref = self.db.collection("Users")
            query = users_ref.where("email", "==", email).where("password", "==", password).stream()
            
            for user in query:
                return True, user.id # Eşleşme bulundu, user_id dönüyor
            
            return False, "E-posta veya şifre hatalı."
        except Exception as e:
            return False, f"Sorgu hatası: {str(e)}"

    def register_user(self, email, password):
        """Yeni bir kullanıcıyı 'Users' koleksiyonuna ekler. Aynı e-posta varsa engeller."""

        # 0. ADIM: Boşluk Kontrolü
        if not email.strip() or not password.strip():
            return False, "Hata: E-posta ve şifre alanları boş bırakılamaz!"

        # 1. ADIM: E-posta formatı geçerli mi?
        if not self._is_valid_email(email):
            return False, "Hata: Lütfen geçerli bir e-posta adresi girin!"

        try:
            users_ref = self.db.collection("Users")
            
            # 2. ADIM: E-posta veritabanında var mı diye kontrol et
            existing_users = users_ref.where("email", "==", email).stream()
            for user in existing_users:
                return False, "Hata: Bu e-posta adresi zaten sisteme kayıtlı!"

            # 3. ADIM: Her şey tamamsa yeni kaydı oluştur
            doc_ref = self.db.collection("Users").document()
            doc_ref.set({
                "email": email,
                "password": password,
                "role": "User",
                "name": "",        # varsayılan boş
                "surname": "",     # varsayılan boş
                "school": ""       # varsayılan boş
            })
            return True, "Kullanıcı başarıyla kaydedildi."
        except Exception as e:
            return False, f"Kayıt hatası: {str(e)}"

    def get_user_profile(self, user_id):
        """Belirtilen user_id'ye ait tüm kullanıcı bilgilerini Firestore'dan okur."""
        try:
            doc_ref = self.db.collection("Users").document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return True, doc.to_dict() # Verileri sözlük (dict) olarak döndür
            else:
                return False, "Kullanıcı bulunamadı."
        except Exception as e:
            return False, f"Profil okuma hatası: {str(e)}"

    def update_user_profile(self, user_id, name, surname, school, new_password=None):
        """Kullanıcının profil bilgilerini ve (eğer girilmişse) şifresini günceller."""
        try:
            doc_ref = self.db.collection("Users").document(user_id)
            
            # Güncellenecek temel veriler
            update_data = {
                "name": name,
                "surname": surname,
                "school": school
            }
            
            # Eğer şifre de değiştirilmek istenmişse onu da sözlüğe ekle
            if new_password:
                update_data["password"] = new_password
                
            doc_ref.update(update_data) # Sadece bu alanları değiştirir, e-postaya dokunmaz
            return True, "Profil ayarları başarıyla kaydedildi."
        except Exception as e:
            return False, f"Profil güncelleme hatası: {str(e)}"

    # ==========================================
    # PROJE MİMARİSİ FONKSİYONLARI (FocuSync)
    # ==========================================

    def add_course(self, user_id, course_name, difficulty_level, exam_date):
        """
        ADIM 2 (PROFIL): Zeynep'in algoritması için dersin kimlik kartını oluşturur.
        Yunus OCR ile PDF'i okuduğunda yeni bir ders bulursan bu fonksiyonu çağıracaksın.
        """
        try:
            self.db.collection("Courses").add({
                "user_id": user_id,
                "course_name": course_name,
                "difficulty_level": difficulty_level, # Algoritma bunu güncelleyecek
                "exam_date": exam_date
            })
            return True, f"{course_name} dersi profile eklendi."
        except Exception as e:
            return False, f"Ders ekleme hatası: {str(e)}"

    def add_base_schedule(self, user_id, day, course_name, start_time, end_time):
        """
        ADIM 1 (OCR Görevi): Yunus PDF'ten okuyacağın SABİT OKUL PROGRAMINI kaydeder.
        """
        try:
            self.db.collection("Schedules").add({
                "user_id": user_id,
                "day": day,
                "course_name": course_name,
                "start_time": start_time,
                "end_time": end_time,
                "type": "School_Class"
            })
            return True, "Sabit okul programı eklendi."
        except Exception as e:
            return False, f"Program ekleme hatası: {str(e)}"

    def add_study_plan(self, user_id, course_name, planned_date, planned_duration):
        """
        ADIM 3 (Algoritma): Zeynep'in algoritmasının ürettiği AKILLI ÇALIŞMA PROGRAMINI kaydeder.
        Dikkat: course_name referans olarak tutuluyor, Courses tablosunu şişirmiyoruz!
        """
        try:
            self.db.collection("StudyPlans").add({
                "user_id": user_id,
                "course_name": course_name, # Hangi derse ait olduğunu burada tutuyoruz
                "planned_date": planned_date,
                "planned_duration": planned_duration,
                "is_completed": False
            })
            return True, "Uygulamanın önerdiği çalışma planı oluşturuldu."
        except Exception as e:
            return False, f"Plan oluşturma hatası: {str(e)}"

    def add_focus_session(self, user_id, plan_id, course_name, actual_focus_time, focus_score, status):
        """
        ADIM 4 (Kamera): Akif'in kamera sisteminden gelen GERÇEKLEŞEN odaklanma raporunu kaydeder.
        """
        try:
            self.db.collection("FocusSessions").add({
                "user_id": user_id,
                "study_plan_id": plan_id, # Hangi plana uyarak çalıştığını bağlarız
                "course_name": course_name,
                "actual_focus_time": actual_focus_time,
                "focus_score": focus_score,
                "status": status,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            return True, "Odaklanma seansı kaydedildi."
        except Exception as e:
            return False, f"Seans ekleme hatası: {str(e)}"

    def add_violation(self, user_id, session_id, app_name, duration):
        """
        ADIM 5 (Whitelist): Kerem'in yakaladığı ihlalleri kaydeder.
        """
        try:
            self.db.collection("Violations").add({
                "user_id": user_id,
                "session_id": session_id,
                "app_name": app_name,
                "duration": duration,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            return True, "İhlal kaydı oluşturuldu."
        except Exception as e:
            return False, f"İhlal ekleme hatası: {str(e)}"