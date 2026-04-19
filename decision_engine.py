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
        
        energy = self.calculate_energy(focus_score, violations)
    
        if energy > 50: 
            new_work = current_work_time - 5
        elif energy < 15:
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
    
class GeneticScheduler:
    """
    Haftalık planı optimize eden Genetik Algoritma sınıfı.
    """
    def __init__(self, courses, focus_history):
        self.courses = courses
        self.focus_history = focus_history
        self.population_size = 10

    def calculate_fitness(self, schedule):
        score = 0
        for slot, course in schedule.items():
            hour_performance = self.focus_history.get(slot, 50)
            score += hour_performance
        return score

    def generate_optimal_plan(self):
        # Basit bir optimizasyon: En iyi saatlere dersleri yerleştirir
        sorted_slots = sorted(self.focus_history.items(), key=lambda x: x[1], reverse=True)
        best_plan = {}
        for i, course in enumerate(self.courses):
            if i < len(sorted_slots):
                slot_time = sorted_slots[i][0]
                best_plan[slot_time] = course
        return best_plan