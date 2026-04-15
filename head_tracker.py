import cv2
import numpy as np
import time
from PyQt6.QtCore import QThread, pyqtSignal

from mediapipe.tasks.python import vision
from mediapipe import Image, ImageFormat
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import FaceLandmarkerOptions, FaceLandmarker


class HeadTracker(QThread):
    focus_status_changed = pyqtSignal(bool)
    face_missing = pyqtSignal(bool)
    error_occurred = pyqtSignal(str)
    session_completed = pyqtSignal(dict)

    frame_processed = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_running = True

        # 🔥 MODEL YÜKLEME
        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path="face_landmarker.task"),
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=True,
            num_faces=1
        )

        self.detector = FaceLandmarker.create_from_options(options)
        # 🔥 KALİBRASYON VE LİMİT DEĞİŞKENLERİ
        self.PITCH_LIMIT = 16  # Eski hali 20'ydi. (Yukarı/Aşağı kafa eğme toleransı)
        self.YAW_LIMIT = 18    # Eski hali 25'ti. (Sağa/Sola kafa çevirme toleransı)
        self.is_calibrated = False
        self.calibration_frames = []
        self.base_pitch = 0.0
        self.base_yaw = 0.0

        # 🔥 DURUM TAKİBİ (STATE MACHINE) VE TAMPON (DEBOUNCE)
        self.current_focus_state = True   
        self.current_face_missing = False 
        self.out_of_bounds_frames = 0     
        self.REQUIRED_FRAMES = 4          
        
        #KRONOMETRE VE VERİ TOPLAMA
        self.total_session_time = 0.0 # Saniye cinsinden
        self.total_focus_time = 0.0   # Saniye cinsinden
        self.is_currently_focused = True
        self.last_time = time.time()
        

    def run(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            self.error_occurred.emit("Kamera açılamadı!")
            return

        fps_limit = 15
        delay = 1.0 / fps_limit

        while self.is_running:
            start_time = time.time()

            #  SÜRE HESAPLAMA (Delta Time)
            delta_time = start_time - self.last_time
            self.last_time = start_time
            
            self.total_session_time += delta_time
            
            # Eğer sistem son olarak "Odaklı" durumdaysa, odak süresini artır
            if self.is_currently_focused:
                self.total_focus_time += delta_time

            success, frame = cap.read()
            if not success:
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            self.frame_processed.emit(rgb_frame)

            # 🔥 MEDIAPIPE IMAGE FORMAT
            mp_image = Image(
                image_format=ImageFormat.SRGB,
                data=rgb_frame
            )

            result = self.detector.detect(mp_image)

            if result.face_landmarks:
                # 1. Yüz bulundu sinyalini SADECE yüz yeni geldiyse gönder (Spam engelleme)
                if self.current_face_missing == True:
                    self.face_missing.emit(False)
                    self.current_face_missing = False

                landmarks = result.face_landmarks[0]
                pitch, yaw, roll = self.calculate_head_pose(frame, landmarks)

                # 🔥 DİNAMİK KALİBRASYON AŞAMASI
                if not self.is_calibrated:
                    self.calibration_frames.append((pitch, yaw))
                    if len(self.calibration_frames) >= 15:
                        self.base_pitch = sum(p[0] for p in self.calibration_frames) / 15
                        self.base_yaw = sum(p[1] for p in self.calibration_frames) / 15
                        self.is_calibrated = True
                        print(f"✅ KALİBRASYON TAMAM! Merkez Pitch: {self.base_pitch:.1f} | Merkez Yaw: {self.base_yaw:.1f}")
                    continue

                # 🔥 MERKEZE GÖRE GÖRECELİ AÇI HESAPLAMA
                relative_pitch = pitch - self.base_pitch
                relative_yaw = yaw - self.base_yaw
               

                # 2. Anlık durum kontrolü (Sınır aşıldı mı?)
                is_out_of_bounds = abs(relative_pitch) > self.PITCH_LIMIT or abs(relative_yaw) > self.YAW_LIMIT

                # 3. TAMPON (DEBOUNCE) UYGULAMASI: Anlık dalgalanmaları filtrele
                if is_out_of_bounds:
                    self.out_of_bounds_frames += 1
                else:
                    # Kafasını hemen geri çevirdiyse sayacı sıfırla, hatasını affet
                    self.out_of_bounds_frames = 0 

                # Eğer kullanıcı 5 kare boyunca ısrarla sınırın dışındaysa (yani kalıcı bir hareketse)
                new_focus_state = True
                if self.out_of_bounds_frames >= self.REQUIRED_FRAMES:
                    new_focus_state = False

                # 4. STATE MACHINE: Sinyali SADECE durum değiştiğinde gönder
                if new_focus_state != self.current_focus_state:
                    self.current_focus_state = new_focus_state
                    self.is_currently_focused = new_focus_state
                    self.focus_status_changed.emit(self.current_focus_state)

            else:
                # Yüz tespit edilemediğinde (Spam engelleme)
                if self.current_face_missing == False:
                    self.face_missing.emit(True)
                    self.current_face_missing = True
                
                # Yüz yoksa odak anında bozulur
                if self.current_focus_state == True:
                    self.current_focus_state = False
                    self.is_currently_focused = False
                    self.focus_status_changed.emit(False)

            elapsed = time.time() - start_time
            if elapsed < delay:
                time.sleep(delay - elapsed)

        cap.release()

    def calculate_head_pose(self, image, landmarks):
        img_h, img_w, _ = image.shape

        # 🔥 Landmark -> pixel
        indices = [1, 152, 226, 446, 57, 287]

        face_2d = []
        for idx in indices:
            lm = landmarks[idx]
            x, y = int(lm.x * img_w), int(lm.y * img_h)
            face_2d.append([x, y])

        face_2d = np.array(face_2d, dtype=np.float64)

        face_3d = np.array([
            [0.0, 0.0, 0.0],
            [0.0, -330.0, -65.0],
            [-225.0, 170.0, -135.0],
            [225.0, 170.0, -135.0],
            [-150.0, -150.0, -125.0],
            [150.0, -150.0, -125.0]
        ], dtype=np.float64)

        focal_length = img_w
        cam_matrix = np.array([
            [focal_length, 0, img_w / 2],
            [0, focal_length, img_h / 2],
            [0, 0, 1]
        ])

        dist_matrix = np.zeros((4, 1))

        success, rot_vec, trans_vec = cv2.solvePnP(
            face_3d, face_2d, cam_matrix, dist_matrix
        )

        rmat, _ = cv2.Rodrigues(rot_vec)
        angles, *_ = cv2.RQDecomp3x3(rmat)

        pitch, yaw, roll = angles
        # 🔥 NORMALIZATION EKLE
        if pitch < -90:
            pitch += 180
        elif pitch > 90:
            pitch -= 180
        return pitch, yaw, roll

    def stop(self):
        self.is_running = False
        
        # 🔥 OTURUM SONU HESAPLAMALARI
        focus_time_minutes = self.total_focus_time / 60.0
        
        # Sıfıra bölünme hatasını önle
        if self.total_session_time > 0:
            focus_score_percent = (self.total_focus_time / self.total_session_time) * 100.0
        else:
            focus_score_percent = 0.0
            
        # Veritabanına (db_manager'a) gönderilecek formatta sözlük oluştur
        session_data = {
            "actual_focus_time": round(focus_time_minutes, 2), # Dakika
            "focus_score": round(focus_score_percent, 1),      # Yüzde
            "head_tilt_degree": round(self.base_pitch, 1)      # Kalibre edilmiş referans eğim
        }
        
        # Sinyali fırlat
        self.session_completed.emit(session_data)
        
        self.wait()