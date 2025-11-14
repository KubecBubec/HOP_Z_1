# Kooperatívne koevolučné algoritmy

Implementácia kooperatívneho koevolučného algoritmu (Cooperative Coevolutionary Algorithm - CCEA) pre riešenie optimalizačných problémov.

## Štruktúra projektu

- `cooperative_coevolution.py` - Hlavná implementácia kooperatívneho koevolučného algoritmu
- `problems.py` - Ukážkové problémy pre testovanie (Rastrigin funkcia, optimalizácia modelu)
- `experiments.py` - Skript pre spúšťanie experimentov
- `visualize_results.py` - Skript pre vizualizáciu výsledkov
- `requirements.txt` - Python závislosti

## Inštalácia

```bash
pip install -r requirements.txt
```

## Spustenie

### 1. Spustenie experimentov

```bash
python experiments.py
```

Tento skript spustí experimenty na oboch problémoch s rôznymi konfiguráciami. Výsledky sa uložia do `experiment_results.json`.

### 2. Vizualizácia výsledkov

```bash
python visualize_results.py
```

Tento skript vytvorí grafy konvergencie a porovnania výsledkov. Výstupné súbory:
- `convergence_rastrigin_*.png` - Konvergenčné krivky pre Rastrigin problém
- `convergence_model_*.png` - Konvergenčné krivky pre model problém
- `comparison.png` - Porovnanie výsledkov
- `results_summary.txt` - Textový súhrn výsledkov

## Popis algoritmu

Kooperatívny koevolučný algoritmus rozdeľuje komplexný problém na menšie podproblémy, ktoré sa riešia paralelne pomocou nezávislých evolúcií. Každý druh (species) reprezentuje časť riešenia a vyvíja sa nezávisle pomocou genetického algoritmu. Jedinci z rôznych druhov spolupracujú pri hodnotení fitness funkcie.

## Testovacie problémy

1. **Rastrigin funkcia** - Multivariačná optimalizácia s veľkým počtom lokálnych optim
2. **Optimalizácia parametrov modelu** - Optimalizácia parametrov matematického modelu

## Konfigurácia

Algoritmus podporuje nasledujúce parametre:

- `num_species` - Počet druhov/populácií
- `population_size` - Veľkosť každej populácie
- `generations` - Počet generácií
- `mutation_rate` - Pravdepodobnosť mutácie
- `crossover_rate` - Pravdepodobnosť kríženia
- `collaboration_size` - Počet partnerov pri hodnotení (1 = best, >1 = random)

