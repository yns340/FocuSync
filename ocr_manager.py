import pdfplumber
import re
import json
import os
import tempfile
import shutil
from google import genai

# ==========================================
# GOOGLE GEMINI API AYARLARI
# geminiKey.json dosyasından okunur — bu dosyayı .gitignore'a ekle!
# ==========================================
API_KEY = ""
try:
    _key_file = os.path.join(os.path.dirname(__file__), "geminiKey.json")
    with open(_key_file, "r", encoding="utf-8") as f:
        API_KEY = json.load(f).get("api_key", "")
except FileNotFoundError:
    print("[OCRManager] UYARI: geminiKey.json bulunamadı! Gemini AI devre dışı.")
except Exception as e:
    print(f"[OCRManager] UYARI: geminiKey.json okunamadı: {e}")

class OCRManager:
    def __init__(self):
        # 1. Sabit Program Regex'i
        self.schedule_pattern = r'([A-Z]+\s*\d{3,4}).*?(\d{2}:\d{2})\s+(\d{2}:\d{2})(u?)'
        
        # 2. Sınav Programı Regex'i 
        self.exam_pattern = r'\b([A-Za-z]{2,4}\s*\d{3,4})\b\s+(.*?)\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})'

    def parse_pdf(self, file_path):
        """
        PDF formatını otomatik tanır ve (success_bool, doc_type, data) döndürür.
        doc_type -> 'schedule', 'exam' veya 'error'
        """
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            return self._parse_with_ai(file_path, extracted_text=None)

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
            pass

        if extracted_text:
            exam_data = self._parse_exam(extracted_text)
            if len(exam_data) > 0:
                return True, "exam", exam_data

            schedule_data = self._parse_schedule(extracted_text)
            has_schedule_courses = any(len(courses) > 0 for courses in schedule_data.values())
            if has_schedule_courses:
                return True, "schedule", schedule_data

        return self._parse_with_ai(file_path, extracted_text=extracted_text)

    # ==========================================
    # SENİN ORİJİNAL REGEX FONKSİYONLARIN
    # ==========================================

    def _parse_schedule(self, text):
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
        exams_list = []
        for line in text.split('\n'):
            match = re.search(self.exam_pattern, line)
            if match:
                course_code = match.group(1).replace(" ", "").upper()
                raw_name_teacher = match.group(2)
                exam_date = match.group(3)
                exam_time = match.group(4)
                
                clean_name = re.split(r'\s+(?:PROF|DOÇ|DR|ÖĞR|ARŞ)\.', raw_name_teacher, flags=re.IGNORECASE)[0].strip()
                
                exams_list.append({
                    "course_id": course_code,
                    "course_name": clean_name,
                    "exam_date": exam_date,
                    "exam_time": exam_time,
                    "exam_type": "Vize", 
                    "notes": ""
                })
        return exams_list

    # ==========================================
    # YENİ GEMINI SDK + ASCII GÜVENLİK YAMASI
    # ==========================================

    def _parse_with_ai(self, file_path, extracted_text=None):
        if not API_KEY.strip():
            return (False, "error", "PDF formatı tanınamadı! Yapay Zeka taraması yapabilmek için lütfen geminiKey.json dosyasına API anahtarınızı girin.")

        prompt = """
Sen FocuSync uygulaması için çalışan bir veri çıkarım uzmanısın. Verilen içeriği analiz et.
Bana SADECE aşağıda belirttiğim kesin JSON formatlarından birini döndür.
Asla markdown (```json) etiketi ekleme, düz JSON yaz.

DURUM 1 (SINAV TAKVİMİ İSE):
{
  "type": "exam",
  "data": [
    {
      "course_id": "Ders Kodu",
      "course_name": "Ders Adı (hoca ismini ve unvanını sil)",
      "exam_date": "Sınav Tarihi (DD.MM.YYYY)",
      "exam_time": "Sınav Saati (HH:MM)",
      "exam_type": "Vize",
      "notes": "Salon bilgisi"
    }
  ]
}

DURUM 2 (DERS PROGRAMI İSE):
{
  "type": "schedule",
  "data": {
    "Pazartesi": [{"course": "KOD - DERS ADI", "start": "09:00", "end": "10:00", "ctype": "Teorik"}],
    "Salı": [], "Çarşamba": [], "Perşembe": [], "Cuma": [], "Cumartesi": [], "Pazar": []
  }
}

DURUM 3 (ANLAŞILAMADIYSa):
{
  "type": "error",
  "data": "Format anlaşılamadı"
}
"""
        uploaded_file = None
        safe_temp_path = None
        
        try:
            client = genai.Client(api_key=API_KEY)

            if extracted_text:
                content_parts = [prompt, f"\n\nDosya içeriği:\n{extracted_text}"]
            else:
                # --- ASCII HATASINI ÇÖZEN HİLE ---
                # Dosya adında Türkçe karakter varsa çökmemesi için geçici bir ASCII isimle kopyalıyoruz
                ext = os.path.splitext(file_path)[1]
                temp_dir = tempfile.gettempdir()
                safe_temp_path = os.path.join(temp_dir, f"focusync_safe_upload{ext}")
                
                shutil.copyfile(file_path, safe_temp_path)
                
                uploaded_file = client.files.upload(file=safe_temp_path, config={'display_name': 'focusync_doc'})
                content_parts = [prompt, uploaded_file]

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=content_parts
            )
            raw_text = response.text.strip()

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
            if uploaded_file:
                try:
                    client.files.delete(name=uploaded_file.name)
                except Exception:
                    pass
            # Kopyaladığımız geçici dosyayı bilgisayardan temizliyoruz
            if safe_temp_path and os.path.exists(safe_temp_path):
                os.remove(safe_temp_path)