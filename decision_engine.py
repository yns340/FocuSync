import random
import math
import uuid
from datetime import datetime

# ──────────────────────────────────────────────────────────────
#  DecisionEngine  (SRS 3.2.7 / SDD 5.7)
#  db_manager.py tarafından import edilen asıl sınıf.
#  Oturum bitiminde tetiklenir ve zorluk katsayısını günceller.
# ──────────────────────────────────────────────────────────────
class DecisionEngine:
    """
    ADG-REQ-01/02/03: Oturum sonucuna göre dersin zorluk seviyesini
    dinamik olarak günceller ve yeni çalışma stratejisi üretir.
    """

    # ADG-PERF-01: Sabit alt/üst limitler (overfitting koruması)
    MIN_WORK_MINUTES  = 15   # Çalışma süresi hiçbir zaman bunun altına inemez
    MAX_WORK_MINUTES  = 60   # Çalışma süresi hiçbir zaman bunun üstüne çıkamaz
    MIN_BREAK_MINUTES = 5    # Mola süresi hiçbir zaman bunun altına inemez
    MAX_BREAK_MINUTES = 30   # Mola süresi hiçbir zaman bunun üstüne çıkamaz

    # ADG-ERR-01: Güncelleme için gereken minimum tamamlanmış oturum sayısı
    MIN_SESSIONS_REQUIRED = 3

    # ADG-REQ-02: Zorluk güncelleme eşikleri
    LOW_FOCUS_THRESHOLD      = 60   # Odak skoru bu değerin altındaysa zorluk artar
    HIGH_VIOLATION_RATIO     = 0.20 # İhlal süresi toplam sürenin %20'sini aşarsa zorluk artar

    def __init__(self, db_manager):
        self.db = db_manager

    # ----------------------------------------------------------
    #  Ana tetikleme noktası — mark_session_completed tarafından çağrılır
    # ----------------------------------------------------------
    def evaluate_session_and_adapt(
        self,
        user_id: str,
        course_id: str,
        planned_duration: float,
        actual_duration: float,
        whitelist_violations: int = 0,
    ):
        """
        ADG-REQ-01: Oturum bittikten sonra çağrılır.
        Odak skoru + ihlal verisiyle zorluk katsayısını günceller.
        """
        try:
            # 1. ADG-ERR-01 — Yeterli veri var mı?
            completed_count = self._count_completed_sessions(user_id, course_id)
            if completed_count < self.MIN_SESSIONS_REQUIRED:
                print(
                    f"[AI ENGINE] {course_id} için yalnızca {completed_count} tamamlanmış "
                    f"oturum var (min {self.MIN_SESSIONS_REQUIRED}). Güncelleme atlandı."
                )
                return

            # 2. ADG-REQ-01 — Son oturumun odak skorunu çek
            focus_score = self._get_last_focus_score(user_id, course_id)
            if focus_score is None:
                print("[AI ENGINE] Odak skoru alınamadı, güncelleme atlandı.")
                return

            # 3. ADG-REQ-02 — İhlal oranını hesapla
            violation_ratio = 0.0
            if actual_duration > 0 and whitelist_violations > 0:
                # Her ihlal olayını ~30 saniyelik ihlal süresi olarak modelle
                estimated_violation_seconds = whitelist_violations * 30
                violation_ratio = estimated_violation_seconds / (actual_duration * 60)

            low_focus      = focus_score < self.LOW_FOCUS_THRESHOLD
            high_violation = violation_ratio > self.HIGH_VIOLATION_RATIO

            # 4. ADG-REQ-02 — Zorluk katsayısını güncelle
            if low_focus or high_violation:
                action = "increase"
                reason = []
                if low_focus:
                    reason.append(f"odak skoru düşük (%{focus_score:.0f})")
                if high_violation:
                    reason.append(f"yüksek ihlal oranı (%{violation_ratio*100:.0f})")
                print(f"[AI ENGINE] {course_id} zorluğu ARTIRILDI. Neden: {', '.join(reason)}")
            else:
                action = "decrease"
                print(f"[AI ENGINE] {course_id} zorluğu AZALTILDI (iyi performans: %{focus_score:.0f})")

            self.db.update_course_difficulty(user_id, course_id, action)

            # 5. ADG-REQ-03 — Telafi seansı gerekiyor mu?
            if focus_score < 50:
                course_name = self._get_course_name(user_id, course_id)
                self._inject_makeup_session(user_id, course_id, course_name)

        except Exception as e:
            print(f"[AI ENGINE] evaluate_session_and_adapt hatası: {e}")

    # ----------------------------------------------------------
    #  Yardımcı metodlar
    # ----------------------------------------------------------
    def _count_completed_sessions(self, user_id: str, course_id: str) -> int:
        """ADG-ERR-01: Belirli bir ders için tamamlanmış oturum sayısını döndürür."""
        try:
            sessions = (
                self.db.db
                .collection("FocusSessions")
                .where("user_id", "==", user_id)
                .where("course_id", "==", course_id)
                .where("status", "==", "Completed")
                .get()
            )
            return len(sessions)
        except Exception as e:
            print(f"[AI ENGINE] Oturum sayısı alınamadı: {e}")
            return 0

    def _get_last_focus_score(self, user_id: str, course_id: str):
        """En son tamamlanmış odak oturumunun focus_score değerini döndürür."""
        try:
            sessions = (
                self.db.db
                .collection("FocusSessions")
                .where("user_id", "==", user_id)
                .where("course_id", "==", course_id)
                .where("status", "==", "Completed")
                .order_by("timestamp", direction="DESCENDING")
                .limit(1)
                .get()
            )
            if sessions:
                return sessions[0].to_dict().get("focus_score", None)
            return None
        except Exception as e:
            print(f"[AI ENGINE] Odak skoru alınamadı: {e}")
            return None

    def _get_course_name(self, user_id: str, course_id: str) -> str:
        """Ders adını Courses koleksiyonundan çeker."""
        try:
            doc = self.db.db.collection("Courses").document(f"{user_id}_{course_id}").get()
            if doc.exists:
                return doc.to_dict().get("course_name", course_id)
        except Exception:
            pass
        return course_id

    def _inject_makeup_session(self, user_id: str, course_id: str, course_name: str) -> bool:
        """
        ADG-REQ-03: Kullanıcı bir seansta başarısız olduğunda haftalık programı tarar
        ve uygun olan ilk güne kısa bir 'Telafi' seansı (Make-up Session) ekler.
        """
        try:
            plan_ref = (
                self.db.db
                .collection("StudyPlans")
                .where("user_id", "==", user_id)
                .limit(1)
                .get()
            )
            if not plan_ref:
                return False

            doc = plan_ref[0]
            weekly_sessions = doc.to_dict().get("weekly_sessions", {})

            days_order = [
                "Pazartesi", "Salı", "Çarşamba",
                "Perşembe", "Cuma", "Cumartesi", "Pazar"
            ]
            turkish_days = {
                "Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba",
                "Thursday": "Perşembe", "Friday": "Cuma",
                "Saturday": "Cumartesi", "Sunday": "Pazar"
            }
            today_tr = turkish_days.get(datetime.now().strftime('%A'), "Pazartesi")

            try:
                today_idx = days_order.index(today_tr)
            except ValueError:
                today_idx = 0

            target_day = None
            for i in range(1, 8):
                check_day = days_order[(today_idx + i) % 7]
                if len(weekly_sessions.get(check_day, [])) < 5:
                    target_day = check_day
                    break

            if not target_day:
                print("[AI ENGINE] Telafi seansı için uygun boş gün bulunamadı.")
                return False

            # ADG-PERF-01: Telafi seansı minimum süreden kısa olamaz
            makeup_duration = max(self.MIN_WORK_MINUTES, 30)

            makeup_session = {
                "session_id"      : f"makeup_{str(uuid.uuid4())[:8]}",
                "course_id"       : course_id,
                "course_name"     : f"{course_name} (Telafi)",
                "planned_duration": makeup_duration,
                "is_completed"    : False,
                "start_time"      : "16:00",
                "end_time"        : "16:30",
                "type"            : "Tekrar",
                "priority"        : "high",
            }

            weekly_sessions.setdefault(target_day, []).append(makeup_session)

            self.db.db.collection("StudyPlans").document(doc.id).update({
                f"weekly_sessions.{target_day}": weekly_sessions[target_day]
            })

            print(f"[AI ENGINE] BAŞARILI: {target_day} gününe '{course_name}' için telafi eklendi.")
            return True

        except Exception as e:
            print(f"[AI ENGINE] Telafi ekleme hatası: {e}")
            return False

    # ----------------------------------------------------------
    #  Haftalık toplu güncelleme (Pazar günü veya manuel tetikleme)
    # ----------------------------------------------------------
    def run_weekly_update(self, user_id: str):
        """
        ADG-REQ-02/03 + SDD §5.7.3:
        Son 7 günlük tüm FocusSessions'ı analiz eder ve zorlukları günceller.
        SuggestedPlanPage içindeki 'Yeniden Oluştur' butonundan veya
        uygulama başlangıcında (Pazar günüyse) tetiklenmelidir.
        """
        try:
            from datetime import timedelta, timezone
            now = datetime.now(timezone.utc)
            week_ago = now - timedelta(days=7)

            sessions = (
                self.db.db
                .collection("FocusSessions")
                .where("user_id", "==", user_id)
                .where("timestamp", ">=", week_ago)
                .get()
            )

            # course_id bazında verileri grupla
            course_data: dict[str, list[float]] = {}
            for s in sessions:
                d = s.to_dict()
                cid = d.get("course_id", "")
                score = d.get("focus_score", 0)
                if cid:
                    course_data.setdefault(cid, []).append(score)

            for course_id, scores in course_data.items():
                # ADG-ERR-01: Minimum oturum sayısı kontrolü
                if len(scores) < self.MIN_SESSIONS_REQUIRED:
                    print(f"[AI ENGINE] weekly: {course_id} yetersiz veri ({len(scores)} oturum).")
                    continue

                avg_score = sum(scores) / len(scores)
                action = "increase" if avg_score < self.LOW_FOCUS_THRESHOLD else "decrease"
                self.db.update_course_difficulty(user_id, course_id, action)
                print(f"[AI ENGINE] weekly: {course_id} → avg=%{avg_score:.0f} → {action}")

        except Exception as e:
            print(f"[AI ENGINE] run_weekly_update hatası: {e}")


# ──────────────────────────────────────────────────────────────
#  FocusDecisionEngine  (focus_page.py tarafından kullanılır)
#  Tek oturum bazında SpinBox sürelerini optimize eder.
# ──────────────────────────────────────────────────────────────
class FocusDecisionEngine:
    """Tek bir odak oturumunun enerji skorunu hesaplar ve çalışma süresini optimize eder."""

    MIN_WORK  = 15
    MAX_WORK  = 60
    MIN_BREAK = 5
    MAX_BREAK = 30

    def __init__(self):
        pass

    def calculate_energy(self, focus_score: float, violations: int) -> float:
        """Düşük odak + yüksek ihlal → yüksek enerji (verimsizlik)."""
        return (100 - focus_score) + (violations * 5)

    def simulated_annealing_step(
        self, current_work_time: int, focus_score: float, violations: int
    ) -> int:
        """ADG-PERF-01 sınırları dahilinde yeni çalışma süresini döndürür."""
        energy = self.calculate_energy(focus_score, violations)
        if energy > 50:
            new_work = current_work_time - 5
        elif energy < 15:
            new_work = current_work_time + 5
        else:
            new_work = current_work_time
        return max(self.MIN_WORK, min(new_work, self.MAX_WORK))

    def optimize_break(self, current_break: int, focus_score: float) -> int:
        """Odak skoruna göre mola süresini optimize eder (ADG-PERF-01 sınırlı)."""
        if focus_score < 50:
            new_break = current_break + 2
        elif focus_score > 85:
            new_break = current_break - 1
        else:
            new_break = current_break
        return max(self.MIN_BREAK, min(new_break, self.MAX_BREAK))

    def genetic_refinement(self, past_sessions: list) -> int:
        """Geçmiş seansların en başarılı 5'inin ortalama süresini döndürür."""
        if not past_sessions:
            return 25
        best_ones = sorted(
            past_sessions, key=lambda x: x.get("focus_score", 0), reverse=True
        )[:5]
        avg_time = sum(s.get("duration", 25) for s in best_ones) / len(best_ones)
        return int(avg_time)

    def predict_course_grades(self, user_id: str, db_manager) -> tuple[bool, list]:
        """
        Kullanıcının odaklanma geçmişini ve ders zorluklarını analiz ederek
        her ders için 0-100 arası not tahmini yapar.
        """
        try:
            success_c, courses = db_manager.get_courses(user_id)
            success_p, plan_data = db_manager.get_study_plan(user_id)

            if not success_c or not courses:
                return False, []

            weekly_sessions = (
                plan_data.get("weekly_sessions", {})
                if success_p and isinstance(plan_data, dict)
                else {}
            )

            predictions = []
            for course in courses:
                if not isinstance(course, dict) or not course.get("is_active", True):
                    continue

                c_id       = course.get("course_id")
                c_name     = course.get("course_name")
                difficulty = float(course.get("difficulty_level", 3.0))

                total_planned   = 0
                total_completed = 0
                for day, day_sessions in weekly_sessions.items():
                    for s in day_sessions:
                        if s.get("course_id") == c_id:
                            total_planned += 1
                            if s.get("is_completed", False):
                                total_completed += 1

                completion_rate = (
                    total_completed / total_planned if total_planned > 0 else 0.5
                )
                avg_focus_score = 40 + (completion_rate * 50)

                base_grade = avg_focus_score
                if difficulty >= 4.0:
                    base_grade += completion_rate * 15
                elif difficulty <= 2.0:
                    base_grade -= 5

                final_grade = max(0, min(100, int(base_grade)))

                if   final_grade >= 90: letter = "AA"
                elif final_grade >= 80: letter = "BA"
                elif final_grade >= 70: letter = "BB"
                elif final_grade >= 60: letter = "CB"
                elif final_grade >= 50: letter = "CC"
                elif final_grade >= 40: letter = "DC"
                else:                   letter = "FF"

                predictions.append({
                    "course_id"      : c_id,
                    "course_name"    : c_name,
                    "predicted_grade": final_grade,
                    "letter_grade"   : letter,
                    "difficulty_level": difficulty,
                })

            return True, predictions

        except Exception as e:
            print(f"[AI ENGINE] Not tahmini hatası: {e}")
            return False, []


# ──────────────────────────────────────────────────────────────
#  GeneticScheduler  (suggested_plan_page.py tarafından kullanılır)
# ──────────────────────────────────────────────────────────────
class GeneticScheduler:
    def __init__(self, courses: list, focus_history: dict):
        self.courses         = courses
        self.focus_history   = focus_history
        self.population_size = 10

    def calculate_fitness(self, schedule: dict) -> float:
        score = 0.0
        for slot, course in schedule.items():
            score += self.focus_history.get(slot, 50)
        return score

    def generate_optimal_plan(self) -> dict:
        sorted_slots = sorted(
            self.focus_history.items(), key=lambda x: x[1], reverse=True
        )
        best_plan = {}
        for i, course in enumerate(self.courses):
            if i < len(sorted_slots):
                best_plan[sorted_slots[i][0]] = course
        return best_plan


# ──────────────────────────────────────────────────────────────
#  SimulatedAnnealingScheduler
# ──────────────────────────────────────────────────────────────
class SimulatedAnnealingScheduler:
    """
    SRS 3.2.7.2'ye uygun: Ders programını 'Enerji' (Verimsizlik)
    değerini minimize ederek optimize eder.
    """

    def __init__(
        self,
        courses: list,
        focus_history: dict,
        temp: float = 100.0,
        cooling_rate: float = 0.95,
    ):
        self.courses      = courses
        self.history      = focus_history
        self.T            = temp
        self.cooling_rate = cooling_rate

    def calculate_energy(self, schedule: dict) -> float:
        total = 0.0
        for slot in schedule:
            total += 100 - self.history.get(slot, 50)
        return total

    def generate_plan(self) -> dict:
        slots = list(self.history.keys())
        current_schedule: dict = {}
        for i, c in enumerate(self.courses):
            if i < len(slots):
                current_schedule[slots[i]] = c

        current_energy = self.calculate_energy(current_schedule)

        while self.T > 1.0:
            new_schedule = current_schedule.copy()
            if len(slots) >= 2:
                s1, s2 = random.sample(slots, 2)
                if s1 in new_schedule and s2 in new_schedule:
                    new_schedule[s1], new_schedule[s2] = (
                        new_schedule[s2],
                        new_schedule[s1],
                    )

            new_energy = self.calculate_energy(new_schedule)
            if new_energy < current_energy:
                current_schedule, current_energy = new_schedule, new_energy
            else:
                delta = new_energy - current_energy
                if random.random() < math.exp(-delta / self.T):
                    current_schedule, current_energy = new_schedule, new_energy

            self.T *= self.cooling_rate

        return current_schedule