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

    def add_course(self, user_id, course_id, course_name, difficulty_level, weekly_hours, exam_date=None, is_active=True):
        """
        Courses (Ana Tablo): Yeni bir ders oluşturur veya günceller.
        AKILLI GÜNCELLEME: Eğer dersin ismi değişirse, 'Schedules' tablosundaki eski isimleri de bulup otomatik düzeltir.
        """
        try:
            # 1. Courses tablosunu güncelle (merge=True diğer verileri silmez)
            doc_ref = self.db.collection("Courses").document(course_id)
            doc_ref.set({
                "user_id": user_id,
                "course_name": course_name,
                "difficulty_level": float(difficulty_level),
                "weekly_hours": int(weekly_hours),
                "exam_date": exam_date,
                "is_active": is_active
            }, merge=True) 

            # 2. CASCADE UPDATE: Programdaki (Schedules) ismi de güncelle
            schedules = self.db.collection("Schedules").where("user_id", "==", user_id).stream()
            for schedule in schedules:
                sched_data = schedule.to_dict()
                routine = sched_data.get("weekly_routine", {})
                updated = False

                for day, courses in routine.items():
                    for c in courses:
                        # Eğer id eşleşirse ve isim değişmişse günceller
                        if c.get("course_id") == course_id and c.get("course_name") != course_name:
                            c["course_name"] = course_name
                            updated = True

                # Eğer programda bir şey değiştiyse Firebase'i yenile
                if updated:
                    schedule.reference.update({"weekly_routine": routine})

            return True, "Ders başarıyla kaydedildi/güncellendi."
        except Exception as e:
            return False, f"Ders kaydetme hatası: {str(e)}"

    def save_full_schedule(self, user_id, schedule_name, weekly_routine, course_hours_dict):
        """
        Eski programı siler, dersleri (Courses) akıllıca günceller/ekler (is_active mantığı ile) 
        ve yeni programı (Schedules) kaydeder.
        """
        try:
            # 1. Eski programı temizle
            self.delete_schedule(user_id)

            # 2. Kullanıcının MEVCUT tüm derslerini bul (Hangilerini False yapacağımızı bilmek için)
            existing_courses_ref = self.db.collection("Courses").where("user_id", "==", user_id).stream()
            existing_course_ids = [doc.id for doc in existing_courses_ref]

            # 3. Courses tablosunu güncelle (Upsert Mantığı)
            for c_id, c_info in course_hours_dict.items():
                doc_ref = self.db.collection("Courses").document(c_id)
                
                if c_id in existing_course_ids:
                    # Ders veritabanında zaten varsa ismini, saatini güncelle ve AKTİF yap
                    doc_ref.update({
                        "course_name": c_info["name"],
                        "weekly_hours": c_info["hours"],
                        "is_active": True
                    })
                    # İşlenen dersi listeden çıkar ki geriye sadece "pasife çekilmesi gerekenler" kalsın
                    existing_course_ids.remove(c_id)
                else:
                    # Ders ilk defa ekleniyorsa sıfırdan oluştur ve AKTİF yap
                    doc_ref.set({
                        "user_id": user_id,
                        "course_name": c_info["name"],
                        "difficulty_level": 3.0, 
                        "weekly_hours": c_info["hours"],
                        "exam_date": None,
                        "is_active": True
                    })

            # 4. Programda OLMAYAN eski dersleri PASİFE ÇEK (Soft Delete)
            # existing_course_ids listesinde kalanlar, yeni programda olmayan eski derslerdir.
            for old_c_id in existing_course_ids:
                self.db.collection("Courses").document(old_c_id).update({
                    "is_active": False
                })

            # 5. Yeni haftalık programı kaydet
            self.db.collection("Schedules").add({
                "user_id": user_id,
                "schedule_name": schedule_name,
                "updated_at": firestore.SERVER_TIMESTAMP,
                "weekly_routine": weekly_routine
            })
            return True, "Ders programı başarıyla kaydedildi, eski dersler arşive alındı."
        except Exception as e:
            return False, f"Program kaydetme hatası: {str(e)}"


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

    def add_focus_session(self, user_id, study_plan_session_id, course_id, actual_focus_time,head_tilt_degree, focus_score, status):
        """
        FocusSessions: Akif'in kamera sisteminden gelen GERÇEKLEŞEN odaklanma raporunu kaydeder.
        """
        try:
            self.db.collection("FocusSessions").add({
                "user_id": user_id,
                "study_plan_session_id": study_plan_session_id, 
                "course_id": course_id,
                "actual_focus_time": int(actual_focus_time),
                "head_tilt_degree": float(head_tilt_degree),
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

    def get_schedule_course_ids(self, user_id):
        """Kullanıcının aktif haftalık programındaki benzersiz ders ID'lerini döndürür (Kilit mekanizması için)."""
        try:
            schedules = self.db.collection("Schedules").where("user_id", "==", user_id).stream()
            course_ids = set()
            for schedule in schedules:
                routine = schedule.to_dict().get("weekly_routine", {})
                for day, courses in routine.items():
                    for c in courses:
                        course_ids.add(c.get("course_id"))
            return True, list(course_ids)
        except Exception as e:
            return False, []

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
    
    def delete_course(self, user_id, course_id):
        """Kullanıcının seçtiği tekil bir dersi veritabanından kalıcı olarak siler."""
        try:
            doc_ref = self.db.collection("Courses").document(course_id)
            doc = doc_ref.get()
            
            # Sadece ders varsa ve bu kullanıcıya aitse silmesine izin ver (Güvenlik)
            if doc.exists and doc.to_dict().get("user_id") == user_id:
                doc_ref.delete()
                return True, "Ders başarıyla silindi."
            return False, "Ders bulunamadı veya silme yetkiniz yok."
        except Exception as e:
            return False, f"Ders silme hatası: {str(e)}"

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