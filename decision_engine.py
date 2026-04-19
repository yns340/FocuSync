import random
import math

class FocusDecisionEngine:
    def __init__(self):
        self.MIN_WORK = 15
        self.MAX_WORK = 60

    def calculate_energy(self, focus_score, violations):
        """SRS: Verimsizlik = (100 - Odak) + (İhlal * 10)"""
        return (100 - focus_score) + (violations * 10)

    def simulated_annealing_step(self, current_work_time, focus_score, violations):
        """Anlık veriye göre bir sonraki seansı belirler."""
        energy = self.calculate_energy(focus_score, violations)
        
        # Eğer verimsizlik (energy) yüksekse süreyi düşür
        if energy > 45:
            new_work = current_work_time - 5
        elif energy < 15: # Çok verimliyse süreyi artır
            new_work = current_work_time + 5
        else:
            new_work = current_work_time
            
        return max(self.MIN_WORK, min(new_work, self.MAX_WORK))

    def genetic_refinement(self, past_sessions):
        """Geçmiş seanslardan (popülasyon) en iyi süreyi evrimleştirir."""
        if not past_sessions: return 25
        # En yüksek odak skorlu 5 seansı seç (Doğal Seçilim)
        best_ones = sorted(past_sessions, key=lambda x: x.get('focus_score', 0), reverse=True)[:5]
        # Bu seansların sürelerinin ortalamasını al (Crossover)
        avg_time = sum(s.get('duration', 25) for s in best_ones) / len(best_ones)
        return int(avg_time)