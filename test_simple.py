"""
Jednoduchý test na overenie funkčnosti algoritmu
"""

import numpy as np
from cooperative_coevolution import CooperativeCoevolution
from problems import get_rastrigin_problem, get_model_optimization_problem


def test_rastrigin():
    """Test Rastrigin problému"""
    print("Test Rastrigin funkcie (10 dimenzií, 2 druhy, 20 jedincov, 20 generácií)...")
    
    dimensions = 10
    fitness_func, dims, bounds = get_rastrigin_problem(dimensions)
    
    ccea = CooperativeCoevolution(
        fitness_function=fitness_func,
        dimensions=dimensions,
        bounds=bounds,
        num_species=2,
        population_size=20,
        generations=20,
        mutation_rate=0.1,
        crossover_rate=0.8,
        collaboration_size=1
    )
    
    best_solution, best_fitness = ccea.run()
    
    # Pre Rastrigin je optimálna hodnota 0, ale algoritmus maximalizuje (negatívna hodnota)
    # Takže lepšie riešenie má vyššiu (menej negatívnu) fitness
    actual_value = -best_fitness  # Pretože fitness je negatívna
    
    print(f"  Najlepšie riešenie: {best_solution[:5]}... (zobrazených prvých 5 dimenzií)")
    print(f"  Fitness: {best_fitness:.6f}")
    print(f"  Skutočná hodnota Rastrigin: {actual_value:.6f}")
    print(f"  Optimálna hodnota: 0.0")
    print(f"  Vzdialenosť od optima: {actual_value:.6f}")
    print("  ✓ Test prebehol úspešne\n")
    
    return best_fitness


def test_model():
    """Test optimalizácie modelu"""
    print("Test optimalizácie modelu (8 dimenzií, 2 druhy, 20 jedincov, 20 generácií)...")
    
    dimensions = 8
    fitness_func, dims, bounds = get_model_optimization_problem(dimensions)
    
    ccea = CooperativeCoevolution(
        fitness_function=fitness_func,
        dimensions=dimensions,
        bounds=bounds,
        num_species=2,
        population_size=20,
        generations=20,
        mutation_rate=0.1,
        crossover_rate=0.8,
        collaboration_size=1
    )
    
    best_solution, best_fitness = ccea.run()
    
    actual_value = -best_fitness  # Pretože fitness je negatívna
    
    print(f"  Najlepšie riešenie: {best_solution}")
    print(f"  Fitness: {best_fitness:.6f}")
    print(f"  Skutočná hodnota chyby: {actual_value:.6f}")
    print(f"  Optimálna hodnota: 0.0")
    print(f"  Vzdialenosť od optima: {actual_value:.6f}")
    print("  ✓ Test prebehol úspešne\n")
    
    return best_fitness


if __name__ == '__main__':
    print("="*60)
    print("Jednoduché testy kooperatívneho koevolučného algoritmu")
    print("="*60)
    print()
    
    try:
        test_rastrigin()
        test_model()
        
        print("="*60)
        print("Všetky testy prebehli úspešne!")
        print("="*60)
    except Exception as e:
        print(f"Chyba pri testovaní: {e}")
        import traceback
        traceback.print_exc()

