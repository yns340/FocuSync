import random
import math

class FocusDecisionEngine:
    def __init__(self):
        self.MIN_WORK = 15
        self.MAX_WORK = 60

    def calculate_energy(self, focus_score, violations):
        return (100 - focus_score) + (violations * 5)

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
        if not past_sessions: return 25
        best_ones = sorted(past_sessions, key=lambda x: x.get('focus_score', 0), reverse=True)[:5]
        avg_time = sum(s.get('duration', 25) for s in best_ones) / len(best_ones)
        return int(avg_time)
    
class GeneticScheduler:
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
        sorted_slots = sorted(self.focus_history.items(), key=lambda x: x[1], reverse=True)
        best_plan = {}
        for i, course in enumerate(self.courses):
            if i < len(sorted_slots):
                slot_time = sorted_slots[i][0]
                best_plan[slot_time] = course
        return best_plan

# 🔥 YENİ: SRS 3.2.7.2'ye Uygun Simulated Annealing Motoru
class SimulatedAnnealingScheduler:
    """
    Ders programını 'Enerji' (Verimsizlik) değerini minimize ederek optimize eder.
    """
    def __init__(self, courses, focus_history, temp=100.0, cooling_rate=0.95):
        self.courses = courses # Liste: ["Ders1", "Ders2"]
        self.history = focus_history # Sözlük: {"09:00": 80, "10:00": 40}
        self.T = temp
        self.cooling_rate = cooling_rate

    def calculate_energy(self, schedule):
        """Programın toplam verimsizlik skorunu hesaplar."""
        total_energy = 0
        for slot, course_name in schedule.items():
            # Geçmiş performans düşükse enerji yüksek çıkar (istenmeyen durum)
            perf = self.history.get(slot, 50)
            total_energy += (100 - perf)
        return total_energy

    def generate_plan(self):
        """Benzetimli Tavlama ile global optimum planı bulur."""
        # 1. Başlangıç Programı (Rastgele)
        slots = list(self.history.keys())
        current_schedule = {}
        for i, c in enumerate(self.courses):
            if i < len(slots): current_schedule[slots[i]] = c
        
        current_energy = self.calculate_energy(current_schedule)
        
        # 2. Soğutma Döngüsü
        while self.T > 1.0:
            # Komşu bir çözüm üret (Derslerin yerini değiştir)
            new_schedule = current_schedule.copy()
            if len(slots) >= 2:
                s1, s2 = random.sample(slots, 2)
                if s1 in new_schedule and s2 in new_schedule:
                    new_schedule[s1], new_schedule[s2] = new_schedule[s2], new_schedule[s1]
            
            new_energy = self.calculate_energy(new_schedule)
            
            # Kabul etme kriteri (Metropolis Algoritması)
            if new_energy < current_energy:
                current_schedule, current_energy = new_schedule, new_energy
            else:
                # Kötü çözümü sıcaklığa bağlı kabul et (Yerel optimumdan kaçış)
                delta = new_energy - current_energy
                if random.random() < math.exp(-delta / self.T):
                    current_schedule, current_energy = new_schedule, new_energy
            
            self.T *= self.cooling_rate # Soğutma
            
        return current_schedule