"""
Kooperatívny koevolučný algoritmus (Cooperative Coevolutionary Algorithm - CCEA)

Algoritmus rozdeľuje komplexný problém na menšie podproblémy, ktoré sa riešia paralelne
pomocou nezávislých evolúcií. Rôzne populácie interagujú spolu cez spoločné hodnotenie.
"""

import numpy as np
import random
from typing import List, Callable, Tuple


class Individual:
    """Reprezentácia jedinca v populácii"""
    
    def __init__(self, genes: np.ndarray, fitness: float = float('-inf')):
        self.genes = genes
        self.fitness = fitness
    
    def copy(self):
        return Individual(self.genes.copy(), self.fitness)


class Population:
    """Populácia jedincov"""
    
    def __init__(self, size: int, dimension: int, bounds: Tuple[float, float]):
        self.size = size
        self.dimension = dimension
        self.bounds = bounds
        self.individuals = []
        self._initialize_population()
    
    def _initialize_population(self):
        """Inicializácia populácie náhodnými jedincami"""
        self.individuals = []
        for _ in range(self.size):
            genes = np.random.uniform(
                self.bounds[0], 
                self.bounds[1], 
                self.dimension
            )
            self.individuals.append(Individual(genes))
    
    def get_best(self) -> Individual:
        """Vráti najlepšieho jedinca"""
        return max(self.individuals, key=lambda x: x.fitness)
    
    def get_random_individual(self) -> Individual:
        """Vráti náhodného jedinca"""
        return random.choice(self.individuals)


class GeneticAlgorithm:
    """Genetický algoritmus pre evolúciu jednej populácie"""
    
    def __init__(
        self,
        population: Population,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.8,
        selection_pressure: float = 2.0
    ):
        self.population = population
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.selection_pressure = selection_pressure
    
    def selection(self) -> List[Individual]:
        """Turnajová selekcia"""
        tournament_size = max(2, int(self.population.size * 0.1))
        selected = []
        
        for _ in range(self.population.size):
            tournament = random.sample(
                self.population.individuals, 
                tournament_size
            )
            winner = max(tournament, key=lambda x: x.fitness)
            selected.append(winner.copy())
        
        return selected
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Arithmetický crossover"""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        alpha = random.random()
        genes1 = alpha * parent1.genes + (1 - alpha) * parent2.genes
        genes2 = (1 - alpha) * parent1.genes + alpha * parent2.genes
        
        return Individual(genes1), Individual(genes2)
    
    def mutation(self, individual: Individual):
        """Gaussovská mutácia"""
        for i in range(len(individual.genes)):
            if random.random() < self.mutation_rate:
                mutation_strength = (self.population.bounds[1] - self.population.bounds[0]) * 0.1
                individual.genes[i] += np.random.normal(0, mutation_strength)
                # Orezanie na hranice
                individual.genes[i] = np.clip(
                    individual.genes[i],
                    self.population.bounds[0],
                    self.population.bounds[1]
                )
    
    def evolve(self, evaluate_func: Callable):
        """Vykoná jednu generáciu evolúcie"""
        # Selekcia
        selected = self.selection()
        
        # Kríženie a mutácia
        new_population = []
        for i in range(0, len(selected), 2):
            if i + 1 < len(selected):
                child1, child2 = self.crossover(selected[i], selected[i + 1])
            else:
                child1 = selected[i].copy()
                child2 = selected[i].copy()
            
            self.mutation(child1)
            self.mutation(child2)
            
            new_population.extend([child1, child2])
        
        # Zmenšiť na pôvodnú veľkosť
        new_population = new_population[:self.population.size]
        
        # Evaluácia
        for individual in new_population:
            individual.fitness = evaluate_func(individual)
        
        # Nahradenie populácie
        self.population.individuals = new_population
        
        # Elitizmus - zachovať najlepšieho
        best_old = self.population.get_best()
        worst_new = min(new_population, key=lambda x: x.fitness)
        if best_old.fitness > worst_new.fitness:
            worst_new.genes = best_old.genes.copy()
            worst_new.fitness = best_old.fitness


class CooperativeCoevolution:
    """Kooperatívny koevolučný algoritmus"""
    
    def __init__(
        self,
        fitness_function: Callable,
        dimensions: int,
        bounds: Tuple[float, float],
        num_species: int = 4,
        population_size: int = 50,
        generations: int = 100,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.8,
        collaboration_size: int = 1
    ):
        """
        Args:
            fitness_function: Funkcia na hodnotenie (prijíma numpy array)
            dimensions: Celkový počet dimenzií problému
            bounds: Hranice pre každú dimenziu (min, max)
            num_species: Počet druhov/populácií (rozdelenie dimenzií)
            population_size: Veľkosť každej populácie
            generations: Počet generácií
            mutation_rate: Pravdepodobnosť mutácie
            crossover_rate: Pravdepodobnosť kríženia
            collaboration_size: Počet partnerov pri hodnotení (1 = best, >1 = random)
        """
        self.fitness_function = fitness_function
        self.dimensions = dimensions
        self.bounds = bounds
        self.num_species = num_species
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.collaboration_size = collaboration_size
        
        # Rozdelenie dimenzií medzi druhy
        self.dimensions_per_species = self._split_dimensions()
        
        # Inicializácia populácií
        self.populations = []
        self.genetic_algorithms = []
        
        for dims in self.dimensions_per_species:
            pop = Population(population_size, dims, bounds)
            ga = GeneticAlgorithm(pop, mutation_rate, crossover_rate)
            self.populations.append(pop)
            self.genetic_algorithms.append(ga)
        
        # História pre sledovanie vývoja
        self.best_fitness_history = []
        self.best_solution_history = []
    
    def _split_dimensions(self) -> List[int]:
        """Rozdelí dimenzie medzi druhy"""
        base_dims = self.dimensions // self.num_species
        extra_dims = self.dimensions % self.num_species
        
        dimensions = [base_dims] * self.num_species
        for i in range(extra_dims):
            dimensions[i] += 1
        
        return dimensions
    
    def _evaluate_individual(
        self, 
        species_index: int, 
        individual: Individual,
        collaborators: List[List[Individual]] = None
    ) -> float:
        """Hodnotí jedinca v kontexte ostatných druhov"""
        if collaborators is None:
            # Vyberie náhodných spolupracovníkov z ostatných druhov
            collaborators = []
            for i, pop in enumerate(self.populations):
                if i == species_index:
                    continue
                
                if self.collaboration_size == 1:
                    # Použiť najlepšieho z každej populácie
                    collaborators.append([pop.get_best()])
                else:
                    # Vybrať náhodných spolupracovníkov
                    collaborators.append([
                        pop.get_random_individual() 
                        for _ in range(self.collaboration_size)
                    ])
        
        # Zostaviť kompletný vektor riešenia
        solution = np.zeros(self.dimensions)
        
        # Vložiť gény aktuálneho jedinca
        start_idx = sum(self.dimensions_per_species[:species_index])
        end_idx = start_idx + self.dimensions_per_species[species_index]
        solution[start_idx:end_idx] = individual.genes
        
        # Vložiť gény spolupracovníkov
        collab_idx = 0
        for i, pop in enumerate(self.populations):
            if i == species_index:
                continue
            
            start_idx = sum(self.dimensions_per_species[:i])
            end_idx = start_idx + self.dimensions_per_species[i]
            
            # Vybrať jedného spolupracovníka (najlepšieho alebo náhodného)
            if self.collaboration_size == 1:
                partner = collaborators[collab_idx][0]
            else:
                partner = random.choice(collaborators[collab_idx])
            
            solution[start_idx:end_idx] = partner.genes
            collab_idx += 1
        
        # Evaluovať kompletný vektor
        return self.fitness_function(solution)
    
    def _evaluate_population(self, species_index: int):
        """Hodnotí celú populáciu daného druhu"""
        for individual in self.populations[species_index].individuals:
            individual.fitness = self._evaluate_individual(species_index, individual)
    
    def _get_best_solution(self) -> Tuple[np.ndarray, float]:
        """Vráti najlepšie riešenie zostavené z najlepších jedincov z každej populácie"""
        solution = np.zeros(self.dimensions)
        
        for i, pop in enumerate(self.populations):
            start_idx = sum(self.dimensions_per_species[:i])
            end_idx = start_idx + self.dimensions_per_species[i]
            best = pop.get_best()
            solution[start_idx:end_idx] = best.genes
        
        fitness = self.fitness_function(solution)
        return solution, fitness
    
    def run(self) -> Tuple[np.ndarray, float]:
        """Spustí kooperatívny koevolučný algoritmus"""
        # Počiatočná evaluácia
        for i in range(self.num_species):
            self._evaluate_population(i)
        
        # Hlavný evolučný cyklus
        for generation in range(self.generations):
            # Evolúcia každej populácie
            for i in range(self.num_species):
                # Vytvoriť evaluačnú funkciu pre tento druh
                def evaluate_func(ind):
                    return self._evaluate_individual(i, ind)
                
                # Evoluovať populáciu
                self.genetic_algorithms[i].evolve(evaluate_func)
            
            # Zaznamenať najlepšie riešenie
            best_solution, best_fitness = self._get_best_solution()
            self.best_fitness_history.append(best_fitness)
            self.best_solution_history.append(best_solution.copy())
            
            if (generation + 1) % 10 == 0:
                print(f"Generácia {generation + 1}/{self.generations}, "
                      f"najlepšia fitness: {best_fitness:.6f}")
        
        # Vrátiť najlepšie riešenie
        return self._get_best_solution()

