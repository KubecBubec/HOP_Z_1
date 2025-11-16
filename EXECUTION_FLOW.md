# Tok výkonu aplikácie - Execution Flow

Tento dokument popisuje celý tok výkonu aplikácie od začiatku do konca pre oba experimenty.

## 📋 Prehľad

Aplikácia sa spúšťa cez `main.py` a podporuje niekoľko možností. Pre experimenty sa používa možnosť 1, ktorá spúšťa `experiments.py`.

---

## 🔄 EXPERIMENT 1: Rastrigin funkcia

### Začiatočný bod

**1. `main.py::main()`** (riadok 182)
   - Vytlačí menu a čaká na vstup používateľa
   - Pri voľbe "1" volá `run_experiments()`

**2. `main.py::run_experiments()`** (riadok 35)
   - Výpis informácií o experimentoch
   - Po potvrdení volá `experiments.py::main()`

---

### Hlavný tok experimentu Rastrigin

**3. `experiments.py::main()`** (riadok 144)
   - **Vytvorí `ExperimentRunner`** (riadok 148):
     ```python
     runner = ExperimentRunner(num_runs=10)
     ```
     - Parameter: `num_runs=10` (každý experiment sa spustí 10-krát)

   - **Nastaví problém Rastrigin** (riadky 159-161):
     ```python
     dimensions = 30
     fitness_func, dims, bounds = get_rastrigin_problem(dimensions)
     optimal_value = get_optimal_value_rastrigin(dimensions)
     ```

**4. `problems.py::get_rastrigin_problem(dimensions=30)`** (riadok 35)
   - Vráti:
     - `fitness`: funkcia, ktorá volá `rastrigin_function()` a vráti negatívnu hodnotu
     - `dimensions`: 30
     - `bounds`: (-5.12, 5.12)

**5. `problems.py::get_optimal_value_rastrigin(dimensions)`** (riadok 135)
   - Vráti: `0.0` (optimálna hodnota Rastrigin funkcie)

---

### Spustenie experimentov pre každú konfiguráciu

**6. `experiments.py::main()` - cyklus cez konfigurácie** (riadok 213)

Pre každú z 5 konfigurácií (Základná, Viac druhov, Väčšia populácia, Viac generácií, Náhodní spolupracovníci):

**7. `experiments.py::ExperimentRunner.run_experiment()`** (riadok 28)
   - **Parametre:**
     - `problem_name`: "Rastrigin - [názov konfigurácie]"
     - `fitness_function`: funkcia z `get_rastrigin_problem()`
     - `dimensions`: 30
     - `bounds`: (-5.12, 5.12)
     - `config`: slovník s parametrami (napr. `{'num_species': 4, 'population_size': 50, ...}`)

   - **Vykoná 10 behov** (riadok 51):
     ```python
     for run in range(self.num_runs):  # 10-krát
     ```

---

### Jeden beh experimentu Rastrigin

**8. `experiments.py::ExperimentRunner.run_experiment()` - jeden beh** (riadok 51)

   **a) Vytvorenie algoritmu** (riadky 58-68):
   ```python
   ccea = CooperativeCoevolution(
       fitness_function=fitness_func,      # funkcia z Rastrigin problému
       dimensions=30,
       bounds=(-5.12, 5.12),
       num_species=config['num_species'],      # napr. 4
       population_size=config['population_size'], # napr. 50
       generations=config['generations'],      # napr. 100
       mutation_rate=config['mutation_rate'],  # napr. 0.1
       crossover_rate=config['crossover_rate'], # napr. 0.8
       collaboration_size=config['collaboration_size'] # napr. 1
   )
   ```

**9. `cooperative_coevolution.py::CooperativeCoevolution.__init__()`** (riadok 181)
   - **Parametre:**
     - `fitness_function`: funkcia, ktorá volá `rastrigin_function()` a vráti negatívnu hodnotu
     - `dimensions`: 30
     - `bounds`: (-5.12, 5.12)
     - `num_species`: 4 (pre základnú konfiguráciu)
     - `population_size`: 50
     - `generations`: 100
     - `mutation_rate`: 0.1
     - `crossover_rate`: 0.8
     - `collaboration_size`: 1

   - **Rozdelí dimenzie** (riadok 216):
     ```python
     self.dimensions_per_species = self._split_dimensions()
     ```

**10. `cooperative_coevolution.py::CooperativeCoevolution._split_dimensions()`** (riadok 234)
    - Vypočíta: 30 dimenzií / 4 druhy = 7-8 dimenzií na druh
    - Vráti: `[8, 8, 7, 7]` (prvé dva druhy majú 8 dimenzií, ďalšie dva majú 7)

   - **Vytvorí populácie** (riadky 222-228):
     ```python
     for dims in self.dimensions_per_species:  # pre každý druh
         pop = Population(population_size, dims, bounds)
         ga = GeneticAlgorithm(pop, mutation_rate, crossover_rate)
     ```

**11. `cooperative_coevolution.py::Population.__init__(size=50, dimension=8, bounds=(-5.12, 5.12))`** (riadok 29)
    - Vytvorí 50 jedincov, každý s 8 dimenziami (pre prvý druh)
    - Volá `_create_initial_population()`

**12. `cooperative_coevolution.py::Population._create_initial_population()`** (riadok 41)
    - Pre každého jedinca:
      ```python
      genes = np.random.uniform(-5.12, 5.12, 8)  # náhodné hodnoty
      individuals.append(Individual(genes))
      ```

**13. `cooperative_coevolution.py::GeneticAlgorithm.__init__(population, mutation_rate=0.1, crossover_rate=0.8)`** (riadok 70)
    - Uloží referenciu na populáciu a parametre

---

**14. `cooperative_coevolution.py::CooperativeCoevolution.run()`** (riadok 333)
    - **Počiatočná evaluácia** (riadky 336-337):
      ```python
      for i in range(self.num_species):  # pre každý druh (4x)
          self._evaluate_population(i)
      ```

**15. `cooperative_coevolution.py::CooperativeCoevolution._evaluate_population(species_index)`** (riadok 309)
    - Pre každého jedinca v populácii:
      ```python
      individual.fitness = self._evaluate_individual(species_index, individual)
      ```

**16. `cooperative_coevolution.py::CooperativeCoevolution._evaluate_individual(species_index=0, individual)`** (riadok 249)
    - **Vyberie spolupracovníkov** (riadky 258-272):
      - Ak `collaboration_size == 1`: použije najlepšieho z každej populácie
      - Inak: vyberie náhodných jedincov
    
    - **Zostaví kompletný vektor riešenia** (riadky 274-304):
      ```python
      solution = np.zeros(30)  # 30 dimenzií
      # Vloží gény aktuálneho jedinca (napr. prvých 8 dimenzií)
      solution[0:8] = individual.genes
      # Vloží gény spolupracovníkov z iných druhov
      solution[8:16] = collaborator1.genes  # druh 1
      solution[16:23] = collaborator2.genes  # druh 2
      solution[23:30] = collaborator3.genes  # druh 3
      ```
    
    - **Ohodnotí kompletný vektor** (riadok 307):
      ```python
      return self.fitness_function(solution)
      ```
      - Volá `fitness_function(solution)` → ktorá volá `rastrigin_function(solution)` → vráti `-rastrigin_value`

---

### Evolučný cyklus (100 generácií)

**17. `cooperative_coevolution.py::CooperativeCoevolution.run()` - evolučný cyklus** (riadok 340)
    ```python
    for generation in range(self.generations):  # 100 generácií
        # Evoluujeme každú populáciu
        for i in range(self.num_species):  # pre každý druh (4x)
    ```

**18. `cooperative_coevolution.py::GeneticAlgorithm.evolve(evaluate_func)`** (riadok 131)
    - **Selekcia** (riadok 134):
      ```python
      selected = self.selection()
      ```

**19. `cooperative_coevolution.py::GeneticAlgorithm.selection()`** (riadok 77)
    - Turnajová selekcia - vyberie 50 jedincov cez turnaje
    - Veľkosť turnaja: max(2, 10% populácie) = max(2, 5) = 5

**20. `cooperative_coevolution.py::GeneticAlgorithm.evolve()` - pokračovanie** (riadky 136-153)
    - **Kríženie a mutácia** (riadky 138-153):
      ```python
      for i in range(0, len(selected), 2):  # po dvojiciach
          child1, child2 = self.crossover(selected[i], selected[i + 1])
          self.mutation(child1)
          self.mutation(child2)
      ```

**21. `cooperative_coevolution.py::GeneticAlgorithm.crossover(parent1, parent2)`** (riadok 100)
    - S pravdepodobnosťou `crossover_rate` (0.8):
      ```python
      alpha = random.random()
      genes1 = alpha * parent1.genes + (1 - alpha) * parent2.genes
      genes2 = (1 - alpha) * parent1.genes + alpha * parent2.genes
      ```

**22. `cooperative_coevolution.py::GeneticAlgorithm.mutation(individual)`** (riadok 116)
    - Pre každý gén s pravdepodobnosťou `mutation_rate` (0.1):
      ```python
      mutation_strength = (5.12 - (-5.12)) * 0.1 = 1.024
      individual.genes[i] += np.random.normal(0, 1.024)
      # Ohraničí hodnoty v rámci bounds
      ```

**23. `cooperative_coevolution.py::GeneticAlgorithm.evolve()` - evaluácia** (riadky 158-163)
    - **Ohodnotí novú populáciu** (riadky 159-160):
      ```python
      for individual in new_population:
          individual.fitness = evaluate_func(individual)
      ```
      - `evaluate_func` je lambda funkcia, ktorá volá `_evaluate_individual()` (pozri krok 16)

    - **Elitizmus** (riadky 165-175):
      - Zachová najlepšieho jedinca z predchádzajúcej generácie

**24. `cooperative_coevolution.py::CooperativeCoevolution.run()` - zaznamenanie výsledkov** (riadky 350-358)
    - Po každej generácii:
      ```python
      best_solution, best_fitness = self._get_best_solution()
      self.best_fitness_history.append(best_fitness)
      ```
      - Každých 10 generácií vypíše pokrok

**25. `cooperative_coevolution.py::CooperativeCoevolution._get_best_solution()`** (riadok 314)
    - Zostaví riešenie z najlepších jedincov z každej populácie
    - Ohodnotí ho a vráti

---

### Návrat z behu experimentu

**26. `cooperative_coevolution.py::CooperativeCoevolution.run()` - návrat** (riadok 361)
    - Vráti: `(best_solution, best_fitness)`

**27. `experiments.py::ExperimentRunner.run_experiment()` - uloženie výsledkov** (riadky 71-82)
    - Uloží výsledky pre tento beh:
      ```python
      all_fitnesses.append(best_fitness)
      all_solutions.append(best_solution)
      all_times.append(elapsed_time)
      convergence_data.append(ccea.best_fitness_history)
      ```

---

### Dokončenie experimentu Rastrigin

**28. `experiments.py::ExperimentRunner.run_experiment()` - štatistiky** (riadky 84-102)
    - Po 10 behoch vypočíta štatistiky:
      ```python
      fitness_mean = np.mean(all_fitnesses)
      fitness_std = np.std(all_fitnesses)
      fitness_min = np.min(all_fitnesses)
      fitness_max = np.max(all_fitnesses)
      time_mean = np.mean(all_times)
      convergence = _average_convergence(convergence_data)
      ```

**29. `experiments.py::ExperimentRunner.run_experiment()` - návrat** (riadok 102)
    - Vráti slovník s výsledkami

**30. `experiments.py::main()` - uloženie** (riadky 230-236)
    - Pridá výsledky do `all_results`
    - Vytlačí výsledky cez `runner.print_results()`

---

## 🔄 EXPERIMENT 2: Optimalizácia parametrov modelu

### Tok je podobný, ale s týmito rozdielmi:

**3. `experiments.py::main()` - nastavenie problému Model** (riadky 246-248)
   ```python
   dimensions = 20
   fitness_func, dims, bounds = get_model_optimization_problem(dimensions)
   optimal_value = get_optimal_value_model(dimensions)
   ```

**4. `problems.py::get_model_optimization_problem(dimensions=20)`** (riadok 106)
   - Vráti:
     - `fitness`: funkcia, ktorá volá `mathematical_model()` a vráti negatívnu hodnotu chyby
     - `dimensions`: 20
     - `bounds`: (-10.0, 10.0)

**5. `problems.py::mathematical_model(x)`** (riadok 64)
   - Vypočíta:
     ```python
     model_value = sum(a_i * sin(b_i * input_val) + c_i * cos(d_i * input_val))
     error = (model_value - 100.0) ** 2
     return error  # čím menšia, tým lepšie
     ```

**10. `cooperative_coevolution.py::CooperativeCoevolution._split_dimensions()`**
    - Pre 20 dimenzií a 4 druhy: `[5, 5, 5, 5]`

**Ostatné kroky sú identické** - len sa mení:
- Počet dimenzií: 20 namiesto 30
- Bounds: (-10.0, 10.0) namiesto (-5.12, 5.12)
- Fitness funkcia: `mathematical_model()` namiesto `rastrigin_function()`
- Počet konfigurácií: 4 namiesto 5

---

## 💾 Finálne uloženie výsledkov

**31. `experiments.py::main()` - uloženie všetkých výsledkov** (riadky 320-327)
   ```python
   with open('experiment_results.json', 'w') as f:
       json.dump(all_results, f, indent=2)
   ```
   - Uloží všetky výsledky z oboch experimentov do JSON súboru

---

## 📊 Súhrn toku volania funkcií

### Rastrigin experiment:
```
main() 
  → run_experiments()
    → experiments.main()
      → ExperimentRunner(num_runs=10)
      → get_rastrigin_problem(30)
      → get_optimal_value_rastrigin(30)
      → [Pre každú konfiguráciu]:
        → runner.run_experiment(...)
          → [10-krát]:
            → CooperativeCoevolution(...)
              → _split_dimensions()
              → Population(...) × 4
                → _create_initial_population()
              → GeneticAlgorithm(...) × 4
              → run()
                → _evaluate_population() × 4
                  → _evaluate_individual()
                    → fitness_function()
                      → rastrigin_function()
                → [100 generácií]:
                  → genetic_algorithms[i].evolve()
                    → selection()
                    → crossover()
                    → mutation()
                    → evaluate_func()
                      → _evaluate_individual()
                        → fitness_function()
                          → rastrigin_function()
                  → _get_best_solution()
            → uloženie výsledkov
          → výpočet štatistík
      → uloženie do JSON
```

### Model experiment:
```
main() 
  → run_experiments()
    → experiments.main()
      → ExperimentRunner(num_runs=10)
      → get_model_optimization_problem(20)
      → get_optimal_value_model(20)
      → [Pre každú konfiguráciu]:
        → runner.run_experiment(...)
          → [10-krát]:
            → CooperativeCoevolution(...)
              → [rovnaký tok ako Rastrigin]
              → fitness_function()
                → mathematical_model()
          → výpočet štatistík
      → uloženie do JSON
```

---

## 🔑 Kľúčové funkcie a ich parametre

### `CooperativeCoevolution.__init__()`
- **Vstupné parametre:**
  - `fitness_function`: funkcia (x) → fitness hodnota
  - `dimensions`: int (30 pre Rastrigin, 20 pre Model)
  - `bounds`: tuple (min, max)
  - `num_species`: int (napr. 4)
  - `population_size`: int (napr. 50)
  - `generations`: int (napr. 100)
  - `mutation_rate`: float (napr. 0.1)
  - `crossover_rate`: float (napr. 0.8)
  - `collaboration_size`: int (napr. 1)

### `ExperimentRunner.run_experiment()`
- **Vstupné parametre:**
  - `problem_name`: str (napr. "Rastrigin - Základná konfigurácia")
  - `fitness_function`: funkcia
  - `dimensions`: int
  - `bounds`: tuple
  - `config`: dict s parametrami algoritmu

### `_evaluate_individual()`
- **Vstupné parametre:**
  - `species_index`: int (ktorý druh hodnotíme)
  - `individual`: Individual (jedinec, ktorého hodnotíme)
  - `collaborators`: list (voliteľné, inak sa vyberú automaticky)

- **Výstup:**
  - Fitness hodnota (float)

---

## 📝 Poznámky

1. **Každý experiment sa spúšťa 10-krát** pre štatistickú významnosť
2. **Každý beh evolvuje 100 generácií** (konfigurovateľné)
3. **Problém sa delí na druhy** (napr. 30 dimenzií → 4 druhy po 7-8 dimenziách)
4. **Každý druh má vlastnú populáciu a genetický algoritmus**
5. **Hodnotenie jedincov vyžaduje spolupracovníkov** z iných druhov
6. **Výsledky sa ukladajú po každom behu** a po dokončení všetkých konfigurácií sa uložia do JSON

