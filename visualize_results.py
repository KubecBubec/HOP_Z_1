"""
Vizualizácia výsledkov experimentov
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict


def load_results(filename: str = 'experiment_results.json') -> List[Dict]:
    """Načíta výsledky z JSON súboru"""
    with open(filename, 'r') as f:
        return json.load(f)


def plot_convergence(results: List[Dict], problem_name: str):
    """Vykreslí konvergenčné krivky pre daný problém"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    problem_results = [r for r in results if problem_name in r['problem']]
    
    for result in problem_results:
        convergence = result['convergence']
        generations = range(1, len(convergence) + 1)
        label = result['config_name']
        ax.plot(generations, convergence, label=label, linewidth=2)
    
    ax.set_xlabel('Generácia', fontsize=12)
    ax.set_ylabel('Priemerná fitness', fontsize=12)
    ax.set_title(f'Konvergencia: {problem_name}', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'convergence_{problem_name.replace(" ", "_").lower()}.png', dpi=300)
    plt.close()


def create_summary_table(results: List[Dict], problem_name: str) -> str:
    """Vytvorí súhrnnú tabuľku výsledkov"""
    problem_results = [r for r in results if problem_name in r['problem']]
    
    table = f"\n{'='*80}\n"
    table += f"Výsledky: {problem_name}\n"
    table += f"{'='*80}\n"
    table += f"{'Konfigurácia':<30} {'Priemer':<15} {'Std':<15} {'Min':<15} {'Max':<15}\n"
    table += f"{'-'*80}\n"
    
    for result in problem_results:
        config = result['config_name']
        mean = result['fitness_mean']
        std = result['fitness_std']
        min_val = result['fitness_min']
        max_val = result['fitness_max']
        
        table += f"{config:<30} {mean:>14.6f} {std:>14.6f} {min_val:>14.6f} {max_val:>14.6f}\n"
    
    table += f"{'='*80}\n"
    
    return table


def plot_comparison(results: List[Dict]):
    """Vykreslí porovnanie výsledkov"""
    # Zoskupiť podľa problému
    problems = set()
    for r in results:
        problem_base = r['problem'].split(' - ')[0]
        problems.add(problem_base)
    
    for problem in problems:
        plot_convergence(results, problem)
    
    # Porovnanie priemerných výsledkov
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Problém 1
    problem1_results = [r for r in results if 'Rastrigin' in r['problem']]
    if problem1_results:
        configs = [r['config_name'] for r in problem1_results]
        means = [r['fitness_mean'] for r in problem1_results]
        stds = [r['fitness_std'] for r in problem1_results]
        
        x_pos = np.arange(len(configs))
        ax1.bar(x_pos, means, yerr=stds, alpha=0.7, capsize=5)
        ax1.set_xlabel('Konfigurácia', fontsize=12)
        ax1.set_ylabel('Priemerná fitness', fontsize=12)
        ax1.set_title('Rastrigin funkcia', fontsize=14, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(configs, rotation=45, ha='right')
        ax1.grid(True, alpha=0.3, axis='y')
    
    # Problém 2
    problem2_results = [r for r in results if 'Model' in r['problem']]
    if problem2_results:
        configs = [r['config_name'] for r in problem2_results]
        means = [r['fitness_mean'] for r in problem2_results]
        stds = [r['fitness_std'] for r in problem2_results]
        
        x_pos = np.arange(len(configs))
        ax2.bar(x_pos, means, yerr=stds, alpha=0.7, capsize=5)
        ax2.set_xlabel('Konfigurácia', fontsize=12)
        ax2.set_ylabel('Priemerná fitness', fontsize=12)
        ax2.set_title('Optimalizácia modelu', fontsize=14, fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(configs, rotation=45, ha='right')
        ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('comparison.png', dpi=300)
    plt.close()


def main():
    """Hlavná funkcia"""
    try:
        results = load_results()
        
        if not results:
            print("Žiadne výsledky na načítanie!")
            return
        
        # Vytvoriť tabuľky
        print("\n" + "="*80)
        print("SÚHRN VÝSLEDKOV")
        print("="*80)
        
        print(create_summary_table(results, "Rastrigin"))
        print(create_summary_table(results, "Model"))
        
        # Vytvoriť grafy
        print("\nGenerovanie grafov...")
        plot_comparison(results)
        print("Grafy uložené!")
        
        # Uložiť tabuľky do súboru
        with open('results_summary.txt', 'w', encoding='utf-8') as f:
            f.write(create_summary_table(results, "Rastrigin"))
            f.write(create_summary_table(results, "Model"))
        
        print("\nSúhrn uložený do 'results_summary.txt'")
        
    except FileNotFoundError:
        print("Súbor 'experiment_results.json' nebol nájdený!")
        print("Najprv spustite 'experiments.py' na vygenerovanie výsledkov.")
    except Exception as e:
        print(f"Chyba: {e}")


if __name__ == '__main__':
    main()

