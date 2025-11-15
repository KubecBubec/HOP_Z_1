# Vysvetlenie Workflowu - Krok za Krokom

Tento dokument vysvetľuje, ako funguje kód na konkrétnych príkladoch pre oba problémy.

---

## 🎯 PROBLÉM 1: Rastrigin funkcia (30 dimenzií)

### Krok 1: Spustenie experimentu (`experiments.py`)

```python
# V main() funkcii:
dimensions = 30
fitness_func, dims, bounds = get_rastrigin_problem(30)
```

**Čo sa stane:**
- Zavolá sa `get_rastrigin_problem(30)` z `problems.py`
- Vráti sa funkcia `fitness`, ktorá prijme 30 čísel a vráti fitness hodnotu
- `bounds = (-5.12, 5.12)` - hodnoty musia byť medzi -5.12 a 5.12

**Čo sa pošle ďalej:**
- `fitness_func` → použije sa v CCEA algoritme
- `dimensions = 30` → algoritmus vie, že má 30 dimenzií
- `bounds = (-5.12, 5.12)` → algoritmus vie, v akých hraniciach má hľadať

---

### Krok 2: Vytvorenie algoritmu (`cooperative_coevolution.py`)

```python
# V experiments.py:
ccea = CooperativeCoevolution(
    fitness_function=fitness_func,  # z problems.py
    dimensions=30,
    bounds=(-5.12, 5.12),
    num_species=4,      # Rozdelíme na 4 druhy
    population_size=50, # 50 jedincov v každej populácii
    generations=100     # 100 generácií evolúcie
)
```

**Čo sa stane v `__init__`:**
1. **Rozdelenie dimenzií:** `_split_dimensions()`
   - 30 dimenzií / 4 druhy = 7.5
   - Zaokrúhli sa: `[8, 8, 7, 7]`
   - Druh 0: dimenzie 0-7 (8 dimenzií)
   - Druh 1: dimenzie 8-15 (8 dimenzií)
   - Druh 2: dimenzie 16-22 (7 dimenzií)
   - Druh 3: dimenzie 23-29 (7 dimenzií)

2. **Vytvorenie populácií:**
   - Druh 0: `Population(50, 8, (-5.12, 5.12))` → 50 jedincov, každý s 8 dimenziami
   - Druh 1: `Population(50, 8, (-5.12, 5.12))` → 50 jedincov, každý s 8 dimenziami
   - Druh 2: `Population(50, 7, (-5.12, 5.12))` → 50 jedincov, každý s 7 dimenziami
   - Druh 3: `Population(50, 7, (-5.12, 5.12))` → 50 jedincov, každý s 7 dimenziami

3. **Inicializácia populácií:**
   - Pre každú populáciu sa zavolá `_create_initial_population()`
   - Vytvorí sa 50 jedincov s náhodnými hodnotami
   - Príklad pre Druh 0, jedinec 1: `genes = [2.3, -1.5, 0.8, 4.1, -2.9, 1.2, 0.5, -3.7]`

**Čo sa pošle ďalej:**
- 4 populácie, každá s 50 jedincami
- 4 genetické algoritmy (jeden pre každú populáciu)

---

### Krok 3: Počiatočná evaluácia (`run()` metóda)

```python
# V CooperativeCoevolution.run():
for i in range(4):  # Pre každý druh
    self._evaluate_population(i)
```

**Čo sa stane pre Druh 0:**

1. **Pre každého jedinca v populácii:**
   - Zavolá sa `_evaluate_individual(0, individual)`

2. **V `_evaluate_individual()`:**
   - **Výber spolupracovníkov:**
     - Druh 1: `get_best()` → najlepší jedinec (zatiaľ náhodný, lebo ešte neboli ohodnotení)
     - Druh 2: `get_best()` → najlepší jedinec
     - Druh 3: `get_best()` → najlepší jedinec
   
   - **Zostavenie kompletného vektora:**
     - Aktuálny jedinec (Druh 0): `[2.3, -1.5, 0.8, 4.1, -2.9, 1.2, 0.5, -3.7]` → pozície 0-7
     - Spolupracovník z Druhu 1: `[1.0, 2.0, -0.5, 3.2, 1.5, -2.1, 0.3, 4.5]` → pozície 8-15
     - Spolupracovník z Druhu 2: `[-1.2, 0.8, 2.3, -0.9, 1.1, 0.5, -2.0]` → pozície 16-22
     - Spolupracovník z Druhu 3: `[0.5, -1.0, 2.1, 0.3, -0.8, 1.2, -1.5]` → pozície 23-29
     
     - **Kompletný vektor (30 dimenzií):**
       ```
       [2.3, -1.5, 0.8, 4.1, -2.9, 1.2, 0.5, -3.7,  # Druh 0 (pozície 0-7)
        1.0, 2.0, -0.5, 3.2, 1.5, -2.1, 0.3, 4.5,   # Druh 1 (pozície 8-15)
        -1.2, 0.8, 2.3, -0.9, 1.1, 0.5, -2.0,       # Druh 2 (pozície 16-22)
        0.5, -1.0, 2.1, 0.3, -0.8, 1.2, -1.5]       # Druh 3 (pozície 23-29)
       ```

3. **Hodnotenie:**
   - Zavolá sa `fitness_func(completný vektor)`
   - To zavolá `rastrigin_function(completný vektor)` z `problems.py`
   - Vypočíta sa: `10*30 + sum(x_i^2 - 10*cos(2*pi*x_i))`
   - Príklad výsledok: `300 + 45.2 - 28.3 = 316.9`
   - Vráti sa negatívna hodnota: `-316.9` (lebo algoritmus maximalizuje, ale Rastrigin minimalizuje)
   - Toto je `fitness` hodnota jedinca

**Čo sa pošle ďalej:**
- Každý jedinec má teraz `fitness` hodnotu
- Najlepší jedinec v každej populácii je označený

---

### Krok 4: Evolučný cyklus - Generácia 1 (`run()` metóda)

```python
for generation in range(100):  # 100 generácií
    for i in range(4):  # Pre každý druh
        # Evoluovať populáciu
```

**Čo sa stane pre Druh 0:**

1. **Vytvorenie evaluačnej funkcie:**
   ```python
   def evaluate_func(ind):
       return self._evaluate_individual(0, ind)
   ```

2. **Evolúcia populácie (`GeneticAlgorithm.evolve()`):**
   
   **a) Selekcia (`selection()`):**
   - Pre každého jedinca v novej populácii (50-krát):
     - Vyberie sa 5 náhodných jedincov (10% z 50)
     - Vyberie sa najlepší z týchto 5
     - Pridá sa do vybraných
   - Výsledok: 50 vybraných jedincov (najlepší majú vyššiu šancu)

   **b) Kríženie (`crossover()`):**
   - Vezme sa pár rodičov: `parent1` a `parent2`
   - S 80% pravdepodobnosťou sa vykoná kríženie:
     - `alpha = 0.3` (náhodné číslo)
     - `child1 = 0.3 * parent1.genes + 0.7 * parent2.genes`
     - `child2 = 0.7 * parent1.genes + 0.3 * parent2.genes`
   - Príklad:
     - `parent1.genes = [2.3, -1.5, 0.8, ...]`
     - `parent2.genes = [1.0, 2.0, -0.5, ...]`
     - `child1 = [1.39, 0.65, -0.11, ...]` (kombinácia)

   **c) Mutácia (`mutation()`):**
   - Pre každý gén s 10% pravdepodobnosťou:
     - Pridá sa náhodná zmena (napr. `+0.5` alebo `-0.3`)
     - Orezá sa na hranice `[-5.12, 5.12]`
   - Príklad: `[1.39, 0.65, -0.11, ...]` → `[1.39, 0.65, 0.15, ...]` (tretí gén sa zmenil)

   **d) Evaluácia:**
   - Pre každého nového jedinca:
     - Zavolá sa `evaluate_func(child)` → `_evaluate_individual(0, child)`
     - Zostaví sa kompletný vektor (s aktuálnymi najlepšími spolupracovníkmi)
     - Vypočíta sa fitness
     - Uloží sa do `child.fitness`

   **e) Elitizmus:**
   - Nájde sa najlepší jedinec z predchádzajúcej generácie
   - Nájde sa najhorší jedinec z novej generácie
   - Ak bol starý lepší, nahradí sa najhorší nový

**Čo sa pošle ďalej:**
- Nová populácia s novými jedincami
- Niektorí jedinci sú lepší ako predtým (kvôli selekcii, kríženiu, mutácii)

---

### Krok 5: Zaznamenanie najlepšieho riešenia

```python
# Po evolúcii všetkých druhov:
best_solution, best_fitness = self._get_best_solution()
```

**Čo sa stane v `_get_best_solution()`:**
1. Zoberie sa najlepší jedinec z každej populácie:
   - Druh 0, najlepší: `[0.1, -0.2, 0.05, ..., 0.08]` (8 dimenzií)
   - Druh 1, najlepší: `[0.15, 0.1, -0.05, ..., 0.12]` (8 dimenzií)
   - Druh 2, najlepší: `[0.08, -0.1, 0.12, ..., 0.05]` (7 dimenzií)
   - Druh 3, najlepší: `[0.12, 0.08, -0.15, ..., 0.1]` (7 dimenzií)

2. Zostaví sa kompletný vektor:
   ```
   [0.1, -0.2, 0.05, ..., 0.08,    # Druh 0
    0.15, 0.1, -0.05, ..., 0.12,   # Druh 1
    0.08, -0.1, 0.12, ..., 0.05,   # Druh 2
    0.12, 0.08, -0.15, ..., 0.1]    # Druh 3
   ```

3. Vypočíta sa fitness: `fitness_func(completný vektor)`
   - Výsledok: `-15.3` (čo znamená Rastrigin hodnota = 15.3)
   - To je lepšie ako počiatočných `-316.9`!

**Čo sa pošle ďalej:**
- `best_fitness_history.append(-15.3)` → uloží sa do histórie
- `best_solution_history.append(completný vektor)` → uloží sa riešenie

---

### Krok 6: Opakovanie pre ďalšie generácie

**Generácia 2:**
- Všetky druhy sa znovu evolvujú
- Teraz už majú lepšie spolupracovníky (z generácie 1)
- Nové jedince sa hodnotia s lepšími spolupracovníkmi
- Výsledok: `best_fitness = -8.5` (lepšie!)

**Generácia 3:**
- Ešte lepšie spolupracovníci
- Výsledok: `best_fitness = -4.2` (ešte lepšie!)

**...**

**Generácia 100:**
- Najlepšie spolupracovníci z generácie 99
- Výsledok: `best_fitness = -0.5` (veľmi blízko optimu 0!)

---

### Krok 7: Finálne riešenie

```python
# Po 100 generáciách:
return self._get_best_solution()
```

**Výsledok:**
- `best_solution`: vektor s hodnotami blízkymi `[0, 0, 0, ..., 0]`
- `best_fitness`: `-0.5` (Rastrigin hodnota = 0.5, optimálne je 0)

**Čo sa pošle ďalej:**
- Vráti sa do `experiments.py`
- Uloží sa do `all_fitnesses`, `all_solutions`, `convergence_data`

---

## 🎯 PROBLÉM 2: Optimalizácia parametrov modelu (20 dimenzií)

### Krok 1: Spustenie experimentu

```python
dimensions = 20
fitness_func, dims, bounds = get_model_optimization_problem(20)
```

**Čo sa stane:**
- Zavolá sa `get_model_optimization_problem(20)` z `problems.py`
- Vráti sa funkcia `fitness`, ktorá:
  - Prijme 20 čísel (parametrov)
  - Rozdelí ich na skupiny po 4: `(a, b, c, d)` × 5 skupín
  - Vypočíta: `y = sum(a_i * sin(b_i * i) + c_i * cos(d_i * i))`
  - Cieľ: `y ≈ 100.0`
  - Chyba: `(y - 100.0)^2`
  - Vráti: `-chyba` (lebo algoritmus maximalizuje)

**Čo sa pošle ďalej:**
- `fitness_func` → použije sa v CCEA
- `dimensions = 20`
- `bounds = (-10.0, 10.0)`

---

### Krok 2: Vytvorenie algoritmu

```python
ccea = CooperativeCoevolution(
    fitness_function=fitness_func,
    dimensions=20,
    bounds=(-10.0, 10.0),
    num_species=4,
    population_size=50,
    generations=100
)
```

**Rozdelenie dimenzií:**
- 20 dimenzií / 4 druhy = 5
- `[5, 5, 5, 5]` - každý druh má presne 5 dimenzií
- Druh 0: dimenzie 0-4 (parametre pre skupinu 0 a začiatok skupiny 1)
- Druh 1: dimenzie 5-9 (pokračovanie skupiny 1 a skupina 2)
- Druh 2: dimenzie 10-14 (skupina 3 a začiatok skupiny 4)
- Druh 3: dimenzie 15-19 (pokračovanie skupiny 4)

**Vytvorenie populácií:**
- Každý druh: 50 jedincov, každý s 5 dimenziami
- Príklad pre Druh 0: `genes = [2.3, -1.5, 0.8, 4.1, -2.9]`

---

### Krok 3: Počiatočná evaluácia

**Pre jedinca z Druhu 0:**

1. **Zostavenie kompletného vektora:**
   - Druh 0: `[2.3, -1.5, 0.8, 4.1, -2.9]` → pozície 0-4
   - Druh 1: `[1.0, 2.0, -0.5, 3.2, 1.5]` → pozície 5-9
   - Druh 2: `[-1.2, 0.8, 2.3, -0.9, 1.1]` → pozície 10-14
   - Druh 3: `[0.5, -1.0, 2.1, 0.3, -0.8]` → pozície 15-19
   
   - **Kompletný vektor (20 dimenzií):**
     ```
     [2.3, -1.5, 0.8, 4.1, -2.9,    # Druh 0
      1.0, 2.0, -0.5, 3.2, 1.5,      # Druh 1
      -1.2, 0.8, 2.3, -0.9, 1.1,     # Druh 2
      0.5, -1.0, 2.1, 0.3, -0.8]     # Druh 3
     ```

2. **Hodnotenie v `mathematical_model()`:**
   - Rozdelí sa na skupiny po 4:
     - Skupina 0: `a=2.3, b=-1.5, c=0.8, d=4.1` → `2.3*sin(-1.5*1) + 0.8*cos(4.1*1) = -1.2 + 0.3 = -0.9`
     - Skupina 1: `a=-2.9, b=1.0, c=2.0, d=-0.5` → `-2.9*sin(1.0*2) + 2.0*cos(-0.5*2) = -2.5 + 1.8 = -0.7`
     - Skupina 2: `a=3.2, b=1.5, c=-1.2, d=0.8` → `3.2*sin(1.5*3) + (-1.2)*cos(0.8*3) = 2.1 - 0.9 = 1.2`
     - Skupina 3: `a=2.3, b=-0.9, c=1.1, d=0.5` → `2.3*sin(-0.9*4) + 1.1*cos(0.5*4) = -1.5 + 0.8 = -0.7`
     - Skupina 4: `a=-1.0, b=2.1, c=0.3, d=-0.8` → `-1.0*sin(2.1*5) + 0.3*cos(-0.8*5) = 0.8 + 0.2 = 1.0`
   
   - **Súčet:** `model_value = -0.9 + (-0.7) + 1.2 + (-0.7) + 1.0 = -0.1`
   
   - **Chyba:** `(model_value - 100.0)^2 = (-0.1 - 100.0)^2 = 10001.0`
   
   - **Fitness:** `-10001.0` (veľmi zlé, lebo chceme `model_value ≈ 100.0`)

**Čo sa pošle ďalej:**
- Každý jedinec má `fitness` hodnotu
- Najlepší jedinec má najmenšiu chybu (najväčšiu fitness)

---

### Krok 4: Evolučný cyklus

**Rovnako ako pre Rastrigin:**
1. Selekcia → vyberú sa najlepší
2. Kríženie → vytvoria sa noví jedinci
3. Mutácia → pridajú sa zmeny
4. Evaluácia → ohodnotia sa noví jedinci
5. Elitizmus → zachová sa najlepší

**Rozdiel:**
- Fitness funkcia je iná (`mathematical_model` namiesto `rastrigin_function`)
- Cieľ je iný (`model_value ≈ 100.0` namiesto `x ≈ [0, 0, ..., 0]`)

---

### Krok 5: Postupné zlepšovanie

**Generácia 1:**
- `best_fitness = -5000.0` (chyba = 5000.0)
- `model_value = 50.0` (ďaleko od 100.0)

**Generácia 50:**
- `best_fitness = -100.0` (chyba = 100.0)
- `model_value = 90.0` (bližšie k 100.0)

**Generácia 100:**
- `best_fitness = -5.0` (chyba = 5.0)
- `model_value = 97.8` (veľmi blízko k 100.0!)

---

## 📊 Porovnanie oboch problémov

### Podobnosti:
1. **Rovnaký algoritmus:** Oba používajú CCEA
2. **Rovnaký proces:** Rozdelenie → Evolúcia → Hodnotenie → Zlepšovanie
3. **Rovnaká štruktúra:** Druhy, populácie, genetické algoritmy

### Rozdiely:
1. **Fitness funkcia:**
   - Rastrigin: `10*n + sum(x_i^2 - 10*cos(2*pi*x_i))`
   - Model: `(sum(a_i*sin(b_i*i) + c_i*cos(d_i*i)) - 100)^2`

2. **Cieľ:**
   - Rastrigin: `x = [0, 0, ..., 0]` (minimum)
   - Model: `model_value = 100.0` (špecifická hodnota)

3. **Rozsah:**
   - Rastrigin: `[-5.12, 5.12]`
   - Model: `[-10.0, 10.0]`

4. **Dimenzie:**
   - Rastrigin: 30 dimenzií
   - Model: 20 dimenzií

---

## 🔄 Kompletný tok dát - Príklad

**Scenár:** Rastrigin, Generácia 5, Druh 0, jedinec #23

```
1. experiments.py
   └─> Vytvorí CCEA s fitness_func z problems.py
   
2. CooperativeCoevolution.__init__()
   └─> Rozdelí 30 dimenzií: [8, 8, 7, 7]
   └─> Vytvorí 4 populácie po 50 jedincoch
   
3. CooperativeCoevolution.run()
   └─> Generácia 5, Druh 0
   
4. GeneticAlgorithm.evolve()
   └─> Selekcia: vyberie najlepších jedincov
   └─> Kríženie: vytvorí nových jedincov
   └─> Mutácia: pridá zmeny
   └─> Evaluácia: zavolá evaluate_func(jedinec #23)
   
5. CooperativeCoevolution._evaluate_individual(0, jedinec #23)
   └─> Zoberie najlepších spolupracovníkov z druhov 1, 2, 3
   └─> Zostaví kompletný vektor (30 dimenzií)
   └─> Zavolá fitness_func(vektor)
   
6. problems.py - fitness_func(vektor)
   └─> Zavolá rastrigin_function(vektor)
   └─> Vypočíta: 10*30 + sum(x_i^2 - 10*cos(2*pi*x_i))
   └─> Vráti: -rastrigin_value
   
7. Späť do _evaluate_individual()
   └─> Vráti fitness hodnotu
   
8. Späť do evolve()
   └─> Uloží fitness do jedinca #23
   
9. Po evolúcii všetkých druhov
   └─> _get_best_solution()
   └─> Zostaví najlepšie riešenie
   └─> Zaznamená do histórie
   
10. Po 100 generáciách
    └─> Vráti najlepšie riešenie do experiments.py
    └─> Uloží výsledky
```

---

## 🎓 Kľúčové body pre obhajobu

1. **Rozdelenie problému:**
   - Veľký problém → malé problémy
   - Každý druh rieši svoju časť

2. **Kooperácia:**
   - Jedinci nemôžu byť ohodnotení sami
   - Potrebujú spolupracovníkov
   - To vytvára závislosť medzi druhmi

3. **Evolúcia:**
   - Každý druh sa vyvíja nezávisle
   - Postupne sa zlepšujú všetky druhy
   - Najlepší spolupracovníci vedú k lepším hodnoteniam

4. **Konvergencia:**
   - Algoritmus sa postupne približuje k optimu
   - História fitness ukazuje zlepšovanie

5. **Univerzálnosť:**
   - Rovnaký algoritmus funguje pre rôzne problémy
   - Stačí zmeniť fitness funkciu

---

**Toto vysvetlenie ukazuje presný tok dát a ako sa každá funkcia podieľa na riešení problému!**

