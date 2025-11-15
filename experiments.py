"""
Experimenty pre testovanie kooperatívneho koevolučného algoritmu

Tento skript spúšťa experimenty s rôznymi konfiguráciami a zbiera výsledky.
"""

import numpy as np
import time
import json
from cooperative_coevolution import CooperativeCoevolution
from problems import (
    get_rastrigin_problem,
    get_model_optimization_problem,
    get_optimal_value_rastrigin,
    get_optimal_value_model
)


class ExperimentRunner:
    """Spúšťa experimenty a zbiera výsledky"""
    
    def __init__(self, num_runs=10):
        # Koľkokrát spustíme každý experiment (pre spoľahlivejšie výsledky)
        self.num_runs = num_runs
        # Zoznam všetkých výsledkov
        self.results = []
    
    def run_experiment(self, problem_name, fitness_function, dimensions, bounds, config):
        """
        Spustí experiment s danou konfiguráciou
        
        Parametre:
        - problem_name: názov problému (napr. "Rastrigin")
        - fitness_function: funkcia na hodnotenie
        - dimensions: počet dimenzií
        - bounds: hranice pre hodnoty
        - config: slovník s konfiguráciou algoritmu
        """
        print(f"\n{'='*60}")
        print(f"Experiment: {problem_name}")
        print(f"Konfigurácia: {config}")
        print(f"{'='*60}\n")
        
        # Zoznamy pre ukladanie výsledkov zo všetkých behov
        all_fitnesses = []      # všetky fitness hodnoty
        all_solutions = []      # všetky riešenia
        all_times = []          # všetky časy behu
        convergence_data = []   # história konvergencie pre každý beh
        
        # Spustíme experiment viackrát
        for run in range(self.num_runs):
            print(f"Beh {run + 1}/{self.num_runs}")
            
            # Zmeriame čas
            start_time = time.time()
            
            # Vytvoríme algoritmus s danou konfiguráciou
            ccea = CooperativeCoevolution(
                fitness_function=fitness_function,
                dimensions=dimensions,
                bounds=bounds,
                num_species=config['num_species'],
                population_size=config['population_size'],
                generations=config['generations'],
                mutation_rate=config['mutation_rate'],
                crossover_rate=config['crossover_rate'],
                collaboration_size=config['collaboration_size']
            )
            
            # Spustíme algoritmus
            best_solution, best_fitness = ccea.run()
            
            # Zmeriame čas behu
            elapsed_time = time.time() - start_time
            
            # Uložíme výsledky
            all_fitnesses.append(best_fitness)
            all_solutions.append(best_solution)
            all_times.append(elapsed_time)
            convergence_data.append(ccea.best_fitness_history)
            
            print(f"  Fitness: {best_fitness:.6f}, Čas: {elapsed_time:.2f}s\n")
        
        # Vypočítame štatistiky
        fitnesses_array = np.array(all_fitnesses)
        
        # Vytvoríme slovník s výsledkami
        results = {
            'problem': problem_name,
            'config': config,
            'num_runs': self.num_runs,
            'fitness_mean': float(np.mean(fitnesses_array)),      # priemer
            'fitness_std': float(np.std(fitnesses_array)),       # štandardná odchýlka
            'fitness_min': float(np.min(fitnesses_array)),       # minimum
            'fitness_max': float(np.max(fitnesses_array)),       # maximum
            'time_mean': float(np.mean(all_times)),              # priemerný čas
            'time_std': float(np.std(all_times)),                # štandardná odchýlka času
            'convergence': self._average_convergence(convergence_data),  # priemerná konvergencia
            'all_fitnesses': [float(f) for f in all_fitnesses]   # všetky fitness hodnoty
        }
        
        return results
    
    def _average_convergence(self, convergence_data):
        """
        Vypočíta priemernú konvergenciu cez všetky behy
        
        convergence_data: zoznam zoznamov - každý zoznam obsahuje históriu jedného behu
        """
        # Nájdeme najdlhšiu históriu
        max_gen = 0
        for conv in convergence_data:
            if len(conv) > max_gen:
                max_gen = len(conv)
        
        # Pre každú generáciu vypočítame priemer cez všetky behy
        averaged = []
        for gen in range(max_gen):
            values = []
            for conv in convergence_data:
                if gen < len(conv):
                    values.append(conv[gen])
            if values:
                averaged.append(float(np.mean(values)))
        
        return averaged
    
    def print_results(self, results):
        """Vytlačí výsledky experimentu"""
        print(f"\n{'='*60}")
        print(f"Výsledky: {results['problem']}")
        print(f"{'='*60}")
        print(f"Konfigurácia:")
        for key, value in results['config'].items():
            print(f"  {key}: {value}")
        print(f"\nŠtatistiky (cez {results['num_runs']} behov):")
        print(f"  Priemerná fitness: {results['fitness_mean']:.6f} ± {results['fitness_std']:.6f}")
        print(f"  Najlepšia fitness: {results['fitness_max']:.6f}")
        print(f"  Najhoršia fitness: {results['fitness_min']:.6f}")
        print(f"  Priemerný čas: {results['time_mean']:.2f}s ± {results['time_std']:.2f}s")
        print(f"{'='*60}\n")


def main():
    """Hlavná funkcia pre spustenie experimentov"""
    
    # Vytvoríme runner, ktorý spustí každý experiment 10-krát
    runner = ExperimentRunner(num_runs=10)
    all_results = []
    
    # ========================================================================
    # PROBLÉM 1: Rastrigin funkcia
    # ========================================================================
    
    print("\n" + "="*60)
    print("PROBLÉM 1: Optimalizácia Rastrigin funkcie")
    print("="*60)
    
    dimensions = 30
    fitness_func, dims, bounds = get_rastrigin_problem(dimensions)
    optimal_value = get_optimal_value_rastrigin(dimensions)
    
    # Rôzne konfigurácie pre testovanie
    configs = [
        {
            'name': 'Základná konfigurácia',
            'num_species': 4,
            'population_size': 50,
            'generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'collaboration_size': 1
        },
        {
            'name': 'Viac druhov',
            'num_species': 8,
            'population_size': 50,
            'generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'collaboration_size': 1
        },
        {
            'name': 'Väčšia populácia',
            'num_species': 4,
            'population_size': 100,
            'generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'collaboration_size': 1
        },
        {
            'name': 'Viac generácií',
            'num_species': 4,
            'population_size': 50,
            'generations': 200,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'collaboration_size': 1
        },
        {
            'name': 'Náhodní spolupracovníci',
            'num_species': 4,
            'population_size': 50,
            'generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'collaboration_size': 3
        }
    ]
    
    # Spustíme každú konfiguráciu
    for config in configs:
        config_name = config['name']
        # Vytvoríme kópiu konfigurácie bez názvu (ten nepotrebujeme v algoritme)
        config_copy = {}
        for k, v in config.items():
            if k != 'name':
                config_copy[k] = v
        
        # Spustíme experiment
        result = runner.run_experiment(
            problem_name=f"Rastrigin - {config_name}",
            fitness_function=fitness_func,
            dimensions=dimensions,
            bounds=bounds,
            config=config_copy
        )
        
        # Pridáme názov konfigurácie a optimálnu hodnotu
        result['config_name'] = config_name
        result['optimal_value'] = optimal_value
        all_results.append(result)
        
        # Vytlačíme výsledky
        runner.print_results(result)
    
    # ========================================================================
    # PROBLÉM 2: Optimalizácia parametrov modelu
    # ========================================================================
    
    print("\n" + "="*60)
    print("PROBLÉM 2: Optimalizácia parametrov matematického modelu")
    print("="*60)
    
    dimensions = 20
    fitness_func, dims, bounds = get_model_optimization_problem(dimensions)
    optimal_value = get_optimal_value_model(dimensions)
    
    # Rôzne konfigurácie pre testovanie
    configs = [
        {
            'name': 'Základná konfigurácia',
            'num_species': 4,
            'population_size': 50,
            'generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'collaboration_size': 1
        },
        {
            'name': 'Viac druhov',
            'num_species': 5,
            'population_size': 50,
            'generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'collaboration_size': 1
        },
        {
            'name': 'Väčšia populácia',
            'num_species': 4,
            'population_size': 100,
            'generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'collaboration_size': 1
        },
        {
            'name': 'Náhodní spolupracovníci',
            'num_species': 4,
            'population_size': 50,
            'generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'collaboration_size': 3
        }
    ]
    
    # Spustíme každú konfiguráciu
    for config in configs:
        config_name = config['name']
        # Vytvoríme kópiu konfigurácie bez názvu
        config_copy = {}
        for k, v in config.items():
            if k != 'name':
                config_copy[k] = v
        
        # Spustíme experiment
        result = runner.run_experiment(
            problem_name=f"Model - {config_name}",
            fitness_function=fitness_func,
            dimensions=dimensions,
            bounds=bounds,
            config=config_copy
        )
        
        # Pridáme názov konfigurácie a optimálnu hodnotu
        result['config_name'] = config_name
        result['optimal_value'] = optimal_value
        all_results.append(result)
        
        # Vytlačíme výsledky
        runner.print_results(result)
    
    # ========================================================================
    # Uloženie výsledkov
    # ========================================================================
    
    # Uložíme výsledky do JSON súboru
    with open('experiment_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "="*60)
    print("Všetky experimenty dokončené!")
    print("Výsledky uložené do 'experiment_results.json'")
    print("="*60)


if __name__ == '__main__':
    main()
