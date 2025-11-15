"""
Kooperatívny koevolučný algoritmus (CCEA)

Jednoduchá implementácia algoritmu, ktorý rozdeľuje veľký problém na menšie časti.
Každá časť sa rieši samostatne pomocou genetického algoritmu.
"""

import numpy as np
import random


class Individual:
    """Jeden jedinec v populácii - má svoje gény a fitness hodnotu"""
    
    def __init__(self, genes, fitness=-999999):
        # Gény = hodnoty riešenia (napr. [1.5, -2.3, 0.8, ...])
        self.genes = genes
        # Fitness = ako dobré je toto riešenie (čím väčšie, tým lepšie)
        self.fitness = fitness
    
    def copy(self):
        """Vytvorí kópiu jedinca"""
        return Individual(self.genes.copy(), self.fitness)


class Population:
    """Populácia = skupina jedincov, ktorí sa vyvíjajú"""
    
    def __init__(self, size, dimension, bounds):
        # Koľko jedincov je v populácii
        self.size = size
        # Koľko dimenzií má každý jedinec (koľko čísel v génoch)
        self.dimension = dimension
        # Hranice pre hodnoty génov (min, max)
        self.bounds = bounds
        # Zoznam všetkých jedincov
        self.individuals = []
        # Vytvoríme počiatočnú populáciu
        self._create_initial_population()
    
    def _create_initial_population(self):
        """Vytvorí počiatočnú populáciu náhodnými jedincami"""
        self.individuals = []
        for i in range(self.size):
            # Vytvoríme náhodné gény v rámci hraníc
            genes = np.random.uniform(
                self.bounds[0],  # minimálna hodnota
                self.bounds[1],  # maximálna hodnota
                self.dimension   # koľko čísel
            )
            # Pridáme nového jedinca
            self.individuals.append(Individual(genes))
    
    def get_best(self):
        """Vráti najlepšieho jedinca (s najväčšou fitness)"""
        best = self.individuals[0]
        for ind in self.individuals:
            if ind.fitness > best.fitness:
                best = ind
        return best
    
    def get_random_individual(self):
        """Vráti náhodného jedinca z populácie"""
        return random.choice(self.individuals)


class GeneticAlgorithm:
    """Genetický algoritmus - vyvíja jednu populáciu"""
    
    def __init__(self, population, mutation_rate=0.1, crossover_rate=0.8):
        self.population = population
        # Pravdepodobnosť, že sa gén zmení (mutácia)
        self.mutation_rate = mutation_rate
        # Pravdepodobnosť, že sa dvaja rodičia skrížia
        self.crossover_rate = crossover_rate
    
    def selection(self):
        """Turnajová selekcia - vyberie najlepších jedincov"""
        # Veľkosť turnaja (10% populácie, minimálne 2)
        tournament_size = max(2, int(self.population.size * 0.1))
        selected = []
        
        # Pre každého jedinca v novej populácii
        for i in range(self.population.size):
            # Vyberieme náhodných jedincov do turnaja
            tournament = random.sample(
                self.population.individuals, 
                tournament_size
            )
            # Vyberieme víťaza turnaja (najlepšieho)
            winner = tournament[0]
            for ind in tournament:
                if ind.fitness > winner.fitness:
                    winner = ind
            # Pridáme víťaza do vybraných
            selected.append(winner.copy())
        
        return selected
    
    def crossover(self, parent1, parent2):
        """Kríženie - vytvorí dvoch potomkov z dvoch rodičov"""
        # Niekedy sa nekrížime, len vrátime rodičov
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        # Vytvoríme nové gény kombináciou rodičovských génov
        alpha = random.random()  # náhodné číslo medzi 0 a 1
        
        # Prvý potomok: kombinácia génov rodičov
        genes1 = alpha * parent1.genes + (1 - alpha) * parent2.genes
        # Druhý potomok: opačná kombinácia
        genes2 = (1 - alpha) * parent1.genes + alpha * parent2.genes
        
        return Individual(genes1), Individual(genes2)
    
    def mutation(self, individual):
        """Mutácia - náhodne zmení niektoré gény"""
        for i in range(len(individual.genes)):
            # S určitou pravdepodobnosťou zmeníme gén
            if random.random() < self.mutation_rate:
                # O koľko zmeníme (10% z rozsahu hraníc)
                mutation_strength = (self.population.bounds[1] - self.population.bounds[0]) * 0.1
                # Pridáme náhodnú zmenu (normálne rozdelenie)
                individual.genes[i] += np.random.normal(0, mutation_strength)
                # Uistíme sa, že hodnota je stále v hraniciach
                if individual.genes[i] < self.population.bounds[0]:
                    individual.genes[i] = self.population.bounds[0]
                if individual.genes[i] > self.population.bounds[1]:
                    individual.genes[i] = self.population.bounds[1]
    
    def evolve(self, evaluate_func):
        """Vykoná jednu generáciu evolúcie"""
        # 1. Selekcia - vyberieme najlepších
        selected = self.selection()
        
        # 2. Kríženie a mutácia - vytvoríme novú generáciu
        new_population = []
        for i in range(0, len(selected), 2):
            if i + 1 < len(selected):
                # Máme pár rodičov - vytvoríme potomkov
                child1, child2 = self.crossover(selected[i], selected[i + 1])
            else:
                # Nemáme pár - len skopírujeme
                child1 = selected[i].copy()
                child2 = selected[i].copy()
            
            # Mutácia potomkov
            self.mutation(child1)
            self.mutation(child2)
            
            # Pridáme do novej populácie
            new_population.append(child1)
            new_population.append(child2)
        
        # Zmenšiť na pôvodnú veľkosť (ak sme vytvorili viac)
        new_population = new_population[:self.population.size]
        
        # 3. Evaluácia - ohodnotíme každého jedinca
        for individual in new_population:
            individual.fitness = evaluate_func(individual)
        
        # 4. Nahradenie populácie
        self.population.individuals = new_population
        
        # 5. Elitizmus - zachováme najlepšieho z predchádzajúcej generácie
        best_old = self.population.get_best()
        worst_new = new_population[0]
        for ind in new_population:
            if ind.fitness < worst_new.fitness:
                worst_new = ind
        
        # Ak bol najlepší z predchádzajúcej generácie lepší, zachováme ho
        if best_old.fitness > worst_new.fitness:
            worst_new.genes = best_old.genes.copy()
            worst_new.fitness = best_old.fitness


class CooperativeCoevolution:
    """Kooperatívny koevolučný algoritmus - hlavná trieda"""
    
    def __init__(
        self,
        fitness_function,
        dimensions,
        bounds,
        num_species=4,
        population_size=50,
        generations=100,
        mutation_rate=0.1,
        crossover_rate=0.8,
        collaboration_size=1
    ):
        """
        Parametre:
        - fitness_function: funkcia, ktorá hodnotí riešenie (čím väčšie, tým lepšie)
        - dimensions: koľko dimenzií má problém (napr. 30)
        - bounds: hranice pre hodnoty (min, max)
        - num_species: na koľko častí rozdelíme problém (napr. 4)
        - population_size: koľko jedincov je v každej populácii
        - generations: koľko generácií budeme evolvovať
        - mutation_rate: pravdepodobnosť mutácie
        - crossover_rate: pravdepodobnosť kríženia
        - collaboration_size: koľko partnerov použijeme pri hodnotení (1 = najlepší, >1 = náhodný)
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
        
        # Rozdelíme dimenzie medzi druhy (napr. 30 dimenzií / 4 druhy = 7-8 dimenzií na druh)
        self.dimensions_per_species = self._split_dimensions()
        
        # Vytvoríme populácie pre každý druh
        self.populations = []
        self.genetic_algorithms = []
        
        for dims in self.dimensions_per_species:
            # Vytvoríme populáciu pre tento druh
            pop = Population(population_size, dims, bounds)
            # Vytvoríme genetický algoritmus pre túto populáciu
            ga = GeneticAlgorithm(pop, mutation_rate, crossover_rate)
            self.populations.append(pop)
            self.genetic_algorithms.append(ga)
        
        # História pre sledovanie vývoja
        self.best_fitness_history = []
        self.best_solution_history = []
    
    def _split_dimensions(self):
        """Rozdelí dimenzie medzi druhy"""
        # Základný počet dimenzií na druh
        base_dims = self.dimensions // self.num_species
        # Zvyšné dimenzie (ak sa nedelí rovnomerne)
        extra_dims = self.dimensions % self.num_species
        
        # Vytvoríme zoznam počtu dimenzií pre každý druh
        dimensions = [base_dims] * self.num_species
        # Rozdelíme zvyšné dimenzie medzi prvé druhy
        for i in range(extra_dims):
            dimensions[i] += 1
        
        return dimensions
    
    def _evaluate_individual(self, species_index, individual, collaborators=None):
        """
        Ohodnotí jedinca - musí spolupracovať s jedincami z iných druhov
        
        species_index: ktorý druh hodnotíme (0, 1, 2, ...)
        individual: jedinec, ktorého hodnotíme
        collaborators: spolupracovníci z iných druhov (ak nie je zadaný, vyberieme náhodne)
        """
        # Ak nemáme spolupracovníkov, vyberieme ich
        if collaborators is None:
            collaborators = []
            for i, pop in enumerate(self.populations):
                if i == species_index:
                    continue  # Preskočíme náš vlastný druh
                
                if self.collaboration_size == 1:
                    # Použijeme najlepšieho z každej populácie
                    collaborators.append([pop.get_best()])
                else:
                    # Vyberieme náhodných spolupracovníkov
                    collab_list = []
                    for j in range(self.collaboration_size):
                        collab_list.append(pop.get_random_individual())
                    collaborators.append(collab_list)
        
        # Zostavíme kompletný vektor riešenia (všetky dimenzie)
        solution = np.zeros(self.dimensions)
        
        # Vložíme gény aktuálneho jedinca na správne miesto
        start_idx = 0
        for i in range(species_index):
            start_idx += self.dimensions_per_species[i]
        end_idx = start_idx + self.dimensions_per_species[species_index]
        solution[start_idx:end_idx] = individual.genes
        
        # Vložíme gény spolupracovníkov z iných druhov
        collab_idx = 0
        for i, pop in enumerate(self.populations):
            if i == species_index:
                continue  # Preskočíme náš vlastný druh
            
            # Nájdeme správne miesto pre tento druh
            start_idx = 0
            for j in range(i):
                start_idx += self.dimensions_per_species[j]
            end_idx = start_idx + self.dimensions_per_species[i]
            
            # Vyberieme jedného spolupracovníka
            if self.collaboration_size == 1:
                partner = collaborators[collab_idx][0]
            else:
                partner = random.choice(collaborators[collab_idx])
            
            # Vložíme jeho gény
            solution[start_idx:end_idx] = partner.genes
            collab_idx += 1
        
        # Ohodnotíme kompletný vektor
        return self.fitness_function(solution)
    
    def _evaluate_population(self, species_index):
        """Ohodnotí celú populáciu daného druhu"""
        for individual in self.populations[species_index].individuals:
            individual.fitness = self._evaluate_individual(species_index, individual)
    
    def _get_best_solution(self):
        """Vráti najlepšie riešenie - zostavené z najlepších jedincov z každej populácie"""
        solution = np.zeros(self.dimensions)
        
        for i, pop in enumerate(self.populations):
            # Nájdeme správne miesto pre tento druh
            start_idx = 0
            for j in range(i):
                start_idx += self.dimensions_per_species[j]
            end_idx = start_idx + self.dimensions_per_species[i]
            
            # Vezmeme najlepšieho jedinca z tejto populácie
            best = pop.get_best()
            solution[start_idx:end_idx] = best.genes
        
        # Ohodnotíme toto riešenie
        fitness = self.fitness_function(solution)
        return solution, fitness
    
    def run(self):
        """Spustí kooperatívny koevolučný algoritmus"""
        # 1. Počiatočná evaluácia - ohodnotíme všetky populácie
        for i in range(self.num_species):
            self._evaluate_population(i)
        
        # 2. Hlavný evolučný cyklus
        for generation in range(self.generations):
            # Evoluujeme každú populáciu
            for i in range(self.num_species):
                # Vytvoríme funkciu, ktorá hodnotí jedinca tohto druhu
                def evaluate_func(ind):
                    return self._evaluate_individual(i, ind)
                
                # Evoluujeme populáciu
                self.genetic_algorithms[i].evolve(evaluate_func)
            
            # Zaznamenáme najlepšie riešenie
            best_solution, best_fitness = self._get_best_solution()
            self.best_fitness_history.append(best_fitness)
            self.best_solution_history.append(best_solution.copy())
            
            # Každých 10 generácií vypíšeme pokrok
            if (generation + 1) % 10 == 0:
                print(f"Generácia {generation + 1}/{self.generations}, "
                      f"najlepšia fitness: {best_fitness:.6f}")
        
        # Vrátime najlepšie riešenie
        return self._get_best_solution()
