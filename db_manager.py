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
        COMPOSITE KEY KULLANILIR (user_id + course_id) Çakışmaları önlemek için!
        """
        try:
            # 1. Courses tablosunu güncelle (Composite Key ile)
            unique_doc_id = f"{user_id}_{course_id}"
            
            doc_ref = self.db.collection("Courses").document(unique_doc_id)
            doc_ref.set({
                "user_id": user_id,
                "course_id": course_id, # UI çökmesin diye kodu içeri de yazıyoruz
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

            # 2. Kullanıcının MEVCUT tüm derslerini bul
            existing_courses_ref = self.db.collection("Courses").where("user_id", "==", user_id).stream()
            existing_course_ids = [doc.to_dict().get("course_id") for doc in existing_courses_ref]

            # 3. Courses tablosunu güncelle (Upsert Mantığı)
            for c_id, c_info in course_hours_dict.items():
                unique_doc_id = f"{user_id}_{c_id}"
                doc_ref = self.db.collection("Courses").document(unique_doc_id)
                
                if c_id in existing_course_ids:
                    # Ders veritabanında zaten varsa ismini, saatini güncelle ve AKTİF yap
                    doc_ref.update({
                        "course_name": c_info["name"],
                        "weekly_hours": c_info["hours"],
                        "is_active": True
                    })
                    existing_course_ids.remove(c_id)
                else:
                    # Ders ilk defa ekleniyorsa sıfırdan oluştur ve AKTİF yap
                    doc_ref.set({
                        "user_id": user_id,
                        "course_id": c_id,
                        "course_name": c_info["name"],
                        "difficulty_level": 3.0, 
                        "weekly_hours": c_info["hours"],
                        "exam_date": None,
                        "is_active": True
                    })

            # 4. Programda OLMAYAN eski dersleri PASİFE ÇEK (Soft Delete)
            for old_c_id in existing_course_ids:
                old_unique_id = f"{user_id}_{old_c_id}"
                self.db.collection("Courses").document(old_unique_id).update({
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
        """Kullanıcının tüm derslerini getirir."""
        try:
            courses = []
            docs = self.db.collection("Courses").where("user_id", "==", user_id).stream()
            for doc in docs:
                data = doc.to_dict()
                courses.append(data)
            return True, courses
        except Exception as e:
            return False, f"Dersleri okuma hatası: {str(e)}"

    def get_schedule(self, user_id):
        """Kullanıcının mevcut haftalık programını getirir."""
        try:
            docs = self.db.collection("Schedules").where("user_id", "==", user_id).stream()
            for doc in docs:
                return True, doc.to_dict() 
            return False, "Kayıtlı bir ders programı bulunamadı."
        except Exception as e:
            return False, f"Program okuma hatası: {str(e)}"

    def get_schedule_course_ids(self, user_id):
        """Kullanıcının aktif haftalık programındaki benzersiz ders ID'lerini döndürür."""
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
            docs = self.db.collection("StudyPlans").where("user_id", "==", user_id).stream()
            plans = [doc.to_dict() for doc in docs]
            if plans:
                return True, plans[-1] 
            return False, "Aktif bir çalışma planı bulunamadı."
        except Exception as e:
            return False, f"Plan okuma hatası: {str(e)}"

    # ==========================================
    # DELETE (SİLME) FONKSİYONU
    # ==========================================

    def delete_schedule(self, user_id):
        """Kullanıcının mevcut ders programını siler ve içindeki dersleri arşive (pasife) çeker."""
        try:
            docs = self.db.collection("Schedules").where("user_id", "==", user_id).stream()
            deleted_count = 0
            for doc in docs:
                data = doc.to_dict()
                routine = data.get("weekly_routine", {})
                
                # 1. Programdaki derslerin ID'lerini topla
                course_ids = set()
                for day, courses in routine.items():
                    for c in courses:
                        if "course_id" in c:
                            course_ids.add(c["course_id"])
                
                # 2. Bu dersleri Courses tablosunda is_active = False (Pasif) yap
                for cid in course_ids:
                    try:
                        unique_id = f"{user_id}_{cid}" # Composite Key Kullan
                        self.db.collection("Courses").document(unique_id).update({"is_active": False})
                    except Exception:
                        pass # Eğer ders daha önceden manuel silinmişse hata vermesin
                        
                # 3. Programı kalıcı olarak sil
                doc.reference.delete()
                deleted_count += 1
            
            if deleted_count > 0:
                return True, "Ders programı silindi ve içindeki dersler arşive alındı."
            return True, "Silinecek eski bir program bulunamadı."
        except Exception as e:
            return False, f"Program silme hatası: {str(e)}"
    
    def delete_course(self, user_id, course_id):
        """Kullanıcının seçtiği tekil bir dersi veritabanından kalıcı olarak siler."""
        try:
            unique_doc_id = f"{user_id}_{course_id}"
            doc_ref = self.db.collection("Courses").document(unique_doc_id)
            doc = doc_ref.get()
            
            if doc.exists and doc.to_dict().get("user_id") == user_id:
                doc_ref.delete()
                return True, "Ders başarıyla silindi."
            return False, "Ders bulunamadı veya silme yetkiniz yok."
        except Exception as e:
            return False, f"Ders silme hatası: {str(e)}"

    # ==========================================
    # UPDATE (GÜNCELLEME) FONKSİYONLARI - ALGORİTMA İÇİN
    # ==========================================

    def update_course_difficulty(self, user_id, course_id, new_difficulty):
        """SPMP Algoritması: Dersin zorluk seviyesini günceller."""
        try:
            unique_doc_id = f"{user_id}_{course_id}"
            doc_ref = self.db.collection("Courses").document(unique_doc_id)
            doc_ref.update({"difficulty_level": float(new_difficulty)})
            return True, "Ders zorluğu algoritma tarafından güncellendi."
        except Exception as e:
            return False, f"Zorluk güncelleme hatası: {str(e)}"

    def mark_session_completed(self, plan_id, day, session_id):
        """
        Kamera modülü bittiğinde, StudyPlans içindeki spesifik bir oturumu 'Tamamlandı' (True) yapar.
        """
        try:
            doc_ref = self.db.collection("StudyPlans").document(plan_id)
            doc = doc_ref.get()
            
            if doc.exists:
                plan_data = doc.to_dict()
                if day in plan_data.get("weekly_sessions", {}):
                    sessions = plan_data["weekly_sessions"][day]
                    for session in sessions:
                        if session.get("session_id") == session_id:
                            session["is_completed"] = True
                            break
                    
                    doc_ref.update({"weekly_sessions": plan_data["weekly_sessions"]})
                    return True, "Oturum başarıyla tamamlandı olarak işaretlendi."
            
            return False, "Plan veya oturum bulunamadı."
        except Exception as e:
            return False, f"Oturum güncelleme hatası: {str(e)}"

    # ==========================================
    # SINAV TAKVİMİ (EXAMS) FONKSİYONLARI
    # ==========================================

    def save_exam_schedule(self, user_id, exam_schedule_name, exams_list):
        """Kullanıcının sınav takvimini kaydeder ve Courses tablosundaki tarih ve notları SENKRONİZE eder."""
        try:
            docs = self.db.collection("Exams").where("user_id", "==", user_id).stream()
            exam_doc_ref = None
            for doc in docs:
                exam_doc_ref = doc.reference
                break
                
            exam_data = {
                "user_id": user_id,
                "exam_schedule_name": exam_schedule_name,
                "updated_at": firestore.SERVER_TIMESTAMP,
                "exams": exams_list
            }

            if exam_doc_ref:
                exam_doc_ref.update(exam_data)
            else:
                self.db.collection("Exams").add(exam_data)

            # --- KUSURSUZ SENKRONİZASYON (CASCADE SYNC) ---
            # 1. Her ders için tarih ve notları toparla
            course_updates = {}
            for exam in exams_list:
                c_id = exam.get("course_id")
                if not c_id: continue
                
                e_date = exam.get("exam_date", "")
                e_type = exam.get("exam_type", "Sınav")
                e_grade = exam.get("exam_grade", "").strip()

                if c_id not in course_updates:
                    course_updates[c_id] = {"exam_date": e_date, "exam_grades": {}}
                
                if e_grade: # Sadece not girilmişse sözlüğe ekle
                    course_updates[c_id]["exam_grades"][e_type] = e_grade

            # 2. Kullanıcının tüm derslerini çek
            courses_ref = self.db.collection("Courses").where("user_id", "==", user_id).stream()
            user_courses = {doc.to_dict().get("course_id"): doc.reference for doc in courses_ref}

            # 3. İlgili dersleri güncelle, listede olmayanların (silinenlerin) notlarını temizle
            for c_id, doc_ref in user_courses.items():
                if c_id in course_updates:
                    doc_ref.update(course_updates[c_id])
                else:
                    # Ders artık sınav takviminde yoksa tarih ve notları sıfırla!
                    doc_ref.update({"exam_date": "", "exam_grades": {}})

            return True, "Sınav takvimi ve ders notları başarıyla senkronize edildi."
        except Exception as e:
            return False, f"Hata: {str(e)}"

    def get_exam_schedule(self, user_id):
        try:
            docs = self.db.collection("Exams").where("user_id", "==", user_id).stream()
            for doc in docs:
                return True, doc.to_dict() 
            return False, "Kayıtlı bir sınav takvimi bulunamadı."
        except Exception as e:
            return False, f"Hata: {str(e)}"

    def delete_exam_schedule(self, user_id):
        """Takvimi siler ve Courses tablosundaki tüm tarih ve notları temizler."""
        try:
            docs = self.db.collection("Exams").where("user_id", "==", user_id).stream()
            deleted_count = 0
            
            for doc in docs:
                exam_data = doc.to_dict()
                exams_list = exam_data.get("exams", [])
                
                # Derslere gidip notları ve tarihleri temizle
                for exam in exams_list:
                    c_id = exam.get("course_id")
                    if c_id:
                        unique_id = f"{user_id}_{c_id}"
                        try:
                            self.db.collection("Courses").document(unique_id).update({
                                "exam_date": "",
                                "exam_grades": {}
                            })
                        except Exception:
                            pass 
                            
                doc.reference.delete()
                deleted_count += 1
            
            if deleted_count > 0:
                return True, "Sınav takvimi silindi ve ders kartlarındaki notlar temizlendi."
            return True, "Silinecek eski bir takvim bulunamadı."
        except Exception as e:
            return False, f"Takvim silme hatası: {str(e)}"