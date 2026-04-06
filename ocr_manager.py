import pdfplumber
import re

class OCRManager:
    def __init__(self):
        # Gazi OBS formatını yakalar (Örn: EEE252 ... 13:30 14:20)
        self.pattern = r'([A-Z]+\s*\d{3,4}).*?(\d{2}:\d{2})\s+(\d{2}:\d{2})(u?)'

    def parse_pdf(self, file_path):
        schedule_data = {
            "Pazartesi": [], "Salı": [], "Çarşamba": [], 
            "Perşembe": [], "Cuma": [], "Cumartesi": [], "Pazar": []
        }
        
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    # Sadece layout=True kullanarak okuyalım ki tablonun yatay boşlukları korunsun
                    page_text = page.extract_text(layout=True)
                    if page_text:
                        text += page_text + "\n"
                        
            if not text.strip():
                return False, "PDF içinden metin okunamadı! Lütfen PDF'i açıp içindeki yazıların seçilebilir olduğundan emin olun."

            days_tr = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
            active_columns = [] 

            for line in text.split('\n'):
                # 1. Başlık satırını bul ve sütunların X koordinatlarını (indeksini) kaydet
                found_days = []
                for day in days_tr:
                    idx = line.find(day)
                    if idx != -1:
                        # KRİTİK DÜZELTME: Alt dize (substring) hatalarını önler
                        # "Pazar" kelimesi "Pazartesi"nin, "Cuma" ise "Cumartesi"nin içinde geçtiği için
                        if day == "Pazar" and line.find("Pazartesi") == idx:
                            continue
                        if day == "Cuma" and line.find("Cumartesi") == idx:
                            continue
                        
                        found_days.append((day, idx))
                
                if found_days:
                    # Sütunları soldan sağa doğru sırala
                    found_days.sort(key=lambda x: x[1])
                    active_columns = found_days
                    continue 
                
                # 2. Eğer elimizde aktif sütunlar varsa, dersleri bul ve ait olduğu güne at
                if active_columns:
                    matches = re.finditer(self.pattern, line)
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
            
            return True, schedule_data

        except Exception as e:
            return False, f"OCR Hatası: {str(e)}"