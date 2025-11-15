# Detailné Vysvetlenie Workflowu - Kompletný Průvodce

Tento dokument poskytuje **ultra-podrobné** vysvetlenie každého kroku, každej funkcie a každého parametra v aplikácii. Je navrhnutý tak, aby niekto, kto ešte nikdy nevidel tento kód, mohol úplne pochopiť, ako všetko funguje.

---

## 📚 Obsah

1. [Úvod a Prehľad Systému](#úvod-a-prehľad-systému)
2. [Problémy (problems.py) - Detailné Vysvetlenie](#problémy-problemspy---detailné-vysvetlenie)
3. [Kooperatívny Koevolučný Algoritmus (cooperative_coevolution.py) - Detailné Vysvetlenie](#kooperatívny-koevolučný-algoritmus-cooperative_coevolutionpy---detailné-vysvetlenie)
4. [Experimenty (experiments.py) - Detailné Vysvetlenie](#experimenty-experimentspy---detailné-vysvetlenie)
5. [Kompletný Príklad Workflowu](#kompletný-príklad-workflowu)

---

## Úvod a Prehľad Systému

### Čo je Kooperatívny Koevolučný Algoritmus (CCEA)?

**Kooperatívny koevolučný algoritmus** je metóda riešenia komplexných optimalizačných problémov. Hlavná myšlienka je:

1. **Rozdelenie problému:** Veľký problém (napr. 30 dimenzií) sa rozdelí na menšie časti (napr. 4 časti po 7-8 dimenziách)
2. **Nezávislá evolúcia:** Každá časť sa rieši samostatne pomocou genetického algoritmu
3. **Kooperácia:** Jedinci z rôznych častí musia spolupracovať, aby boli ohodnotení
4. **Spoločné zlepšovanie:** Postupne sa zlepšujú všetky časti, čo vedie k lepšiemu celkovému riešeniu

### Prečo sa to používa?

- **Škálovateľnosť:** Veľké problémy (100+ dimenzií) sú ťažko riešiteľné klasickými metódami
- **Paralelizácia:** Rôzne časti sa môžu riešiť paralelne
- **Efektívnosť:** Menšie problémy sa riešia rýchlejšie

### Štruktúra Aplikácie

```
experiments.py
    ↓ (volá)
problems.py → vráti fitness funkciu
    ↓ (použije)
cooperative_coevolution.py → vyrieši problém
    ↓ (vráti výsledky)
experiments.py → uloží a analyzuje
```

---

## Problémy (problems.py) - Detailné Vysvetlenie

### 1. Rastrigin Funkcia

#### `rastrigin_function(x: np.ndarray) -> float`

**Účel:** Vypočíta hodnotu Rastrigin funkcie pre daný vektor `x`.

**Parametre:**
- `x`: `np.ndarray` - vektor čísel (napr. `[1.5, -2.3, 0.8, ...]`)
  - **Odkiaľ pochádza:** Zavolá sa z fitness funkcie v `get_rastrigin_problem()`
  - **Čo obsahuje:** Hodnoty pre každú dimenziu problému

**Čo robí krok za krokom:**

```python
def rastrigin_function(x):
    n = len(x)  # Počet dimenzií (napr. 30)
    A = 10      # Konštanta (štandardná hodnota pre Rastrigin)
    
    # Vypočítame hodnotu funkcie
    result = A * n  # Začíname s 10 * n (napr. 10 * 30 = 300)
    
    # Pre každú dimenziu pridáme príspevok
    for i in range(n):
        result += x[i]**2 - A * np.cos(2 * np.pi * x[i])
    
    return result
```

**Vzorec:**
```
f(x) = 10n + Σ(x_i² - 10·cos(2πx_i))
```

**Príklad výpočtu:**
- `x = [0, 0, 0]` (3 dimenzie, optimálne riešenie)
- `n = 3`, `A = 10`
- `result = 10*3 = 30`
- Pre `i=0`: `0² - 10*cos(0) = 0 - 10*1 = -10`
- Pre `i=1`: `0² - 10*cos(0) = 0 - 10*1 = -10`
- Pre `i=2`: `0² - 10*cos(0) = 0 - 10*1 = -10`
- `result = 30 + (-10) + (-10) + (-10) = 0` ✅ (optimum!)

**Vlastnosti:**
- **Globálne optimum:** `x = [0, 0, ..., 0]` s hodnotou `0`
- **Lokálne optimá:** Veľa lokálnych optim (kvôli `cos` členu)
- **Náročnosť:** Ťažký problém kvôli veľkému počtu lokálnych optim

**Prečo je to dobrý test:**
- Testuje schopnosť uniknúť z lokálnych optim
- Reprezentatívny pre real-world problémy

---

#### `get_rastrigin_problem(dimensions: int = 30)`

**Účel:** Vytvorí fitness funkciu pre CCEA algoritmus.

**Parametre:**
- `dimensions`: `int` - počet dimenzií problému (default: 30)
  - **Odkiaľ pochádza:** Zavolá sa z `experiments.py` v `main()` funkcii
  - **Príklad:** `dimensions = 30` pre 30-rozmerný problém

**Čo robí krok za krokom:**

```python
def get_rastrigin_problem(dimensions=30):
    # Vytvoríme vnútornú funkciu, ktorá bude použitá ako fitness
    def fitness(x):
        # Vypočítame hodnotu Rastrigin funkcie
        value = rastrigin_function(x)
        
        # DÔLEŽITÉ: Vrátime negatívnu hodnotu!
        # Prečo? Algoritmus MAXIMALIZUJE fitness (väčšie = lepšie)
        # Ale Rastrigin sa MINIMALIZUJE (menšie = lepšie)
        # Takže -rastrigin sa maximalizuje (menšia Rastrigin = väčšia fitness)
        return -value
    
    # Hranice pre hodnoty (štandardné pre Rastrigin)
    bounds = (-5.12, 5.12)
    
    # Vrátime tri veci:
    return fitness, dimensions, bounds
    # fitness: funkcia, ktorá prijme vektor a vráti fitness
    # dimensions: počet dimenzií
    # bounds: hranice pre hodnoty
```

**Výstup:**
- `fitness`: Funkcia, ktorá prijíma `np.ndarray` a vracia `float`
  - **Kde sa použije:** V `CooperativeCoevolution.__init__()` ako `fitness_function`
- `dimensions`: Počet dimenzií
  - **Kde sa použije:** V `CooperativeCoevolution.__init__()` ako `dimensions`
- `bounds`: Tuple `(min, max)` pre hodnoty
  - **Kde sa použije:** V `CooperativeCoevolution.__init__()` a `Population.__init__()`

**Príklad použitia:**
```python
# V experiments.py:
fitness_func, dims, bounds = get_rastrigin_problem(30)
# fitness_func je teraz funkcia, ktorá:
#   - prijme vektor 30 čísel
#   - vypočíta Rastrigin hodnotu
#   - vráti negatívnu hodnotu (pre maximalizáciu)
```

---

### 2. Optimalizácia Parametrov Modelu

#### `mathematical_model(x: np.ndarray) -> float`

**Účel:** Vypočíta chybu matematického modelu pre dané parametre.

**Parametre:**
- `x`: `np.ndarray` - vektor parametrov (napr. `[1.5, -2.3, 0.8, 4.1, ...]`)
  - **Odkiaľ pochádza:** Zavolá sa z fitness funkcie v `get_model_optimization_problem()`
  - **Čo obsahuje:** Parametre modelu zoskupené po 4: `(a, b, c, d)` pre každú skupinu

**Čo robí krok za krokom:**

```python
def mathematical_model(x):
    # Každá skupina má 4 parametre (a, b, c, d)
    n = len(x) // 4  # Počet skupín
    
    # Ak sa nedelí rovnomerne, doplníme nulami
    if len(x) % 4 != 0:
        x = np.pad(x, (0, 4 - (len(x) % 4)), mode='constant')
        n = len(x) // 4
    
    # Cieľová hodnota, ktorú chceme dosiahnuť
    target_value = 100.0
    
    # Vypočítame hodnotu modelu
    model_value = 0.0
    for i in range(n):
        # Zoberieme 4 parametre pre túto skupinu
        a = x[i * 4]      # parameter a (koeficient pre sin)
        b = x[i * 4 + 1]  # parameter b (frekvencia pre sin)
        c = x[i * 4 + 2]  # parameter c (koeficient pre cos)
        d = x[i * 4 + 3]  # parameter d (frekvencia pre cos)
        
        # Použijeme pevné vstupné hodnoty pre model
        input_val = i + 1  # Pre skupinu 0: 1, pre skupinu 1: 2, atď.
        
        # Vypočítame príspevok tejto skupiny
        contribution = a * np.sin(b * input_val) + c * np.cos(d * input_val)
        model_value += contribution
    
    # Vypočítame chybu (RMSE - Root Mean Square Error)
    error = (model_value - target_value) ** 2
    
    return error
```

**Vzorec modelu:**
```
y = Σ(a_i·sin(b_i·i) + c_i·cos(d_i·i))
```

**Cieľ:** Nájsť parametre tak, aby `y ≈ 100.0`

**Príklad výpočtu:**
- `x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]` (8 dimenzií = 2 skupiny)
- Skupina 0: `a=1.0, b=2.0, c=3.0, d=4.0`, `input_val=1`
  - `contribution = 1.0*sin(2.0*1) + 3.0*cos(4.0*1) = 0.91 + (-2.16) = -1.25`
- Skupina 1: `a=5.0, b=6.0, c=7.0, d=8.0`, `input_val=2`
  - `contribution = 5.0*sin(6.0*2) + 7.0*cos(8.0*2) = -2.27 + 5.21 = 2.94`
- `model_value = -1.25 + 2.94 = 1.69`
- `error = (1.69 - 100.0)² = 9658.56`

**Prečo je to dobrý test:**
- Reprezentuje real-world problém (optimalizácia parametrov modelu)
- Testuje schopnosť nájsť správnu kombináciu parametrov
- Interakcie medzi parametrami (a, b, c, d v rámci skupiny)

---

#### `get_model_optimization_problem(dimensions: int = 20)`

**Účel:** Vytvorí fitness funkciu pre CCEA algoritmus.

**Parametre:**
- `dimensions`: `int` - počet dimenzií problému (default: 20)
  - **Odkiaľ pochádza:** Zavolá sa z `experiments.py` v `main()` funkcii
  - **Poznámka:** Malo by byť násobkom 4 (každá skupina má 4 parametre)

**Čo robí krok za krokom:**

```python
def get_model_optimization_problem(dimensions=20):
    # Vytvoríme vnútornú funkciu, ktorá bude použitá ako fitness
    def fitness(x):
        # Vypočítame chybu modelu
        error = mathematical_model(x)
        
        # DÔLEŽITÉ: Vrátime negatívnu hodnotu!
        # Prečo? Algoritmus MAXIMALIZUJE fitness (väčšie = lepšie)
        # Ale chyba sa MINIMALIZUJE (menšia = lepšie)
        # Takže -error sa maximalizuje (menšia chyba = väčšia fitness)
        return -error
    
    # Hranice pre hodnoty parametrov
    bounds = (-10.0, 10.0)
    
    # Vrátime tri veci:
    return fitness, dimensions, bounds
```

**Výstup:** Rovnako ako `get_rastrigin_problem()`

---

## Kooperatívny Koevolučný Algoritmus (cooperative_coevolution.py) - Detailné Vysvetlenie

### Trieda: `Individual`

#### `__init__(self, genes, fitness=-999999)`

**Účel:** Vytvorí jedinca s génmi a fitness hodnotou.

**Parametre:**
- `genes`: `np.ndarray` - hodnoty riešenia (napr. `[1.5, -2.3, 0.8, ...]`)
  - **Odkiaľ pochádza:** 
    - Pri vytváraní: Z `Population._create_initial_population()` - náhodné hodnoty
    - Pri krížení: Z `GeneticAlgorithm.crossover()` - kombinácia rodičov
    - Pri mutácii: Z `GeneticAlgorithm.mutation()` - zmenené hodnoty
  - **Čo obsahuje:** Hodnoty pre dimenzie, ktoré tento jedinec rieši
- `fitness`: `float` - hodnota fitness (default: `-999999` = veľmi zlá)
  - **Odkiaľ pochádza:** 
    - Počiatočne: `-999999` (ešte nebol ohodnotený)
    - Po evaluácii: Z `CooperativeCoevolution._evaluate_individual()`

**Čo robí:**
```python
def __init__(self, genes, fitness=-999999):
    self.genes = genes      # Uloží gény
    self.fitness = fitness  # Uloží fitness
```

**Príklad:**
```python
# Vytvorenie jedinca s 8 dimenziami
genes = np.array([2.3, -1.5, 0.8, 4.1, -2.9, 1.2, 0.5, -3.7])
individual = Individual(genes)
# individual.genes = [2.3, -1.5, 0.8, 4.1, -2.9, 1.2, 0.5, -3.7]
# individual.fitness = -999999 (ešte nebol ohodnotený)
```

---

#### `copy(self)`

**Účel:** Vytvorí kópiu jedinca.

**Parametre:** Žiadne (používa `self`)

**Prečo je to potrebné:**
- Pri selekcii: Potrebujeme kópie, aby sme nezmenili originál
- Pri krížení: Potrebujeme kópie rodičov
- Pri elitizme: Potrebujeme kópiu najlepšieho jedinca

**Čo robí:**
```python
def copy(self):
    return Individual(self.genes.copy(), self.fitness)
    # .copy() vytvorí nový numpy array (nie referenciu!)
```

**Príklad:**
```python
original = Individual(np.array([1.0, 2.0, 3.0]), fitness=10.0)
copy = original.copy()
copy.genes[0] = 999.0  # Zmeníme kópiu
# original.genes[0] je stále 1.0 (nezmenené!)
```

---

### Trieda: `Population`

#### `__init__(self, size, dimension, bounds)`

**Účel:** Vytvorí populáciu jedincov.

**Parametre:**
- `size`: `int` - počet jedincov v populácii (napr. 50)
  - **Odkiaľ pochádza:** Z `CooperativeCoevolution.__init__()` ako `population_size`
- `dimension`: `int` - počet dimenzií každého jedinca (napr. 8)
  - **Odkiaľ pochádza:** Z `CooperativeCoevolution._split_dimensions()` - počet dimenzií pre tento druh
- `bounds`: `Tuple[float, float]` - hranice pre hodnoty (napr. `(-5.12, 5.12)`)
  - **Odkiaľ pochádza:** Z `CooperativeCoevolution.__init__()` ako `bounds`

**Čo robí krok za krokom:**

```python
def __init__(self, size, dimension, bounds):
    # Uložíme parametre
    self.size = size           # 50
    self.dimension = dimension # 8
    self.bounds = bounds       # (-5.12, 5.12)
    self.individuals = []     # Zatiaľ prázdny zoznam
    
    # Vytvoríme počiatočnú populáciu
    self._create_initial_population()
```

**Príklad:**
```python
# Vytvorenie populácie pre Druh 0 (8 dimenzií)
pop = Population(size=50, dimension=8, bounds=(-5.12, 5.12))
# Vytvorí sa 50 jedincov, každý s 8 náhodnými hodnotami medzi -5.12 a 5.12
```

---

#### `_create_initial_population(self)`

**Účel:** Vytvorí počiatočnú populáciu náhodnými jedincami.

**Parametre:** Žiadne (používa `self.size`, `self.dimension`, `self.bounds`)

**Čo robí krok za krokom:**

```python
def _create_initial_population(self):
    self.individuals = []  # Vyčistíme zoznam
    
    # Pre každého jedinca v populácii
    for i in range(self.size):  # 50-krát
        # Vytvoríme náhodné gény v rámci hraníc
        genes = np.random.uniform(
            self.bounds[0],  # minimálna hodnota (-5.12)
            self.bounds[1],  # maximálna hodnota (5.12)
            self.dimension   # koľko čísel (8)
        )
        # Príklad: genes = [2.3, -1.5, 0.8, 4.1, -2.9, 1.2, 0.5, -3.7]
        
        # Vytvoríme nového jedinca
        individual = Individual(genes)
        # individual.fitness = -999999 (ešte nebol ohodnotený)
        
        # Pridáme do populácie
        self.individuals.append(individual)
```

**Výsledok:**
- `self.individuals` obsahuje 50 jedincov
- Každý jedinec má 8 náhodných hodnôt medzi -5.12 a 5.12
- Žiadny jedinec ešte nemá ohodnotenú fitness

---

#### `get_best(self)`

**Účel:** Vráti najlepšieho jedinca (s najväčšou fitness hodnotou).

**Parametre:** Žiadne (používa `self.individuals`)

**Čo robí krok za krokom:**

```python
def get_best(self):
    # Začneme s prvým jedincom
    best = self.individuals[0]
    
    # Prejdeme cez všetkých jedincov
    for ind in self.individuals:
        # Ak má tento jedinec lepšiu fitness, stane sa najlepším
        if ind.fitness > best.fitness:
            best = ind
    
    return best
```

**Kde sa používa:**
- V `CooperativeCoevolution._evaluate_individual()` - výber najlepšieho spolupracovníka
- V `CooperativeCoevolution._get_best_solution()` - zostavenie najlepšieho riešenia
- V `GeneticAlgorithm.evolve()` - elitizmus

**Príklad:**
```python
# Populácia s 3 jedincami
individual1.fitness = -100.0
individual2.fitness = -50.0
individual3.fitness = -200.0

best = pop.get_best()
# best = individual2 (má najväčšiu fitness: -50.0)
```

---

#### `get_random_individual(self)`

**Účel:** Vráti náhodného jedinca z populácie.

**Parametre:** Žiadne (používa `self.individuals`)

**Kde sa používa:**
- V `CooperativeCoevolution._evaluate_individual()` - výber náhodného spolupracovníka (ak `collaboration_size > 1`)

**Príklad:**
```python
random_ind = pop.get_random_individual()
# Môže byť ktorýkoľvek z 50 jedincov
```

---

### Trieda: `GeneticAlgorithm`

#### `__init__(self, population, mutation_rate=0.1, crossover_rate=0.8)`

**Účel:** Vytvorí genetický algoritmus pre evolúciu populácie.

**Parametre:**
- `population`: `Population` - populácia, ktorá sa má vyvíjať
  - **Odkiaľ pochádza:** Z `CooperativeCoevolution.__init__()` - jedna z populácií druhov
- `mutation_rate`: `float` - pravdepodobnosť mutácie (default: 0.1 = 10%)
  - **Odkiaľ pochádza:** Z `CooperativeCoevolution.__init__()` ako `mutation_rate`
  - **Čo znamená:** 10% šanca, že sa každý gén zmení
- `crossover_rate`: `float` - pravdepodobnosť kríženia (default: 0.8 = 80%)
  - **Odkiaľ pochádza:** Z `CooperativeCoevolution.__init__()` ako `crossover_rate`
  - **Čo znamená:** 80% šanca, že sa dvaja rodičia skrížia

**Čo robí:**
```python
def __init__(self, population, mutation_rate=0.1, crossover_rate=0.8):
    self.population = population
    self.mutation_rate = mutation_rate
    self.crossover_rate = crossover_rate
```

---

#### `selection(self)`

**Účel:** Turnajová selekcia - vyberie najlepších jedincov.

**Parametre:** Žiadne (používa `self.population`)

**Čo robí krok za krokom:**

```python
def selection(self):
    # Veľkosť turnaja = 10% populácie, minimálne 2
    tournament_size = max(2, int(self.population.size * 0.1))
    # Pre populáciu 50: tournament_size = max(2, 5) = 5
    
    selected = []  # Zoznam vybraných jedincov
    
    # Pre každého jedinca v novej populácii (50-krát)
    for i in range(self.population.size):
        # Vyberieme náhodných jedincov do turnaja
        tournament = random.sample(
            self.population.individuals,  # Zoznam všetkých jedincov
            tournament_size                # Koľko ich vybrať (5)
        )
        # Príklad: tournament = [ind3, ind15, ind42, ind7, ind28]
        
        # Vyberieme víťaza turnaja (najlepšieho)
        winner = tournament[0]  # Začneme s prvým
        for ind in tournament:
            if ind.fitness > winner.fitness:
                winner = ind  # Tento je lepší
        
        # Pridáme víťaza do vybraných (ako kópiu!)
        selected.append(winner.copy())
    
    return selected  # 50 vybraných jedincov
```

**Prečo turnajová selekcia:**
- Jednoduchá implementácia
- Umožňuje kontrolovať tlak selekcie (veľkosť turnaja)
- Lepší jedinci majú vyššiu šancu, ale aj horší môžu byť vybraní (diverzita)

**Príklad:**
```python
# Populácia s 50 jedincami
# Turnaj 1: [ind3(fitness=-50), ind15(fitness=-100), ind42(fitness=-30), ...]
# Víťaz: ind42 (najlepšia fitness: -30)
# Turnaj 2: [ind7(fitness=-200), ind21(fitness=-80), ind33(fitness=-150), ...]
# Víťaz: ind21 (najlepšia fitness: -80)
# ...
# Výsledok: 50 vybraných jedincov (najlepší majú vyššiu šancu)
```

---

#### `crossover(self, parent1, parent2)`

**Účel:** Arithmetický crossover - vytvorí dvoch potomkov z dvoch rodičov.

**Parametre:**
- `parent1`: `Individual` - prvý rodič
  - **Odkiaľ pochádza:** Z `selection()` - vybraný jedinec
- `parent2`: `Individual` - druhý rodič
  - **Odkiaľ pochádza:** Z `selection()` - ďalší vybraný jedinec

**Čo robí krok za krokom:**

```python
def crossover(self, parent1, parent2):
    # S určitou pravdepodobnosťou sa nekrížime
    if random.random() > self.crossover_rate:  # 20% šanca
        return parent1.copy(), parent2.copy()  # Vrátime rodičov bez zmeny
    
    # Vytvoríme náhodné číslo medzi 0 a 1
    alpha = random.random()  # Napr. alpha = 0.3
    
    # Prvý potomok: kombinácia génov rodičov
    genes1 = alpha * parent1.genes + (1 - alpha) * parent2.genes
    # = 0.3 * parent1.genes + 0.7 * parent2.genes
    
    # Druhý potomok: opačná kombinácia
    genes2 = (1 - alpha) * parent1.genes + alpha * parent2.genes
    # = 0.7 * parent1.genes + 0.3 * parent2.genes
    
    return Individual(genes1), Individual(genes2)
```

**Príklad:**
```python
parent1.genes = [2.0, -1.0, 0.5]
parent2.genes = [1.0, 2.0, -0.5]
alpha = 0.3

child1.genes = 0.3 * [2.0, -1.0, 0.5] + 0.7 * [1.0, 2.0, -0.5]
            = [0.6, -0.3, 0.15] + [0.7, 1.4, -0.35]
            = [1.3, 1.1, -0.2]

child2.genes = 0.7 * [2.0, -1.0, 0.5] + 0.3 * [1.0, 2.0, -0.5]
            = [1.4, -0.7, 0.35] + [0.3, 0.6, -0.15]
            = [1.7, -0.1, 0.2]
```

**Prečo arithmetický crossover:**
- Funguje dobre pre spojité optimalizačné problémy
- Zachováva hranice (ak rodičia sú v bounds, aj potomkovia budú)
- Vytvára nové kombinácie hodnôt

---

#### `mutation(self, individual)`

**Účel:** Gaussovská mutácia - náhodne zmení niektoré gény.

**Parametre:**
- `individual`: `Individual` - jedinec, ktorého gény sa majú zmeniť
  - **Odkiaľ pochádza:** Z `crossover()` - nový potomok

**Čo robí krok za krokom:**

```python
def mutation(self, individual):
    # Pre každý gén v génoch jedinca
    for i in range(len(individual.genes)):
        # S určitou pravdepodobnosťou zmeníme gén
        if random.random() < self.mutation_rate:  # 10% šanca
            # O koľko zmeníme (10% z rozsahu hraníc)
            mutation_strength = (self.population.bounds[1] - self.population.bounds[0]) * 0.1
            # Pre bounds (-5.12, 5.12): mutation_strength = 10.24 * 0.1 = 1.024
            
            # Pridáme náhodnú zmenu (normálne rozdelenie)
            individual.genes[i] += np.random.normal(0, mutation_strength)
            # N(0, 1.024) - stred=0, štandardná odchýlka=1.024
            
            # Uistíme sa, že hodnota je stále v hraniciach
            if individual.genes[i] < self.population.bounds[0]:
                individual.genes[i] = self.population.bounds[0]
            if individual.genes[i] > self.population.bounds[1]:
                individual.genes[i] = self.population.bounds[1]
```

**Príklad:**
```python
# Jedinec pred mutáciou
individual.genes = [1.3, 1.1, -0.2]
bounds = (-5.12, 5.12)
mutation_strength = 1.024

# Gén 0: random() = 0.05 < 0.1 → MUTÁCIA
#   np.random.normal(0, 1.024) = 0.5
#   individual.genes[0] = 1.3 + 0.5 = 1.8

# Gén 1: random() = 0.15 > 0.1 → ŽIADNA MUTÁCIA
#   individual.genes[1] = 1.1 (nezmenené)

# Gén 2: random() = 0.08 < 0.1 → MUTÁCIA
#   np.random.normal(0, 1.024) = -0.3
#   individual.genes[2] = -0.2 + (-0.3) = -0.5

# Výsledok: [1.8, 1.1, -0.5]
```

**Prečo Gaussovská mutácia:**
- Malé zmeny sú pravdepodobnejšie ako veľké
- Vhodné pre jemné doladenie riešenia
- Normálne rozdelenie je prirodzené pre spojité hodnoty

---

#### `evolve(self, evaluate_func)`

**Účel:** Vykoná jednu generáciu evolúcie.

**Parametre:**
- `evaluate_func`: `Callable` - funkcia na hodnotenie jedinca
  - **Odkiaľ pochádza:** Z `CooperativeCoevolution.run()` - vytvorí sa ako:
    ```python
    def evaluate_func(ind):
        return self._evaluate_individual(i, ind)
    ```
  - **Čo robí:** Prijme jedinca a vráti jeho fitness hodnotu

**Čo robí krok za krokom:**

```python
def evolve(self, evaluate_func):
    # 1. Selekcia - vyberieme najlepších
    selected = self.selection()
    # Výsledok: 50 vybraných jedincov
    
    # 2. Kríženie a mutácia - vytvoríme novú generáciu
    new_population = []
    for i in range(0, len(selected), 2):  # Po dvojiciach
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
        new_population.extend([child1, child2])
    
    # Zmenšiť na pôvodnú veľkosť (ak sme vytvorili viac)
    new_population = new_population[:self.population.size]
    
    # 3. Evaluácia - ohodnotíme každého jedinca
    for individual in new_population:
        individual.fitness = evaluate_func(individual)
        # evaluate_func zavolá _evaluate_individual()
        # ktorá zostaví kompletný vektor a vypočíta fitness
    
    # 4. Nahradenie populácie
    self.population.individuals = new_population
    
    # 5. Elitizmus - zachováme najlepšieho z predchádzajúcej generácie
    best_old = self.population.get_best()  # Najlepší z novej populácie
    # (Poznámka: V kóde sa to robí trochu inak, ale myšlienka je rovnaká)
    worst_new = new_population[0]
    for ind in new_population:
        if ind.fitness < worst_new.fitness:
            worst_new = ind
    
    # Ak bol najlepší z predchádzajúcej generácie lepší, zachováme ho
    if best_old.fitness > worst_new.fitness:
        worst_new.genes = best_old.genes.copy()
        worst_new.fitness = best_old.fitness
```

**Prečo elitizmus:**
- Zabezpečuje, že najlepšie riešenie sa neztratí
- Zlepšuje konvergenciu (algoritmus sa nezhoršuje)

---

### Trieda: `CooperativeCoevolution`

#### `__init__(self, fitness_function, dimensions, bounds, num_species=4, population_size=50, generations=100, mutation_rate=0.1, crossover_rate=0.8, collaboration_size=1)`

**Účel:** Vytvorí kooperatívny koevolučný algoritmus.

**Parametre:**
- `fitness_function`: `Callable` - funkcia na hodnotenie riešenia
  - **Odkiaľ pochádza:** Z `problems.py` - `get_rastrigin_problem()` alebo `get_model_optimization_problem()`
  - **Čo robí:** Prijme kompletný vektor riešenia a vráti fitness hodnotu
- `dimensions`: `int` - celkový počet dimenzií problému (napr. 30)
  - **Odkiaľ pochádza:** Z `experiments.py` - `dimensions = 30`
- `bounds`: `Tuple[float, float]` - hranice pre hodnoty (napr. `(-5.12, 5.12)`)
  - **Odkiaľ pochádza:** Z `problems.py` - vráti sa spolu s fitness funkciou
- `num_species`: `int` - počet druhov/populácií (default: 4)
  - **Odkiaľ pochádza:** Z `experiments.py` - konfigurácia experimentu
  - **Čo znamená:** Na koľko častí sa rozdelí problém
- `population_size`: `int` - veľkosť každej populácie (default: 50)
  - **Odkiaľ pochádza:** Z `experiments.py` - konfigurácia experimentu
- `generations`: `int` - počet generácií (default: 100)
  - **Odkiaľ pochádza:** Z `experiments.py` - konfigurácia experimentu
- `mutation_rate`: `float` - pravdepodobnosť mutácie (default: 0.1)
  - **Odkiaľ pochádza:** Z `experiments.py` - konfigurácia experimentu
- `crossover_rate`: `float` - pravdepodobnosť kríženia (default: 0.8)
  - **Odkiaľ pochádza:** Z `experiments.py` - konfigurácia experimentu
- `collaboration_size`: `int` - počet partnerov pri hodnotení (default: 1)
  - **Odkiaľ pochádza:** Z `experiments.py` - konfigurácia experimentu
  - **Čo znamená:** 
    - `1` = použije najlepšieho z každej populácie
    - `>1` = náhodne vyberie viacero, potom jeden z nich

**Čo robí krok za krokom:**

```python
def __init__(self, fitness_function, dimensions, bounds, ...):
    # 1. Uložíme parametre
    self.fitness_function = fitness_function
    self.dimensions = dimensions  # 30
    self.bounds = bounds          # (-5.12, 5.12)
    self.num_species = num_species  # 4
    self.population_size = population_size  # 50
    self.generations = generations  # 100
    self.mutation_rate = mutation_rate  # 0.1
    self.crossover_rate = crossover_rate  # 0.8
    self.collaboration_size = collaboration_size  # 1
    
    # 2. Rozdelíme dimenzie medzi druhy
    self.dimensions_per_species = self._split_dimensions()
    # Výsledok: [8, 8, 7, 7] pre 30 dimenzií a 4 druhy
    
    # 3. Vytvoríme populácie a genetické algoritmy
    self.populations = []
    self.genetic_algorithms = []
    
    for dims in self.dimensions_per_species:
        # Vytvoríme populáciu pre tento druh
        pop = Population(population_size, dims, bounds)
        # pop.size = 50, pop.dimension = 8 (alebo 7), pop.bounds = (-5.12, 5.12)
        
        # Vytvoríme genetický algoritmus pre túto populáciu
        ga = GeneticAlgorithm(pop, mutation_rate, crossover_rate)
        
        self.populations.append(pop)
        self.genetic_algorithms.append(ga)
    
    # 4. História pre sledovanie vývoja
    self.best_fitness_history = []
    self.best_solution_history = []
```

**Výsledok:**
- 4 populácie, každá s 50 jedincami
- 4 genetické algoritmy, jeden pre každú populáciu
- Prázdne histórie (budú sa naplniť počas evolúcie)

---

#### `_split_dimensions(self)`

**Účel:** Rozdelí dimenzie medzi druhy.

**Parametre:** Žiadne (používa `self.dimensions`, `self.num_species`)

**Čo robí krok za krokom:**

```python
def _split_dimensions(self):
    # Základný počet dimenzií na druh
    base_dims = self.dimensions // self.num_species
    # Pre 30 dimenzií a 4 druhy: base_dims = 30 // 4 = 7
    
    # Zvyšné dimenzie (ak sa nedelí rovnomerne)
    extra_dims = self.dimensions % self.num_species
    # extra_dims = 30 % 4 = 2
    
    # Vytvoríme zoznam počtu dimenzií pre každý druh
    dimensions = [base_dims] * self.num_species
    # dimensions = [7, 7, 7, 7]
    
    # Rozdelíme zvyšné dimenzie medzi prvé druhy
    for i in range(extra_dims):  # 2-krát
        dimensions[i] += 1
    # dimensions[0] = 7 + 1 = 8
    # dimensions[1] = 7 + 1 = 8
    # dimensions = [8, 8, 7, 7]
    
    return dimensions
```

**Príklady:**
- 30 dimenzií, 4 druhy: `[8, 8, 7, 7]`
- 20 dimenzií, 4 druhy: `[5, 5, 5, 5]`
- 31 dimenzií, 4 druhy: `[8, 8, 8, 7]`

---

#### `_evaluate_individual(self, species_index, individual, collaborators=None)`

**Účel:** Ohodnotí jedinca - musí spolupracovať s jedincami z iných druhov.

**Parametre:**
- `species_index`: `int` - ktorý druh hodnotíme (0, 1, 2, 3)
  - **Odkiaľ pochádza:** Z `_evaluate_population()` alebo `run()` - index aktuálneho druhu
- `individual`: `Individual` - jedinec, ktorého hodnotíme
  - **Odkiaľ pochádza:** Z `_evaluate_population()` - jeden z jedincov populácie
- `collaborators`: `List[List[Individual]]` - spolupracovníci (default: None)
  - **Odkiaľ pochádza:** Voliteľný parameter (ak None, vyberú sa automaticky)

**Čo robí krok za krokom:**

```python
def _evaluate_individual(self, species_index, individual, collaborators=None):
    # 1. Ak nemáme spolupracovníkov, vyberieme ich
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
    
    # 2. Zostavíme kompletný vektor riešenia (všetky dimenzie)
    solution = np.zeros(self.dimensions)  # Vektor dĺžky 30, všetky nuly
    
    # 3. Vložíme gény aktuálneho jedinca na správne miesto
    start_idx = 0
    for i in range(species_index):
        start_idx += self.dimensions_per_species[i]
    # Pre species_index=0: start_idx = 0
    # Pre species_index=1: start_idx = 8
    # Pre species_index=2: start_idx = 16
    # Pre species_index=3: start_idx = 23
    
    end_idx = start_idx + self.dimensions_per_species[species_index]
    # Pre species_index=0: end_idx = 0 + 8 = 8
    # Pre species_index=1: end_idx = 8 + 8 = 16
    # Pre species_index=2: end_idx = 16 + 7 = 23
    # Pre species_index=3: end_idx = 23 + 7 = 30
    
    solution[start_idx:end_idx] = individual.genes
    # Pre species_index=0: solution[0:8] = individual.genes (8 hodnôt)
    
    # 4. Vložíme gény spolupracovníkov z iných druhov
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
    
    # 5. Ohodnotíme kompletný vektor
    return self.fitness_function(solution)
    # fitness_function zavolá rastrigin_function alebo mathematical_model
    # a vráti fitness hodnotu
```

**Príklad:**
```python
# Druh 0, jedinec s génmi [2.3, -1.5, 0.8, 4.1, -2.9, 1.2, 0.5, -3.7]
# Spolupracovníci:
#   Druh 1, najlepší: [1.0, 2.0, -0.5, 3.2, 1.5, -2.1, 0.3, 4.5]
#   Druh 2, najlepší: [-1.2, 0.8, 2.3, -0.9, 1.1, 0.5, -2.0]
#   Druh 3, najlepší: [0.5, -1.0, 2.1, 0.3, -0.8, 1.2, -1.5]

# Kompletný vektor (30 dimenzií):
solution = [
    2.3, -1.5, 0.8, 4.1, -2.9, 1.2, 0.5, -3.7,  # Druh 0 (pozície 0-7)
    1.0, 2.0, -0.5, 3.2, 1.5, -2.1, 0.3, 4.5,   # Druh 1 (pozície 8-15)
    -1.2, 0.8, 2.3, -0.9, 1.1, 0.5, -2.0,        # Druh 2 (pozície 16-22)
    0.5, -1.0, 2.1, 0.3, -0.8, 1.2, -1.5         # Druh 3 (pozície 23-29)
]

# fitness_function(solution) vypočíta Rastrigin a vráti -316.9
```

---

#### `_evaluate_population(self, species_index)`

**Účel:** Ohodnotí celú populáciu daného druhu.

**Parametre:**
- `species_index`: `int` - ktorý druh hodnotíme

**Čo robí:**
```python
def _evaluate_population(self, species_index):
    for individual in self.populations[species_index].individuals:
        individual.fitness = self._evaluate_individual(species_index, individual)
```

**Kde sa používa:**
- V `run()` - počiatočná evaluácia všetkých populácií

---

#### `_get_best_solution(self)`

**Účel:** Vráti najlepšie riešenie - zostavené z najlepších jedincov z každej populácie.

**Parametre:** Žiadne

**Čo robí krok za krokom:**

```python
def _get_best_solution(self):
    # Vytvoríme vektor dĺžky dimensions
    solution = np.zeros(self.dimensions)
    
    # Pre každý druh
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
```

**Kde sa používa:**
- V `run()` - zaznamenanie najlepšieho riešenia po každej generácii
- V `run()` - vrátenie finálneho riešenia

---

#### `run(self)`

**Účel:** Spustí kooperatívny koevolučný algoritmus.

**Parametre:** Žiadne

**Čo robí krok za krokom:**

```python
def run(self):
    # 1. Počiatočná evaluácia - ohodnotíme všetky populácie
    for i in range(self.num_species):
        self._evaluate_population(i)
    # Teraz má každý jedinec ohodnotenú fitness
    
    # 2. Hlavný evolučný cyklus
    for generation in range(self.generations):  # 100-krát
        # Evoluujeme každú populáciu
        for i in range(self.num_species):  # 4-krát
            # Vytvoríme funkciu, ktorá hodnotí jedinca tohto druhu
            def evaluate_func(ind):
                return self._evaluate_individual(i, ind)
            
            # Evoluujeme populáciu
            self.genetic_algorithms[i].evolve(evaluate_func)
            # Toto vykoná: selekciu, kríženie, mutáciu, evaluáciu, elitizmus
        
        # Zaznamenáme najlepšie riešenie
        best_solution, best_fitness = self._get_best_solution()
        self.best_fitness_history.append(best_fitness)
        self.best_solution_history.append(best_solution.copy())
        
        # Každých 10 generácií vypíšeme pokrok
        if (generation + 1) % 10 == 0:
            print(f"Generácia {generation + 1}/{self.generations}, "
                  f"najlepšia fitness: {best_fitness:.6f}")
    
    # 3. Vrátime najlepšie riešenie
    return self._get_best_solution()
```

**Výstup:**
- `best_solution`: `np.ndarray` - najlepšie riešenie (vektor dĺžky dimensions)
- `best_fitness`: `float` - fitness hodnota najlepšieho riešenia

**Kde sa používa:**
- V `experiments.py` - `runner.run_experiment()` volá `ccea.run()`

---

## Experimenty (experiments.py) - Detailné Vysvetlenie

### Trieda: `ExperimentRunner`

#### `__init__(self, num_runs=10)`

**Účel:** Vytvorí runner pre spúšťanie experimentov.

**Parametre:**
- `num_runs`: `int` - počet behov pre každú konfiguráciu (default: 10)
  - **Prečo 10:** Štatistická významnosť (priemer, štandardná odchýlka)
  - **Čo znamená:** Každý experiment sa spustí 10-krát a výsledky sa spriemerujú

**Čo robí:**
```python
def __init__(self, num_runs=10):
    self.num_runs = num_runs  # 10
    self.results = []         # Zoznam výsledkov
```

---

#### `run_experiment(self, problem_name, fitness_function, dimensions, bounds, config)`

**Účel:** Spustí experiment s danou konfiguráciou.

**Parametre:**
- `problem_name`: `str` - názov problému (napr. "Rastrigin - Základná konfigurácia")
  - **Odkiaľ pochádza:** Z `main()` - vytvorí sa z názvu konfigurácie
- `fitness_function`: `Callable` - fitness funkcia
  - **Odkiaľ pochádza:** Z `problems.py` - `get_rastrigin_problem()` alebo `get_model_optimization_problem()`
- `dimensions`: `int` - počet dimenzií
  - **Odkiaľ pochádza:** Z `main()` - `dimensions = 30` alebo `20`
- `bounds`: `Tuple[float, float]` - hranice
  - **Odkiaľ pochádza:** Z `problems.py` - vráti sa spolu s fitness funkciou
- `config`: `Dict` - konfigurácia algoritmu
  - **Odkiaľ pochádza:** Z `main()` - jeden z konfiguračných slovníkov
  - **Obsahuje:** `num_species`, `population_size`, `generations`, `mutation_rate`, `crossover_rate`, `collaboration_size`

**Čo robí krok za krokom:**

```python
def run_experiment(self, problem_name, fitness_function, dimensions, bounds, config):
    # 1. Vytlačíme informácie o experimente
    print(f"Experiment: {problem_name}")
    print(f"Konfigurácia: {config}")
    
    # 2. Zoznamy pre ukladanie výsledkov zo všetkých behov
    all_fitnesses = []      # Všetky fitness hodnoty
    all_solutions = []      # Všetky riešenia
    all_times = []          # Všetky časy behu
    convergence_data = []   # História konvergencie pre každý beh
    
    # 3. Spustíme experiment viackrát
    for run in range(self.num_runs):  # 10-krát
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
        # Toto môže trvať niekoľko sekúnd až minút
        
        # Zmeriame čas behu
        elapsed_time = time.time() - start_time
        
        # Uložíme výsledky
        all_fitnesses.append(best_fitness)
        all_solutions.append(best_solution)
        all_times.append(elapsed_time)
        convergence_data.append(ccea.best_fitness_history)
        # best_fitness_history obsahuje fitness pre každú generáciu
        
        print(f"  Fitness: {best_fitness:.6f}, Čas: {elapsed_time:.2f}s")
    
    # 4. Vypočítame štatistiky
    fitnesses_array = np.array(all_fitnesses)
    
    results = {
        'problem': problem_name,
        'config': config,
        'num_runs': self.num_runs,
        'fitness_mean': float(np.mean(fitnesses_array)),      # Priemer
        'fitness_std': float(np.std(fitnesses_array)),       # Štandardná odchýlka
        'fitness_min': float(np.min(fitnesses_array)),        # Minimum
        'fitness_max': float(np.max(fitnesses_array)),       # Maximum
        'time_mean': float(np.mean(all_times)),              # Priemerný čas
        'time_std': float(np.std(all_times)),                # Štandardná odchýlka času
        'convergence': self._average_convergence(convergence_data),  # Priemerná konvergencia
        'all_fitnesses': [float(f) for f in all_fitnesses]   # Všetky fitness hodnoty
    }
    
    return results
```

**Výstup:**
- `results`: `Dict` - slovník so štatistikami experimentu

---

#### `_average_convergence(self, convergence_data)`

**Účel:** Vypočíta priemernú konvergenciu cez všetky behy.

**Parametre:**
- `convergence_data`: `List[List[float]]` - zoznam zoznamov
  - **Odkiaľ pochádza:** Z `run_experiment()` - `ccea.best_fitness_history` pre každý beh
  - **Čo obsahuje:** Každý zoznam obsahuje fitness pre každú generáciu jedného behu

**Čo robí krok za krokom:**

```python
def _average_convergence(self, convergence_data):
    # Nájdeme najdlhšiu históriu
    max_gen = 0
    for conv in convergence_data:
        if len(conv) > max_gen:
            max_gen = len(conv)
    # max_gen = 100 (počet generácií)
    
    # Pre každú generáciu vypočítame priemer cez všetky behy
    averaged = []
    for gen in range(max_gen):  # 100-krát
        values = []
        for conv in convergence_data:
            if gen < len(conv):
                values.append(conv[gen])
        # values obsahuje fitness pre generáciu 'gen' zo všetkých behov
        
        if values:
            averaged.append(float(np.mean(values)))
        # Priemerná fitness pre generáciu 'gen'
    
    return averaged
```

**Príklad:**
```python
# Beh 1: [f1, f2, f3, ..., f100]
# Beh 2: [g1, g2, g3, ..., g100]
# Beh 3: [h1, h2, h3, ..., h100]

# Priemer:
# Generácia 0: (f1 + g1 + h1) / 3
# Generácia 1: (f2 + g2 + h2) / 3
# ...
# Generácia 99: (f100 + g100 + h100) / 3
```

**Kde sa používa:**
- Pre vizualizáciu konvergencie (grafy)

---

#### `print_results(self, results)`

**Účel:** Vytlačí výsledky experimentu.

**Parametre:**
- `results`: `Dict` - výsledky z `run_experiment()`

**Čo robí:**
```python
def print_results(self, results):
    print(f"Výsledky: {results['problem']}")
    print(f"Konfigurácia: {results['config']}")
    print(f"Priemerná fitness: {results['fitness_mean']:.6f} ± {results['fitness_std']:.6f}")
    print(f"Najlepšia fitness: {results['fitness_max']:.6f}")
    print(f"Najhoršia fitness: {results['fitness_min']:.6f}")
    print(f"Priemerný čas: {results['time_mean']:.2f}s ± {results['time_std']:.2f}s")
```

---

### Funkcia: `main()`

**Účel:** Hlavná funkcia, ktorá spúšťa všetky experimenty.

**Parametre:** Žiadne

**Čo robí krok za krokom:**

```python
def main():
    # 1. Vytvoríme runner
    runner = ExperimentRunner(num_runs=10)
    all_results = []
    
    # 2. PROBLÉM 1: Rastrigin
    dimensions = 30
    fitness_func, dims, bounds = get_rastrigin_problem(dimensions)
    optimal_value = get_optimal_value_rastrigin(dimensions)
    
    # Konfigurácie pre testovanie
    configs = [
        {'name': 'Základná konfigurácia', 'num_species': 4, ...},
        {'name': 'Viac druhov', 'num_species': 8, ...},
        ...
    ]
    
    # Pre každú konfiguráciu
    for config in configs:
        config_copy = {k: v for k, v in config.items() if k != 'name'}
        result = runner.run_experiment(...)
        all_results.append(result)
        runner.print_results(result)
    
    # 3. PROBLÉM 2: Model (podobne)
    ...
    
    # 4. Uloženie výsledkov
    with open('experiment_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
```

**Výstup:**
- Vytlačí výsledky na obrazovku
- Uloží výsledky do `experiment_results.json`

---

## Kompletný Príklad Workflowu

### Scenár: Rastrigin, 30 dimenzií, 4 druhy, 50 jedincov, 100 generácií

**Krok 1: Spustenie (`experiments.py` → `main()`)**
```python
dimensions = 30
fitness_func, dims, bounds = get_rastrigin_problem(30)
# fitness_func je funkcia, ktorá prijme 30 čísel a vráti fitness
# bounds = (-5.12, 5.12)
```

**Krok 2: Vytvorenie algoritmu (`CooperativeCoevolution.__init__()`)**
```python
ccea = CooperativeCoevolution(
    fitness_function=fitness_func,
    dimensions=30,
    bounds=(-5.12, 5.12),
    num_species=4,
    population_size=50,
    generations=100
)
```

**Vnútorné kroky:**
1. `_split_dimensions()` → `[8, 8, 7, 7]`
2. Vytvorenie 4 populácií:
   - Druh 0: 50 jedincov, každý s 8 dimenziami
   - Druh 1: 50 jedincov, každý s 8 dimenziami
   - Druh 2: 50 jedincov, každý s 7 dimenziami
   - Druh 3: 50 jedincov, každý s 7 dimenziami
3. Vytvorenie 4 genetických algoritmov

**Krok 3: Počiatočná evaluácia (`run()`)**
```python
for i in range(4):
    self._evaluate_population(i)
```

**Pre Druh 0:**
- Pre každého z 50 jedincov:
  - `_evaluate_individual(0, individual)`
  - Zostaví kompletný vektor (30 dimenzií)
  - Zavolá `fitness_func(vektor)` → `rastrigin_function(vektor)` → vráti `-316.9`
  - `individual.fitness = -316.9`

**Krok 4: Evolučný cyklus - Generácia 1**

**Pre Druh 0:**
1. `GeneticAlgorithm.evolve(evaluate_func)`
2. `selection()` → 50 vybraných jedincov
3. `crossover()` → vytvoria sa noví jedinci
4. `mutation()` → pridajú sa zmeny
5. `evaluate_func(child)` → ohodnotia sa noví jedinci
6. Elitizmus → zachová sa najlepší

**Po každej generácii:**
- `_get_best_solution()` → zostaví najlepšie riešenie
- Zaznamená do histórie

**Krok 5: Finálne riešenie**
```python
best_solution, best_fitness = ccea.run()
# best_solution: vektor blízky [0, 0, ..., 0]
# best_fitness: -0.5 (Rastrigin hodnota = 0.5)
```

**Krok 6: Zbieranie výsledkov (`experiments.py`)**
```python
all_fitnesses.append(best_fitness)
all_times.append(elapsed_time)
convergence_data.append(ccea.best_fitness_history)
```

**Krok 7: Štatistiky**
```python
results = {
    'fitness_mean': np.mean(all_fitnesses),
    'fitness_std': np.std(all_fitnesses),
    ...
}
```

---

## Zhrnutie

Tento dokument poskytuje **ultra-podrobné** vysvetlenie každého kroku, každej funkcie a každého parametra. Každý parameter má vysvetlenie:
- **Čo to je**
- **Odkiaľ pochádza**
- **Čo znamená**
- **Kde sa používa**

S týmto dokumentom by mal byť každý schopný úplne pochopiť, ako funguje celá aplikácia!

