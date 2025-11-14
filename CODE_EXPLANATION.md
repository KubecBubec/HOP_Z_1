# Kompletný prehľad kódu - Kooperatívny koevolučný algoritmus

## 📋 Obsah
1. [cooperative_coevolution.py - Detailný prehľad](#1-cooperative_coevolutionpy)
2. [problems.py - Všetky funkcie](#2-problemspy)
3. [experiments.py - Celý workflow](#3-experimentspy)
4. [Ako to všetko spolupracuje](#4-ako-to-všetko-spolupracuje)

---

## 1. cooperative_coevolution.py

### 🎯 Prehľad
Tento súbor obsahuje implementáciu kooperatívneho koevolučného algoritmu (CCEA). Algoritmus rozdeľuje komplexný problém na menšie časti, ktoré sa riešia paralelne pomocou nezávislých genetických algoritmov.

---

### 📦 Trieda: `Individual` (riadky 13-21)

**Účel:** Reprezentuje jedného jedinca v populácii.

```python
class Individual:
    def __init__(self, genes: np.ndarray, fitness: float = float('-inf')):
        self.genes = genes      # Genotyp - hodnoty dimenzií (napr. [0.5, -2.3, 1.1, ...])
        self.fitness = fitness  # Fenotyp - hodnota fitness funkcie
```

**Metódy:**
- `__init__`: Vytvorí jedinca s genami (numpy array) a fitness hodnotou
- `copy()`: Vytvorí kópiu jedinca (dôležité pri selekcii a krížení)

**Príklad:**
- Pre Rastrigin s 10 dimenziami: `genes = [0.1, -0.5, 2.3, ..., 1.2]` (10 čísel)
- `fitness` je hodnota fitness funkcie pre tieto gény

---

### 📦 Trieda: `Population` (riadky 24-51)

**Účel:** Spravuje populáciu jedincov jedného druhu.

```python
class Population:
    def __init__(self, size: int, dimension: int, bounds: Tuple[float, float]):
        self.size = size           # Počet jedincov v populácii (napr. 50)
        self.dimension = dimension  # Počet dimenzií, ktoré tento druh rieši
        self.bounds = bounds        # Hranice pre hodnoty (min, max)
        self.individuals = []       # Zoznam všetkých jedincov
```

**Metódy:**

#### `_initialize_population()` (riadky 34-43)
- **Čo robí:** Vytvorí počiatočnú populáciu náhodnými jedincami
- **Ako:** Pre každého jedinca vygeneruje náhodné hodnoty v rámci `bounds`
- **Príklad:** Pre `size=50`, `dimension=7`, `bounds=(-5.12, 5.12)` vytvorí 50 jedincov, každý s 7 náhodnými hodnotami medzi -5.12 a 5.12

#### `get_best()` (riadky 45-47)
- **Čo robí:** Vráti jedinca s najvyššou fitness hodnotou
- **Ako:** Použije `max()` s kľúčom `fitness`
- **Použitie:** Pri výbere najlepšieho spolupracovníka alebo pri elitizme

#### `get_random_individual()` (riadky 49-51)
- **Čo robí:** Vráti náhodného jedinca z populácie
- **Použitie:** Pri výbere náhodných spolupracovníkov (`collaboration_size > 1`)

---

### 📦 Trieda: `GeneticAlgorithm` (riadky 54-142)

**Účel:** Implementuje genetický algoritmus pre evolúciu jednej populácie.

**Parametre:**
- `population`: Populácia, ktorá sa má vyvíjať
- `mutation_rate`: Pravdepodobnosť mutácie (0.1 = 10%)
- `crossover_rate`: Pravdepodobnosť kríženia (0.8 = 80%)
- `selection_pressure`: Tlak selekcie (nie je aktívne používaný)

**Metódy:**

#### `selection()` (riadky 69-82) - Turnajová selekcia
```python
def selection(self) -> List[Individual]:
    tournament_size = max(2, int(self.population.size * 0.1))
    # Pre populáciu 50: tournament_size = 5
```

**Ako funguje:**
1. Vypočíta veľkosť turnaja (10% populácie, min. 2)
2. Pre každého jedinca v novej populácii:
   - Vyberie náhodne `tournament_size` jedincov
   - Vyberie najlepšieho z turnaja
   - Pridá ho do vybraných
3. Vráti zoznam vybraných jedincov

**Prečo turnajová selekcia:**
- Jednoduchá implementácia
- Umožňuje kontrolovať tlak selekcie (veľkosť turnaja)
- Lepší jedinci majú vyššiu šancu, ale aj horší môžu byť vybraní

#### `crossover()` (riadky 84-93) - Arithmetický crossover
```python
def crossover(self, parent1: Individual, parent2: Individual):
    if random.random() > self.crossover_rate:
        return parent1.copy(), parent2.copy()  # Bez kríženia
    
    alpha = random.random()  # Náhodné číslo 0-1
    genes1 = alpha * parent1.genes + (1 - alpha) * parent2.genes
    genes2 = (1 - alpha) * parent1.genes + alpha * parent2.genes
```

**Ako funguje:**
1. S pravdepodobnosťou `crossover_rate` vykoná kríženie
2. Vytvorí dva potomkov pomocou váženého priemeru génov rodičov
3. `alpha` určuje, koľko z každého rodiča sa použije

**Príklad:**
- `parent1.genes = [1.0, 2.0, 3.0]`
- `parent2.genes = [4.0, 5.0, 6.0]`
- `alpha = 0.3`
- `child1 = 0.3 * [1,2,3] + 0.7 * [4,5,6] = [3.1, 4.1, 5.1]`
- `child2 = 0.7 * [1,2,3] + 0.3 * [4,5,6] = [1.9, 2.9, 3.9]`

**Prečo arithmetický crossover:**
- Funguje dobre pre spojité optimalizačné problémy
- Zachováva hranice (ak rodičia sú v bounds, aj potomkovia budú)

#### `mutation()` (riadky 95-106) - Gaussovská mutácia
```python
def mutation(self, individual: Individual):
    for i in range(len(individual.genes)):
        if random.random() < self.mutation_rate:
            mutation_strength = (bounds[1] - bounds[0]) * 0.1
            individual.genes[i] += np.random.normal(0, mutation_strength)
            individual.genes[i] = np.clip(..., bounds[0], bounds[1])
```

**Ako funguje:**
1. Pre každý gén s pravdepodobnosťou `mutation_rate`:
   - Vypočíta silu mutácie (10% rozsahu bounds)
   - Pridá náhodnú hodnotu z normálneho rozdelenia (stred=0, std=mutation_strength)
   - Orezá hodnotu na hranice

**Príklad:**
- `bounds = (-5.12, 5.12)`, rozsah = 10.24
- `mutation_strength = 10.24 * 0.1 = 1.024`
- Ak `genes[i] = 2.0` a mutácia nastane: `2.0 + N(0, 1.024)` → napr. `2.5`
- Potom `clip(2.5, -5.12, 5.12)` → `2.5` (v bounds)

**Prečo Gaussovská mutácia:**
- Malé zmeny sú pravdepodobnejšie ako veľké
- Vhodné pre jemné doladenie riešenia

#### `evolve()` (riadky 108-142) - Hlavná evolučná metóda
```python
def evolve(self, evaluate_func: Callable):
    # 1. Selekcia
    selected = self.selection()
    
    # 2. Kríženie a mutácia
    new_population = []
    for i in range(0, len(selected), 2):
        child1, child2 = self.crossover(selected[i], selected[i+1])
        self.mutation(child1)
        self.mutation(child2)
        new_population.extend([child1, child2])
    
    # 3. Evaluácia
    for individual in new_population:
        individual.fitness = evaluate_func(individual)
    
    # 4. Nahradenie populácie
    self.population.individuals = new_population
    
    # 5. Elitizmus
    best_old = self.population.get_best()
    worst_new = min(new_population, key=lambda x: x.fitness)
    if best_old.fitness > worst_new.fitness:
        worst_new = best_old.copy()
```

**Kroky evolúcie:**
1. **Selekcia:** Vyberie najlepších jedincov
2. **Kríženie:** Vytvorí nové jedince kombináciou rodičov
3. **Mutácia:** Pridá náhodné zmeny
4. **Evaluácia:** Ohodnotí nové jedince (použije `evaluate_func` z CCEA)
5. **Nahradenie:** Nová populácia nahradí starú
6. **Elitizmus:** Zachová najlepšieho jedinca z predchádzajúcej generácie

**Prečo elitizmus:**
- Zabezpečuje, že najlepšie riešenie sa neztratí
- Zlepšuje konvergenciu

---

### 📦 Trieda: `CooperativeCoevolution` (riadky 145-308)

**Účel:** Hlavná trieda, ktorá koordinuje kooperatívny koevolučný algoritmus.

**Kľúčová myšlienka:**
- Problém s `dimensions` dimenziami sa rozdelí na `num_species` druhov
- Každý druh rieši časť dimenzií
- Jedinci z rôznych druhov spolupracujú pri hodnotení

**Inicializácia (`__init__`, riadky 148-197):**
```python
def __init__(self, fitness_function, dimensions, bounds, 
             num_species=4, population_size=50, generations=100, ...):
    # 1. Uloží parametre
    self.fitness_function = fitness_function
    self.dimensions = dimensions  # Celkový počet dimenzií
    self.num_species = num_species  # Počet druhov
    
    # 2. Rozdelí dimenzie medzi druhy
    self.dimensions_per_species = self._split_dimensions()
    # Príklad: 30 dimenzií, 4 druhy → [8, 8, 7, 7]
    
    # 3. Vytvorí populácie a GA pre každý druh
    for dims in self.dimensions_per_species:
        pop = Population(population_size, dims, bounds)
        ga = GeneticAlgorithm(pop, mutation_rate, crossover_rate)
        self.populations.append(pop)
        self.genetic_algorithms.append(ga)
```

**Príklad rozdelenia:**
- `dimensions = 30`, `num_species = 4`
- `dimensions_per_species = [8, 8, 7, 7]`
- Druh 0 rieši dimenzie 0-7
- Druh 1 rieši dimenzie 8-15
- Druh 2 rieši dimenzie 16-22
- Druh 3 rieši dimenzie 23-29

**Metódy:**

#### `_split_dimensions()` (riadky 199-208)
```python
def _split_dimensions(self) -> List[int]:
    base_dims = self.dimensions // self.num_species
    extra_dims = self.dimensions % self.num_species
    
    dimensions = [base_dims] * self.num_species
    for i in range(extra_dims):
        dimensions[i] += 1
    
    return dimensions
```

**Ako funguje:**
1. Vypočíta základný počet dimenzií na druh
2. Vypočíta zvyšné dimenzie
3. Rozdelí ich rovnomerne (prvé druhy dostanú o 1 viac)

**Príklady:**
- 30 dimenzií, 4 druhy: `[8, 8, 7, 7]`
- 20 dimenzií, 4 druhy: `[5, 5, 5, 5]`
- 31 dimenzií, 4 druhy: `[8, 8, 8, 7]`

#### `_evaluate_individual()` (riadky 210-261) - Kľúčová metóda!
```python
def _evaluate_individual(self, species_index: int, individual: Individual):
    # 1. Vyberie spolupracovníkov z ostatných druhov
    if self.collaboration_size == 1:
        collaborators = [pop.get_best() for pop in other_populations]
    else:
        collaborators = [pop.get_random_individual() for ...]
    
    # 2. Zostaví kompletný vektor riešenia
    solution = np.zeros(self.dimensions)
    
    # Vloží gény aktuálneho jedinca
    start_idx = sum(self.dimensions_per_species[:species_index])
    end_idx = start_idx + self.dimensions_per_species[species_index]
    solution[start_idx:end_idx] = individual.genes
    
    # Vloží gény spolupracovníkov
    for i, pop in enumerate(other_populations):
        solution[their_indices] = collaborator.genes
    
    # 3. Evaluuje kompletný vektor
    return self.fitness_function(solution)
```

**Ako funguje:**
1. **Výber spolupracovníkov:**
   - `collaboration_size = 1`: Použije najlepšieho z každej populácie
   - `collaboration_size > 1`: Náhodne vyberie viacero, potom jeden z nich

2. **Zostavenie riešenia:**
   - Vytvorí vektor dĺžky `dimensions`
   - Vloží gény aktuálneho jedinca na správne pozície
   - Vloží gény spolupracovníkov na ich pozície

3. **Evaluácia:**
   - Zavolá `fitness_function` s kompletným vektorom
   - Vráti fitness hodnotu

**Príklad:**
- Druh 0, jedinec s génmi `[0.5, -1.2, 0.8]`
- Spolupracovníci: Druh 1: `[1.0, 2.0]`, Druh 2: `[3.0]`
- Kompletný vektor: `[0.5, -1.2, 0.8, 1.0, 2.0, 3.0]`
- Tento vektor sa pošle do `fitness_function`

**Prečo je to dôležité:**
- Jedinec nemôže byť ohodnotený sám, potrebuje spolupracovníkov
- Fitness závisí od kvality spolupracovníkov
- To vytvára kooperáciu medzi druhmi

#### `_evaluate_population()` (riadky 263-266)
```python
def _evaluate_population(self, species_index: int):
    for individual in self.populations[species_index].individuals:
        individual.fitness = self._evaluate_individual(species_index, individual)
```

**Účel:** Ohodnotí všetkých jedincov v populácii daného druhu.

#### `_get_best_solution()` (riadky 268-279)
```python
def _get_best_solution(self) -> Tuple[np.ndarray, float]:
    solution = np.zeros(self.dimensions)
    
    for i, pop in enumerate(self.populations):
        best = pop.get_best()
        solution[their_indices] = best.genes
    
    fitness = self.fitness_function(solution)
    return solution, fitness
```

**Účel:** Zostaví najlepšie riešenie kombináciou najlepších jedincov z každej populácie.

**Použitie:**
- Na sledovanie vývoja algoritmu
- Na vrátenie finálneho riešenia

#### `run()` (riadky 281-308) - Hlavný algoritmus
```python
def run(self) -> Tuple[np.ndarray, float]:
    # 1. Počiatočná evaluácia
    for i in range(self.num_species):
        self._evaluate_population(i)
    
    # 2. Hlavný evolučný cyklus
    for generation in range(self.generations):
        # Evolúcia každej populácie
        for i in range(self.num_species):
            def evaluate_func(ind):
                return self._evaluate_individual(i, ind)
            
            self.genetic_algorithms[i].evolve(evaluate_func)
        
        # Zaznamenanie najlepšieho riešenia
        best_solution, best_fitness = self._get_best_solution()
        self.best_fitness_history.append(best_fitness)
    
    return self._get_best_solution()
```

**Kroky algoritmu:**
1. **Inicializácia:** Vytvorí populácie a ohodnotí ich
2. **Pre každú generáciu:**
   - Pre každý druh:
     - Vytvorí evaluačnú funkciu, ktorá používa spolupracovníkov
     - Evoluuje populáciu pomocou GA
   - Zaznamená najlepšie riešenie
3. **Vráti najlepšie riešenie**

**Prečo to funguje:**
- Každý druh sa špecializuje na svoju časť problému
- Spolupracovníci sa postupne zlepšujú
- Najlepší spolupracovníci vedú k lepším hodnoteniam
- Algoritmus konverguje k optimálnemu riešeniu

---

## 2. problems.py

### 🎯 Prehľad
Tento súbor definuje testovacie problémy pre CCEA. Každý problém poskytuje fitness funkciu, ktorá sa používa na hodnotenie riešení.

---

### 📊 PROBLÉM 1: Rastrigin funkcia

#### `rastrigin_function(x: np.ndarray) -> float` (riadky 13-22)
```python
def rastrigin_function(x: np.ndarray) -> float:
    n = len(x)
    A = 10
    return A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x))
```

**Čo robí:**
- Vypočíta hodnotu Rastrigin funkcie pre vektor `x`
- **Vzorec:** `f(x) = 10n + Σ(xᵢ² - 10·cos(2πxᵢ))`

**Vlastnosti:**
- **Globálne optimum:** `x = [0, 0, ..., 0]` s hodnotou `0`
- **Lokálne optimá:** Veľa lokálnych optim (kvôli cos členu)
- **Rozsah:** Typicky testované na `[-5.12, 5.12]`
- **Náročnosť:** Ťažký problém kvôli veľkému počtu lokálnych optim

**Príklad:**
- `x = [0, 0, 0]` → `f(x) = 0` (optimum)
- `x = [1, 1, 1]` → `f(x) = 10*3 + (1+1+1) - 10*(cos(2π)+cos(2π)+cos(2π)) = 30 + 3 - 30 = 3`

**Prečo je to dobrý test:**
- Testuje schopnosť uniknúť z lokálnych optim
- Reprezentatívny problém pre real-world aplikácie

#### `get_rastrigin_problem(dimensions: int = 30)` (riadky 25-37)
```python
def get_rastrigin_problem(dimensions: int = 30):
    def fitness(x):
        return -rastrigin_function(x)  # Negatívna hodnota pre maximalizáciu
    
    bounds = (-5.12, 5.12)
    return fitness, dimensions, bounds
```

**Čo robí:**
- Vytvorí fitness funkciu pre CCEA
- **Dôležité:** Vracia negatívnu hodnotu, pretože:
  - Rastrigin sa minimalizuje (menšie = lepšie)
  - CCEA maximalizuje (väčšie = lepšie)
  - Takže `-rastrigin` sa maximalizuje (menšia Rastrigin = väčšia fitness)

**Výstup:**
- `fitness`: Funkcia, ktorá prijíma numpy array a vracia fitness
- `dimensions`: Počet dimenzií
- `bounds`: Hranice pre hodnoty

**Použitie:**
```python
fitness_func, dims, bounds = get_rastrigin_problem(30)
# fitness_func je funkcia, ktorá sa použije v CCEA
```

---

### 📊 PROBLÉM 2: Optimalizácia parametrov matematického modelu

#### `mathematical_model(x: np.ndarray) -> float` (riadky 44-78)
```python
def mathematical_model(x: np.ndarray) -> float:
    n = len(x) // 4  # Každá skupina 4 parametrov (a, b, c, d)
    
    # Cieľová hodnota
    target_value = 100.0
    
    # Vypočítať hodnotu modelu
    model_value = 0.0
    for i in range(n):
        a = x[i * 4]
        b = x[i * 4 + 1]
        c = x[i * 4 + 2]
        d = x[i * 4 + 3]
        
        input_val = i + 1
        model_value += a * np.sin(b * input_val) + c * np.cos(d * input_val)
    
    # Chyba (RMSE)
    error = (model_value - target_value) ** 2
    return error
```

**Čo robí:**
- Modeluje matematický model pomocou trigonometrických funkcií
- **Model:** `y = Σ(aᵢ·sin(bᵢ·i) + cᵢ·cos(dᵢ·i))`
- **Cieľ:** Nájsť parametre `a, b, c, d` tak, aby `y ≈ 100.0`

**Ako funguje:**
1. Rozdelí vektor `x` na skupiny po 4 parametroch
2. Pre každú skupinu vypočíta `a·sin(b·i) + c·cos(d·i)`
3. Sčíta všetky hodnoty → `model_value`
4. Vypočíta chybu: `(model_value - 100.0)²`

**Príklad:**
- `x = [1, 2, 3, 4, 5, 6, 7, 8]` (8 dimenzií = 2 skupiny)
- Skupina 0: `a=1, b=2, c=3, d=4` → `1·sin(2·1) + 3·cos(4·1)`
- Skupina 1: `a=5, b=6, c=7, d=8` → `5·sin(6·2) + 7·cos(8·2)`
- `model_value = súčet oboch`
- `error = (model_value - 100)²`

**Prečo je to dobrý test:**
- Reprezentuje real-world problém (optimalizácia parametrov modelu)
- Testuje schopnosť nájsť správnu kombináciu parametrov
- Interakcie medzi parametrami (a, b, c, d v rámci skupiny)

#### `get_model_optimization_problem(dimensions: int = 20)` (riadky 81-93)
```python
def get_model_optimization_problem(dimensions: int = 20):
    def fitness(x):
        return -mathematical_model(x)  # Negatívna hodnota pre maximalizáciu
    
    bounds = (-10.0, 10.0)
    return fitness, dimensions, bounds
```

**Čo robí:**
- Podobne ako `get_rastrigin_problem`, vytvorí fitness funkciu
- Vracia negatívnu hodnotu chyby (menšia chyba = väčšia fitness)

**Poznámka:**
- `dimensions` by malo byť násobkom 4 (každá skupina má 4 parametre)
- Ak nie je, funkcia doplní nulami

---

### 🔧 Pomocné funkcie

#### `get_optimal_value_rastrigin(dimensions: int) -> float` (riadky 100-102)
```python
def get_optimal_value_rastrigin(dimensions: int) -> float:
    return 0.0
```

**Účel:** Vráti optimálnu hodnotu Rastrigin funkcie (vždy 0.0).

**Použitie:** Pre porovnanie výsledkov s optimom.

#### `get_optimal_value_model(dimensions: int) -> float` (riadky 105-108)
```python
def get_optimal_value_model(dimensions: int) -> float:
    return 0.0
```

**Účel:** Vráti optimálnu hodnotu pre model (minimálna chyba = 0.0).

**Poznámka:** V skutočnosti môže byť optimálna hodnota iná, ale pre účely testovania sa používa 0.0.

---

## 3. experiments.py

### 🎯 Prehľad
Tento súbor spúšťa experimenty s rôznymi konfiguráciami CCEA a zbiera štatistiky.

---

### 📦 Trieda: `ExperimentRunner` (riadky 18-122)

**Účel:** Spúšťa experimenty a zbiera výsledky.

#### `__init__(num_runs: int = 10)` (riadky 21-23)
```python
def __init__(self, num_runs: int = 10):
    self.num_runs = num_runs  # Počet behov pre každú konfiguráciu
    self.results = []         # Zoznam výsledkov
```

**Prečo `num_runs = 10`:**
- Štatistická významnosť (priemer, štandardná odchýlka)
- Algoritmy sú stochastické, potrebujeme viacero behov

#### `run_experiment(...)` (riadky 25-92) - Hlavná metóda
```python
def run_experiment(self, problem_name, fitness_function, 
                   dimensions, bounds, config):
    all_fitnesses = []
    all_solutions = []
    all_times = []
    convergence_data = []
    
    # Pre každý beh
    for run in range(self.num_runs):
        # Vytvoriť algoritmus
        ccea = CooperativeCoevolution(...)
        
        # Spustiť algoritmus
        best_solution, best_fitness = ccea.run()
        
        # Zaznamenať výsledky
        all_fitnesses.append(best_fitness)
        all_times.append(elapsed_time)
        convergence_data.append(ccea.best_fitness_history)
    
    # Vypočítať štatistiky
    results = {
        'fitness_mean': np.mean(all_fitnesses),
        'fitness_std': np.std(all_fitnesses),
        'fitness_min': np.min(all_fitnesses),
        'fitness_max': np.max(all_fitnesses),
        'time_mean': np.mean(all_times),
        'convergence': self._average_convergence(convergence_data),
        ...
    }
    
    return results
```

**Kroky:**
1. **Pre každý beh (10-krát):**
   - Vytvorí nový CCEA s danou konfiguráciou
   - Spustí algoritmus
   - Zaznamená výsledky (fitness, čas, konvergenciu)

2. **Vypočíta štatistiky:**
   - Priemer, štandardná odchýlka, min, max
   - Priemerná konvergencia cez všetky behy

3. **Vráti výsledky:**
   - Dictionary so všetkými štatistikami

**Prečo viacero behov:**
- Algoritmus je stochastický (náhodná inicializácia, mutácia, selekcia)
- Jeden beh môže byť šťastný/nešťastný
- Priemer cez 10 behov dáva lepší obraz výkonu

#### `_average_convergence(...)` (riadky 94-107)
```python
def _average_convergence(self, convergence_data: List[List[float]]):
    max_gen = max(len(conv) for conv in convergence_data)
    averaged = []
    
    for gen in range(max_gen):
        values = []
        for conv in convergence_data:
            if gen < len(conv):
                values.append(conv[gen])
        if values:
            averaged.append(np.mean(values))
    
    return averaged
```

**Čo robí:**
- Zoberie konvergenčné krivky zo všetkých behov
- Pre každú generáciu vypočíta priemernú fitness
- Vráti priemernú konvergenčnú krivku

**Príklad:**
- Beh 1: `[f1, f2, f3, ...]`
- Beh 2: `[g1, g2, g3, ...]`
- Beh 3: `[h1, h2, h3, ...]`
- Priemer: `[(f1+g1+h1)/3, (f2+g2+h2)/3, ...]`

**Použitie:** Pre vizualizáciu konvergencie (grafy).

#### `print_results(...)` (riadky 109-122)
```python
def print_results(self, results: Dict):
    print(f"Výsledky: {results['problem']}")
    print(f"Konfigurácia: {results['config']}")
    print(f"Priemerná fitness: {results['fitness_mean']:.6f} ± {results['fitness_std']:.6f}")
    print(f"Najlepšia fitness: {results['fitness_max']:.6f}")
    print(f"Najhoršia fitness: {results['fitness_min']:.6f}")
    print(f"Priemerný čas: {results['time_mean']:.2f}s")
```

**Účel:** Vytlačí výsledky experimentu na obrazovku.

---

### 🚀 Funkcia: `main()` (riadky 125-285)

**Účel:** Hlavná funkcia, ktorá spúšťa všetky experimenty.

#### Krok 1: Inicializácia (riadky 128-129)
```python
runner = ExperimentRunner(num_runs=10)
all_results = []
```

#### Krok 2: PROBLÉM 1 - Rastrigin (riadky 131-205)
```python
# Nastavenie problému
dimensions = 30
fitness_func, dims, bounds = get_rastrigin_problem(dimensions)
optimal_value = get_optimal_value_rastrigin(dimensions)

# Konfigurácie pre testovanie
configs = [
    {
        'name': 'Základná konfigurácia',
        'num_species': 4,
        'population_size': 50,
        'generations': 100,
        ...
    },
    {
        'name': 'Viac druhov',
        'num_species': 8,
        ...
    },
    ...
]

# Pre každú konfiguráciu
for config in configs:
    result = runner.run_experiment(
        problem_name=f"Rastrigin - {config['name']}",
        fitness_function=fitness_func,
        dimensions=dimensions,
        bounds=bounds,
        config=config_copy
    )
    all_results.append(result)
    runner.print_results(result)
```

**Čo robí:**
1. Načíta Rastrigin problém
2. Definuje 5 rôznych konfigurácií:
   - Základná (4 druhy, 50 jedincov, 100 generácií)
   - Viac druhov (8 druhov)
   - Väčšia populácia (100 jedincov)
   - Viac generácií (200 generácií)
   - Náhodní spolupracovníci (collaboration_size=3)
3. Pre každú konfiguráciu:
   - Spustí 10 behov
   - Zaznamená výsledky
   - Vytlačí štatistiky

**Prečo rôzne konfigurácie:**
- Testuje vplyv rôznych parametrov na výkon
- Umožňuje porovnanie (ktorá konfigurácia je najlepšia)

#### Krok 3: PROBLÉM 2 - Model (riadky 207-272)
```python
# Podobne ako Rastrigin, ale pre Model problém
dimensions = 20
fitness_func, dims, bounds = get_model_optimization_problem(dimensions)
optimal_value = get_optimal_value_model(dimensions)

configs = [
    {'name': 'Základná konfigurácia', ...},
    {'name': 'Viac druhov', 'num_species': 5, ...},
    ...
]

for config in configs:
    result = runner.run_experiment(...)
    all_results.append(result)
```

**Rozdiel oproti Rastrigin:**
- `dimensions = 20` (nie 30)
- `num_species = 5` pre "Viac druhov" (nie 8)
- Iné konfigurácie (bez "Viac generácií")

#### Krok 4: Uloženie výsledkov (riadky 274-285)
```python
# Uložiť výsledky do JSON súboru
with open('experiment_results.json', 'w') as f:
    json.dump(all_results, f, indent=2)

print("Všetky experimenty dokončené!")
print("Výsledky uložené do 'experiment_results.json'")
```

**Čo sa uloží:**
- Všetky výsledky zo všetkých konfigurácií
- Štatistiky, konvergenčné krivky, časy
- Formát: JSON (ľahko načítateľný pre vizualizáciu)

**Použitie:**
- `visualize_results.py` načíta tento súbor a vytvorí grafy

---

## 4. Ako to všetko spolupracuje

### 🔄 Kompletný workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. experiments.py - main()                                  │
│    └─> Vytvorí ExperimentRunner                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. problems.py - get_rastrigin_problem(30)                  │
│    └─> Vráti: fitness_func, dimensions=30, bounds=(-5.12,5.12)│
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. experiments.py - runner.run_experiment()                 │
│    └─> Pre každý beh (10-krát):                             │
│        │                                                      │
│        ├─> Vytvorí CooperativeCoevolution                   │
│        │   └─> Použije fitness_func z problems.py           │
│        │                                                      │
│        └─> Spustí ccea.run()                                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. cooperative_coevolution.py - CooperativeCoevolution.run() │
│    │                                                          │
│    ├─> Rozdelí 30 dimenzií medzi 4 druhy: [8,8,7,7]         │
│    │                                                          │
│    ├─> Vytvorí 4 populácie (každá s 50 jedincami)          │
│    │                                                          │
│    ├─> Pre každú generáciu (100-krát):                       │
│    │   │                                                      │
│    │   ├─> Pre každý druh:                                   │
│    │   │   ├─> GeneticAlgorithm.evolve()                    │
│    │   │   │   ├─> selection() - turnajová selekcia          │
│    │   │   │   ├─> crossover() - arithmetický crossover      │
│    │   │   │   ├─> mutation() - Gaussovská mutácia           │
│    │   │   │   └─> evaluate_func() - hodnotenie             │
│    │   │   │       └─> _evaluate_individual()                 │
│    │   │   │           ├─> Zostaví kompletný vektor         │
│    │   │   │           └─> fitness_func(completný vektor)    │
│    │   │   │               └─> problems.py - rastrigin_function│
│    │   │   │                                                   │
│    │   │   └─> elitizmus - zachová najlepšieho               │
│    │   │                                                      │
│    │   └─> Zaznamená najlepšie riešenie                       │
│    │                                                          │
│    └─> Vráti najlepšie riešenie                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. experiments.py - Zbiera výsledky                         │
│    ├─> Pre každý beh: fitness, čas, konvergencia            │
│    ├─> Vypočíta štatistiky: priemer, std, min, max          │
│    └─> Uloží do experiment_results.json                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. visualize_results.py (voliteľné)                         │
│    └─> Načíta experiment_results.json                        │
│    └─> Vytvorí grafy konvergencie a porovnania              │
└─────────────────────────────────────────────────────────────┘
```

### 📊 Príklad toku dát

**Scenár:** Rastrigin s 30 dimenziami, 4 druhy, 50 jedincov

1. **Inicializácia:**
   - Druh 0: 50 jedincov, každý s 8 dimenziami
   - Druh 1: 50 jedincov, každý s 8 dimenziami
   - Druh 2: 50 jedincov, každý s 7 dimenziami
   - Druh 3: 50 jedincov, každý s 7 dimenziami

2. **Hodnotenie jedinca:**
   - Druh 0, jedinec A: `genes = [0.5, -1.2, ..., 0.8]` (8 hodnôt)
   - Spolupracovníci:
     - Druh 1, najlepší: `[1.0, 2.0, ..., 0.5]` (8 hodnôt)
     - Druh 2, najlepší: `[3.0, -2.0, ..., 1.1]` (7 hodnôt)
     - Druh 3, najlepší: `[0.1, 0.2, ..., -0.5]` (7 hodnôt)
   - Kompletný vektor: `[0.5, -1.2, ..., 0.8, 1.0, 2.0, ..., 0.5, 3.0, -2.0, ..., 1.1, 0.1, 0.2, ..., -0.5]` (30 hodnôt)
   - Fitness: `fitness_func(completný vektor)` → `-rastrigin_function(completný vektor)`

3. **Evolúcia:**
   - Každý druh sa vyvíja nezávisle
   - Pri hodnotení používa aktuálne najlepšie spolupracovníky
   - Postupne sa zlepšujú všetky druhy

4. **Výsledok:**
   - Najlepšie riešenie = kombinácia najlepších z každej populácie
   - Fitness = hodnota Rastrigin funkcie (čím menšia, tým lepšie)

### 🎯 Kľúčové body

1. **Rozdelenie problému:**
   - Veľký problém (30 dimenzií) → malé problémy (7-8 dimenzií)
   - Každý druh rieši svoju časť

2. **Kooperácia:**
   - Jedinci nemôžu byť ohodnotení sami
   - Potrebujú spolupracovníkov z ostatných druhov
   - To vytvára závislosť medzi druhmi

3. **Evolúcia:**
   - Každý druh sa vyvíja nezávisle pomocou GA
   - Postupne sa zlepšujú všetky druhy
   - Najlepší spolupracovníci vedú k lepším hodnoteniam

4. **Konvergencia:**
   - Algoritmus konverguje k optimálnemu riešeniu
   - História fitness sa zaznamenáva pre analýzu

---

## 📝 Zhrnutie

### cooperative_coevolution.py
- **Individual:** Reprezentuje jedinca
- **Population:** Spravuje populáciu jedincov
- **GeneticAlgorithm:** Evoluuje populáciu (selekcia, crossover, mutácia)
- **CooperativeCoevolution:** Koordinuje kooperatívnu koevolúciu viacerých druhov

### problems.py
- **rastrigin_function:** Vypočíta hodnotu Rastrigin funkcie
- **get_rastrigin_problem:** Vytvorí fitness funkciu pre CCEA
- **mathematical_model:** Vypočíta chybu matematického modelu
- **get_model_optimization_problem:** Vytvorí fitness funkciu pre CCEA

### experiments.py
- **ExperimentRunner:** Spúšťa experimenty a zbiera štatistiky
- **main:** Spúšťa všetky experimenty s rôznymi konfiguráciami
- Ukladá výsledky do JSON súboru

### Spolupráca
1. `experiments.py` načíta problém z `problems.py`
2. Vytvorí `CooperativeCoevolution` z `cooperative_coevolution.py`
3. Algoritmus používa fitness funkciu z `problems.py`
4. Výsledky sa zbierajú a ukladajú v `experiments.py`

---

**Tento dokument poskytuje kompletný prehľad všetkých troch súborov a ich vzájomnej spolupráce.**

