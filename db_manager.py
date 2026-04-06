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
        regex_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(regex_pattern, email) is not None

    def login_user(self, email, password):
        """Veritabanında email ve şifre eşleşmesini kontrol eder."""
        if not email.strip() or not password.strip():
            return False, "Hata: E-posta ve şifre alanları boş bırakılamaz!"

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
        """Yeni bir kullanıcıyı 'Users' koleksiyonuna şema formatında ekler."""
        if not email.strip() or not password.strip():
            return False, "Hata: E-posta ve şifre alanları boş bırakılamaz!"

        if not self._is_valid_email(email):
            return False, "Hata: Lütfen geçerli bir e-posta adresi girin!"

        try:
            users_ref = self.db.collection("Users")
            
            existing_users = users_ref.where("email", "==", email).stream()
            for user in existing_users:
                return False, "Hata: Bu e-posta adresi zaten sisteme kayıtlı!"

            doc_ref = self.db.collection("Users").document()
            doc_ref.set({
                "email": email,
                "password": password,
                "role": "User",
                "name": "",        
                "surname": "",     
                "school": "",      
                "allowed_apps": [],     # Whitelist için varsayılan boş liste
                "daily_study_goal": 0   # Algoritma için varsayılan çalışma hedefi
            })
            return True, "Kullanıcı başarıyla kaydedildi."
        except Exception as e:
            return False, f"Kayıt hatası: {str(e)}"

    def get_user_profile(self, user_id):
        """Belirtilen user_id'ye ait tüm kullanıcı bilgilerini okur."""
        try:
            doc_ref = self.db.collection("Users").document(user_id)
            doc = doc_ref.get()
            if doc.exists:
                return True, doc.to_dict()
            else:
                return False, "Kullanıcı bulunamadı."
        except Exception as e:
            return False, f"Profil okuma hatası: {str(e)}"

    def update_user_profile(self, user_id, name, surname, school, new_password=None, allowed_apps=None, daily_study_goal=None):
        """Kullanıcının profil bilgilerini, whitelist'ini veya çalışma hedefini günceller."""
        try:
            doc_ref = self.db.collection("Users").document(user_id)
            update_data = {
                "name": name,
                "surname": surname,
                "school": school
            }
            if new_password:
                update_data["password"] = new_password
            if allowed_apps is not None:
                update_data["allowed_apps"] = allowed_apps
            if daily_study_goal is not None:
                update_data["daily_study_goal"] = daily_study_goal
                
            doc_ref.update(update_data) 
            return True, "Profil ayarları başarıyla kaydedildi."
        except Exception as e:
            return False, f"Profil güncelleme hatası: {str(e)}"

    def get_dashboard_stats(self, user_id):
        """Dashboard sayfası için gerekli özet istatistikleri hesaplar ve döndürür."""
        try:
            stats = {
                "user_name": "",
                "course_count": 0,
                "avg_focus_score": 0,
                "total_study_time": 0, # Dakika cinsinden
                "violation_count": 0
            }

            # 1. Kullanıcı Adını Al
            user_doc = self.db.collection("Users").document(user_id).get()
            if user_doc.exists:
                stats["user_name"] = user_doc.to_dict().get("name", "")

            # 2. Ders Sayısını Al
            courses = self.db.collection("Courses").where("user_id", "==", user_id).stream()
            stats["course_count"] = sum(1 for _ in courses)

            # 3. İhlal Sayısını Al
            violations = self.db.collection("Violations").where("user_id", "==", user_id).stream()
            stats["violation_count"] = sum(1 for _ in violations)

            # 4. Toplam Çalışma Süresi ve Ortalama Odak Skoru
            sessions = self.db.collection("FocusSessions").where("user_id", "==", user_id).stream()
            total_score = 0
            session_count = 0
            
            for session in sessions:
                data = session.to_dict()
                stats["total_study_time"] += data.get("actual_focus_time", 0)
                total_score += data.get("focus_score", 0)
                session_count += 1
                
            if session_count > 0:
                stats["avg_focus_score"] = int(total_score / session_count)

            return True, stats
        except Exception as e:
            return False, f"Dashboard verileri alınamadı: {str(e)}"

    # ==========================================
    # PROJE MİMARİSİ FONKSİYONLARI (FocuSync SPMP)
    # ==========================================

    def add_course(self, user_id, course_id, course_name, difficulty_level, weekly_hours, exam_date=None):
        """
        Courses (Ana Tablo): Yeni bir ders oluşturur.
        DİKKAT: Firebase'in rastgele ID'si YERİNE, parametre olarak gelen course_id doküman ID'si olarak kullanılır.
        """
        try:
            doc_ref = self.db.collection("Courses").document(course_id)
            doc_ref.set({
                "user_id": user_id,
                "course_name": course_name,
                "difficulty_level": float(difficulty_level), 
                "weekly_hours": int(weekly_hours),
                "exam_date": exam_date
            })
            return True, doc_ref.id # Başarılı olursa course_id döner
        except Exception as e:
            return False, f"Ders ekleme hatası: {str(e)}"

    def save_schedule(self, user_id, schedule_name, weekly_routine):
        """
        Schedules: OCR ile okunan 7 günlük programı tek bir sözlük (dict) olarak kaydeder.
        weekly_routine formatı: {"Pazartesi": [{"course_id": "ceng318", "course_name": "Mikroişlemciler", "start_time": "09:30", "end_time": "10:20", "type": "School_Class"}...]}
        """
        try:
            self.db.collection("Schedules").add({
                "user_id": user_id,
                "schedule_name": schedule_name,
                "updated_at": firestore.SERVER_TIMESTAMP,
                "weekly_routine": weekly_routine
            })
            return True, "Haftalık program başarıyla kaydedildi."
        except Exception as e:
            return False, f"Program ekleme hatası: {str(e)}"

    def save_study_plan(self, user_id, plan_start_date, weekly_sessions):
        """
        StudyPlans: Zeynep'in algoritmasının ürettiği 7 günlük çalışma planını kaydeder.
        weekly_sessions formatı: {"Pazartesi": [{"session_id": "session1", "course_id": "ceng318", "course_name": "Mikroişlemciler", "planned_duration": 45, "is_completed": False}]}
        """
        try:
            self.db.collection("StudyPlans").add({
                "user_id": user_id,
                "plan_start_date": plan_start_date,
                "weekly_sessions": weekly_sessions
            })
            return True, "Akıllı çalışma planı oluşturuldu."
        except Exception as e:
            return False, f"Plan oluşturma hatası: {str(e)}"

    def add_focus_session(self, user_id, study_plan_session_id, course_id, actual_focus_time, focus_score, status):
        """
        FocusSessions: Akif'in kamera sisteminden gelen GERÇEKLEŞEN odaklanma raporunu kaydeder.
        """
        try:
            self.db.collection("FocusSessions").add({
                "user_id": user_id,
                "study_plan_session_id": study_plan_session_id, 
                "course_id": course_id,
                "actual_focus_time": int(actual_focus_time),
                "focus_score": float(focus_score),
                "status": status,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            return True, "Odaklanma seansı kaydedildi."
        except Exception as e:
            return False, f"Seans ekleme hatası: {str(e)}"

    def add_violation(self, user_id, focus_session_id, app_name, duration):
        """
        Violations: Kerem'in yakaladığı ihlalleri kaydeder.
        """
        try:
            self.db.collection("Violations").add({
                "user_id": user_id,
                "focus_session_id": focus_session_id,
                "app_name": app_name,
                "duration": int(duration),
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            return True, "İhlal kaydı oluşturuldu."
        except Exception as e:
            return False, f"İhlal ekleme hatası: {str(e)}"

    # ==========================================
    # GET (OKUMA) FONKSİYONLARI
    # ==========================================

    def get_courses(self, user_id):
        """Kullanıcının tüm derslerini ID'leri ile birlikte getirir."""
        try:
            courses = []
            docs = self.db.collection("Courses").where("user_id", "==", user_id).stream()
            for doc in docs:
                data = doc.to_dict()
                data["course_id"] = doc.id # Sonradan kullanmak için ID'yi de ekliyoruz
                courses.append(data)
            return True, courses
        except Exception as e:
            return False, f"Dersleri okuma hatası: {str(e)}"

    def get_schedule(self, user_id):
        """Kullanıcının mevcut haftalık programını getirir."""
        try:
            docs = self.db.collection("Schedules").where("user_id", "==", user_id).stream()
            for doc in docs:
                return True, doc.to_dict() # Sadece 1 tane olacağı için ilk bulduğunu döner
            return False, "Kayıtlı bir ders programı bulunamadı."
        except Exception as e:
            return False, f"Program okuma hatası: {str(e)}"

    def get_study_plan(self, user_id):
        """Kullanıcının güncel akıllı çalışma planını getirir."""
        try:
            # En son oluşturulan planı getirmek için tarihe göre sıralayabiliriz
            docs = self.db.collection("StudyPlans").where("user_id", "==", user_id).stream()
            plans = [doc.to_dict() for doc in docs]
            if plans:
                return True, plans[-1] # Şimdilik en son ekleneni dönüyoruz
            return False, "Aktif bir çalışma planı bulunamadı."
        except Exception as e:
            return False, f"Plan okuma hatası: {str(e)}"

    # (İstatistik sayfası için FocusSessions ve Violations GET fonksiyonları da eklenebilir)

    # ==========================================
    # DELETE (SİLME) FONKSİYONU
    # ==========================================

    def delete_schedule(self, user_id):
        """Kullanıcının mevcut ders programını siler (Yeni program yüklemeden önce çağrılır)."""
        try:
            docs = self.db.collection("Schedules").where("user_id", "==", user_id).stream()
            deleted_count = 0
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
            
            if deleted_count > 0:
                return True, "Eski ders programı başarıyla silindi."
            return True, "Silinecek eski bir program bulunamadı (Temiz)."
        except Exception as e:
            return False, f"Program silme hatası: {str(e)}"

    # ==========================================
    # UPDATE (GÜNCELLEME) FONKSİYONLARI - ALGORİTMA İÇİN
    # ==========================================

    def update_course_difficulty(self, course_id, new_difficulty):
        """SPMP Algoritması: Dersin zorluk seviyesini günceller."""
        try:
            doc_ref = self.db.collection("Courses").document(course_id)
            doc_ref.update({"difficulty_level": float(new_difficulty)})
            return True, "Ders zorluğu algoritma tarafından güncellendi."
        except Exception as e:
            return False, f"Zorluk güncelleme hatası: {str(e)}"

    def mark_session_completed(self, plan_id, day, session_id):
        """
        Kamera modülü bittiğinde, StudyPlans içindeki spesifik bir oturumu 'Tamamlandı' (True) yapar.
        Not: Firebase'de iç içe geçmiş sözlükleri güncellemek için önce belgeyi okuyup, 
        değişikliği yapıp tekrar kaydetmek en güvenli yoldur.
        """
        try:
            doc_ref = self.db.collection("StudyPlans").document(plan_id)
            doc = doc_ref.get()
            
            if doc.exists:
                plan_data = doc.to_dict()
                # İlgili günün içindeki oturumları ara
                if day in plan_data.get("weekly_sessions", {}):
                    sessions = plan_data["weekly_sessions"][day]
                    for session in sessions:
                        if session.get("session_id") == session_id:
                            session["is_completed"] = True
                            break
                    
                    # Güncellenmiş veriyi tekrar Firebase'e yaz
                    doc_ref.update({"weekly_sessions": plan_data["weekly_sessions"]})
                    return True, "Oturum başarıyla tamamlandı olarak işaretlendi."
            
            return False, "Plan veya oturum bulunamadı."
        except Exception as e:
            return False, f"Oturum güncelleme hatası: {str(e)}"