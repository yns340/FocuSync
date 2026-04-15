import pdfplumber
import re
import json
import os
import google.generativeai as genai

# ==========================================
# GOOGLE GEMINI API AYARLARI
# geminiKey.json dosyasından okunur — bu dosyayı .gitignore'a ekle!
# ==========================================
API_KEY = ""
try:
    _key_file = os.path.join(os.path.dirname(__file__), "geminiKey.json")
    with open(_key_file, "r") as f:
        API_KEY = json.load(f).get("api_key", "")
except FileNotFoundError:
    print("[OCRManager] UYARI: geminiKey.json bulunamadı! Gemini AI devre dışı.")
except Exception as e:
    print(f"[OCRManager] UYARI: geminiKey.json okunamadı: {e}")

if API_KEY.strip():
    genai.configure(api_key=API_KEY)


class OCRManager:
    def __init__(self):
        # 1. Sabit Program Regex'i (Örn: EEE252 ... 13:30 14:20)
        self.schedule_pattern = r'([A-Z]+\s*\d{3,4}).*?(\d{2}:\d{2})\s+(\d{2}:\d{2})(u?)'
        
        # 2. Sınav Programı Regex'i (Ders Kodu, İsim+Hoca, Tarih, Saat)
        # Örn: CENG442 MICROSERVICE BASED SOFTWARE DEV. DR. HÜSEYİN 01.04.2026 11:00
        self.exam_pattern = r'\b([A-Za-z]{2,4}\s*\d{3,4})\b\s+(.*?)\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})'

    def parse_pdf(self, file_path):
        """
        PDF formatını otomatik tanır ve (success_bool, doc_type, data) döndürür.
        doc_type -> 'schedule', 'exam' veya 'error'

        CASE 1: Sınav Takvimi → pdfplumber + _parse_exam regex
        CASE 2: Sabit Ders Programı → pdfplumber + _parse_schedule regex
        CASE 3: Hiçbiri değilse → Gemini AI son çare
        """
        # Görüntü dosyası ise direkt Gemini'ye gönder (pdfplumber görüntü okuyamaz)
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            return self._parse_with_ai(file_path, extracted_text=None)

        # --- PDF Okuma ---
        extracted_text = None
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text(layout=True)
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                extracted_text = text
        except Exception:
            # PDF açılamadıysa Gemini'ye bırak
            pass

        # Metin çıkarıldıysa önce regex'leri dene
        if extracted_text:
            # CASE 1: Sınav Takvimi mi?
            exam_data = self._parse_exam(extracted_text)
            if len(exam_data) > 0:
                return True, "exam", exam_data

            # CASE 2: Sabit Ders Programı mı?
            schedule_data = self._parse_schedule(extracted_text)
            has_schedule_courses = any(len(courses) > 0 for courses in schedule_data.values())
            if has_schedule_courses:
                return True, "schedule", schedule_data

        # CASE 3: Regex'ler tutmadı ya da metin çıkarılamadı → Gemini son çare
        return self._parse_with_ai(file_path, extracted_text=extracted_text)

    # ==========================================
    # CASE 1 & 2 — SENİN ORIJINAL REGEX FONKSİYONLARI
    # (Hiçbir satırına dokunulmadı)
    # ==========================================

    def _parse_schedule(self, text):
        """Sabit ders programını günlere göre ayırır."""
        schedule_data = {
            "Pazartesi": [], "Salı": [], "Çarşamba": [], 
            "Perşembe": [], "Cuma": [], "Cumartesi": [], "Pazar": []
        }
        days_tr = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        active_columns = [] 

        for line in text.split('\n'):
            found_days = []
            for day in days_tr:
                idx = line.find(day)
                if idx != -1:
                    # Alt kelime karmaşasını önle (Pazar / Pazartesi)
                    if day == "Pazar" and line.find("Pazartesi") == idx: continue
                    if day == "Cuma" and line.find("Cumartesi") == idx: continue
                    found_days.append((day, idx))
            
            if found_days:
                found_days.sort(key=lambda x: x[1])
                active_columns = found_days
                continue 
            
            if active_columns:
                matches = re.finditer(self.schedule_pattern, line)
                for match in matches:
                    match_pos = match.start() 
                    assigned_day = active_columns[0][0] 
                    for day, pos in active_columns:
                        if match_pos >= pos - 20: 
                            assigned_day = day

                    course_code = match.group(1).replace(" ", "") 
                    start_time = match.group(2)
                    end_time = match.group(3)
                    is_uygulamali = match.group(4) == 'u'

                    schedule_data[assigned_day].append({
                        "course": f"{course_code} - ", 
                        "start": start_time,
                        "end": end_time,
                        "ctype": "Uygulamalı" if is_uygulamali else "Teorik"
                    })
        return schedule_data

    def _parse_exam(self, text):
        """Sınav takviminden kodu, adı, tarihi ve saati çeker."""
        exams_list = []
        for line in text.split('\n'):
            match = re.search(self.exam_pattern, line)
            if match:
                course_code = match.group(1).replace(" ", "").upper()
                raw_name_teacher = match.group(2)
                exam_date = match.group(3)
                exam_time = match.group(4)
                
                # Zekice bir hamle: Hoca Unvanlarını gördüğümüz yerden metni kesiyoruz!
                # Böylece elimizde sadece tertemiz "DERS ADI" kalıyor.
                clean_name = re.split(r'\s+(?:PROF|DOÇ|DR|ÖĞR|ARŞ)\.', raw_name_teacher, flags=re.IGNORECASE)[0].strip()
                
                exams_list.append({
                    "course_id": course_code,
                    "course_name": clean_name,
                    "exam_date": exam_date,
                    "exam_time": exam_time,
                    "exam_type": "Vize",  # Standart Vize atıyoruz, UI'dan değiştirebilir
                    "notes": ""
                })
        return exams_list

    # ==========================================
    # CASE 3 — GEMINI AI SON ÇARE
    # ==========================================

    def _parse_with_ai(self, file_path, extracted_text=None):
        """
        Regex'lere uymayan dosyaları Gemini AI okur.
        
        Strateji:
        - PDF'den metin çıkarılabildiyse → metni Gemini'ye ver (daha hızlı, dosya upload gerekmez)
        - Metin çıkarılamadıysa (taranmış PDF, görüntü) → dosyayı Gemini'ye upload et
        """
        if not API_KEY.strip():
            return (
                False, "error",
                "PDF formatı tanınamadı! Akıllı Yapay Zeka taraması yapabilmek için "
                "lütfen ocr_manager.py dosyasına Google API anahtarınızı girin."
            )

        prompt = """
Sen FocuSync uygulaması için çalışan bir veri çıkarım uzmanısın. Verilen içeriği analiz et.
Bana SADECE aşağıda belirttiğim kesin JSON formatlarından birini döndür.
Asla markdown (```json) etiketi ekleme, düz JSON yaz.

DURUM 1 (SINAV TAKVİMİ İSE):
{
  "type": "exam",
  "data": [
    {
      "course_id": "Ders Kodu (boşluksuz büyük harf, örn: CENG442)",
      "course_name": "Ders Adı (hoca ismini ve unvanını sil)",
      "exam_date": "Sınav Tarihi (DD.MM.YYYY formatında)",
      "exam_time": "Sınav Saati (HH:MM formatında)",
      "exam_type": "Vize",
      "notes": "Salon bilgisi varsa buraya, yoksa boş bırak"
    }
  ]
}

DURUM 2 (DERS PROGRAMI İSE):
{
  "type": "schedule",
  "data": {
    "Pazartesi": [{"course": "KOD - DERS ADI", "start": "09:00", "end": "10:00", "ctype": "Teorik"}],
    "Salı": [],
    "Çarşamba": [],
    "Perşembe": [],
    "Cuma": [],
    "Cumartesi": [],
    "Pazar": []
  }
}

DURUM 3 (ANLAŞILAMADIYSa):
{
  "type": "error",
  "data": "Format anlaşılamadı"
}
"""

        uploaded_file = None
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')

            # Strateji: Metin varsa dosya yükleme, doğrudan metni ver
            if extracted_text:
                content_parts = [
                    prompt,
                    f"\n\nDosya içeriği (düz metin):\n{extracted_text}"
                ]
            else:
                # Metin yoksa (taranmış PDF / görüntü) dosyayı yükle
                uploaded_file = genai.upload_file(path=file_path, display_name="focusync_doc")
                content_parts = [prompt, uploaded_file]

            response = model.generate_content(content_parts)
            raw_text = response.text.strip()

            # Yine de markdown fence geldiyse temizle (güvenlik önlemi)
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:].strip()
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3].strip()

            ai_data = json.loads(raw_text)
            doc_type = ai_data.get("type")
            data = ai_data.get("data")

            if doc_type == "exam" and isinstance(data, list) and len(data) > 0:
                return True, "exam", data
            elif doc_type == "schedule" and isinstance(data, dict):
                return True, "schedule", data
            else:
                return False, "error", "Yapay Zeka dosyayı inceledi ancak içinden geçerli bir program çıkaramadı."

        except json.JSONDecodeError:
            return False, "error", "Yapay Zeka geçersiz bir yanıt döndürdü. Lütfen tekrar deneyin."
        except Exception as e:
            return False, "error", f"Yapay Zeka Çözümleme Hatası: {str(e)}"
        finally:
            # Upload ettiyse temizle
            if uploaded_file:
                try:
                    genai.delete_file(uploaded_file.name)
                except Exception:
                    pass