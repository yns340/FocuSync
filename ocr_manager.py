import pdfplumber
import re

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
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text(layout=True)
                    if page_text:
                        text += page_text + "\n"
                        
            if not text.strip():
                return False, "error", "PDF içinden metin okunamadı! PDF'in seçilebilir metin içerdiğinden emin olun."

            # -- SWITCH CASE MANTIĞI --
            
            # CASE 1: Sınav Takvimi mi?
            exam_data = self._parse_exam(text)
            if len(exam_data) > 0:
                return True, "exam", exam_data

            # CASE 2: Sabit Ders Programı mı?
            schedule_data = self._parse_schedule(text)
            has_schedule_courses = any(len(courses) > 0 for courses in schedule_data.values())
            if has_schedule_courses:
                return True, "schedule", schedule_data

            # DEFAULT CASE: İkisi de değilse
            return False, "error", "PDF formatı tanınamadı! Lütfen geçerli bir Gazi Üniversitesi Sabit Ders Programı veya Sınav Takvimi yükleyin."

        except Exception as e:
            return False, "error", f"OCR Hatası: {str(e)}"

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
                    "exam_type": "Vize", # Standart Vize atıyoruz, UI'dan değiştirebilir
                    "notes": ""
                })
        return exams_list