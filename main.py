"""
Hlavný skript pre spúšťanie všetkých funkcionalít projektu
Kooperatívny koevolučný algoritmus - HOP Zadanie 1
"""

import os
import sys
from typing import Optional


def clear_screen():
    """Vymaže obrazovku"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Vytlačí hlavičku menu"""
    print("\n" + "="*70)
    print("  KOOPERATÍVNY KOEVOLUČNÝ ALGORITMUS - HOP Zadanie 1")
    print("="*70)


def print_menu():
    """Vytlačí hlavné menu"""
    print("\nHLAVNÉ MENU:")
    print("-" * 70)
    print("1. Spustiť experimenty (experiments.py)")
    print("2. Vizualizovať výsledky a vytvoriť grafy (visualize_results.py)")
    print("3. Zobraziť súhrn výsledkov (textový výstup)")
    print("4. Spustiť jednoduché testy (test_simple.py)")
    print("5. Zobraziť informácie o projekte")
    print("0. Ukončiť program")
    print("-" * 70)


def run_experiments():
    """Spustí experimenty"""
    print("\n" + "="*70)
    print("SPUSTENIE EXPERIMENTOV")
    print("="*70)
    print("\nToto môže trvať dlhšie (každá konfigurácia sa spustí 10-krát).")
    print("Výsledky sa uložia do 'experiment_results.json'")
    
    response = input("\nPokračovať? (a/n): ").strip().lower()
    if response != 'a':
        print("Zrušené.")
        return
    
    try:
        from experiments import main as experiments_main
        experiments_main()
        print("\n✓ Experimenty úspešne dokončené!")
        input("\nStlačte Enter pre pokračovanie...")
    except Exception as e:
        print(f"\n✗ Chyba pri spúšťaní experimentov: {e}")
        import traceback
        traceback.print_exc()
        input("\nStlačte Enter pre pokračovanie...")


def visualize_results():
    """Vizualizuje výsledky a vytvorí grafy"""
    print("\n" + "="*70)
    print("VIZUALIZÁCIA VÝSLEDKOV")
    print("="*70)
    
    if not os.path.exists('experiment_results.json'):
        print("\n✗ Súbor 'experiment_results.json' nebol nájdený!")
        print("Najprv musíte spustiť experimenty (možnosť 1).")
        input("\nStlačte Enter pre pokračovanie...")
        return
    
    try:
        from visualize_results import main as visualize_main
        visualize_main()
        print("\n✓ Vizualizácia úspešne dokončená!")
        print("Grafy sú uložené v aktuálnom adresári.")
        input("\nStlačte Enter pre pokračovanie...")
    except Exception as e:
        print(f"\n✗ Chyba pri vizualizácii: {e}")
        import traceback
        traceback.print_exc()
        input("\nStlačte Enter pre pokračovanie...")


def show_summary():
    """Zobrazí súhrn výsledkov"""
    print("\n" + "="*70)
    print("SÚHRN VÝSLEDKOV")
    print("="*70)
    
    if not os.path.exists('experiment_results.json'):
        print("\n✗ Súbor 'experiment_results.json' nebol nájdený!")
        print("Najprv musíte spustiť experimenty (možnosť 1).")
        input("\nStlačte Enter pre pokračovanie...")
        return
    
    try:
        import json
        from visualize_results import create_summary_table
        
        with open('experiment_results.json', 'r') as f:
            results = json.load(f)
        
        if not results:
            print("\n✗ Žiadne výsledky v súbore!")
            input("\nStlačte Enter pre pokračovanie...")
            return
        
        print(create_summary_table(results, "Rastrigin"))
        print(create_summary_table(results, "Model"))
        
        # Zobrazenie základných štatistík
        print("\n" + "="*70)
        print("ZÁKLADNÉ ŠTATISTIKY")
        print("="*70)
        
        rastrigin_results = [r for r in results if 'Rastrigin' in r['problem']]
        model_results = [r for r in results if 'Model' in r['problem']]
        
        if rastrigin_results:
            best_rastrigin = max(rastrigin_results, key=lambda x: x['fitness_mean'])
            print(f"\nNajlepšia konfigurácia pre Rastrigin: {best_rastrigin['config_name']}")
            print(f"  Priemerná fitness: {best_rastrigin['fitness_mean']:.6f}")
        
        if model_results:
            best_model = max(model_results, key=lambda x: x['fitness_mean'])
            print(f"\nNajlepšia konfigurácia pre Model: {best_model['config_name']}")
            print(f"  Priemerná fitness: {best_model['fitness_mean']:.6f}")
        
        input("\nStlačte Enter pre pokračovanie...")
    except Exception as e:
        print(f"\n✗ Chyba pri načítaní výsledkov: {e}")
        import traceback
        traceback.print_exc()
        input("\nStlačte Enter pre pokračovanie...")


def run_simple_tests():
    """Spustí jednoduché testy"""
    print("\n" + "="*70)
    print("SPUSTENIE JEDNODUCHÝCH TESTOV")
    print("="*70)
    
    if not os.path.exists('test_simple.py'):
        print("\n✗ Súbor 'test_simple.py' nebol nájdený!")
        input("\nStlačte Enter pre pokračovanie...")
        return
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'test_simple.py'], 
                              capture_output=False)
        print("\n✓ Testy dokončené!")
        input("\nStlačte Enter pre pokračovanie...")
    except Exception as e:
        print(f"\n✗ Chyba pri spúšťaní testov: {e}")
        import traceback
        traceback.print_exc()
        input("\nStlačte Enter pre pokračovanie...")


def show_project_info():
    """Zobrazí informácie o projekte"""
    print("\n" + "="*70)
    print("INFORMÁCIE O PROJEKTE")
    print("="*70)
    
    print("""
PROJEKT: Kooperatívny koevolučný algoritmus (CCEA)

POPIS:
Tento projekt implementuje kooperatívny koevolučný algoritmus pre riešenie
optimalizačných problémov. Algoritmus rozdeľuje komplexný problém na menšie
časti, ktoré sa riešia paralelne pomocou nezávislých genetických algoritmov.

ŠTRUKTÚRA PROJEKTU:
- cooperative_coevolution.py  - Hlavná implementácia CCEA
- problems.py                 - Testovacie problémy (Rastrigin, Model)
- experiments.py              - Spúšťanie experimentov
- visualize_results.py        - Vizualizácia výsledkov
- test_simple.py              - Jednoduché testy
- CODE_EXPLANATION.md         - Detailné vysvetlenie kódu
- REPORT.md                   - Správa o projekte

TESTOVACIE PROBLÉMY:
1. Rastrigin funkcia (30 dimenzií)
   - Multivariačná optimalizácia s veľkým počtom lokálnych optim
   - Globálne optimum: [0, 0, ..., 0] s hodnotou 0

2. Optimalizácia parametrov matematického modelu (20 dimenzií)
   - Optimalizácia parametrov trigonometrického modelu
   - Cieľ: Minimalizovať chybu medzi modelom a cieľovou hodnotou

POUŽITIE:
1. Spustite experimenty (možnosť 1) - vygeneruje experiment_results.json
2. Vizualizujte výsledky (možnosť 2) - vytvorí grafy a tabuľky
3. Zobrazte súhrn (možnosť 3) - textový výstup výsledkov

POZNÁMKA:
Experimenty môžu trvať dlhšie, pretože každá konfigurácia sa spustí 10-krát
pre štatistickú významnosť výsledkov.
""")
    
    input("\nStlačte Enter pre pokračovanie...")


def main():
    """Hlavná funkcia programu"""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        try:
            choice = input("\nVyberte možnosť (0-5): ").strip()
            
            if choice == '0':
                print("\nĎakujeme za použitie programu. Dovidenia!")
                break
            elif choice == '1':
                run_experiments()
            elif choice == '2':
                visualize_results()
            elif choice == '3':
                show_summary()
            elif choice == '4':
                run_simple_tests()
            elif choice == '5':
                show_project_info()
            else:
                print("\n✗ Neplatná voľba! Prosím vyberte číslo 0-5.")
                input("Stlačte Enter pre pokračovanie...")
        
        except KeyboardInterrupt:
            print("\n\nProgram bol prerušený používateľom.")
            break
        except Exception as e:
            print(f"\n✗ Neočakávaná chyba: {e}")
            import traceback
            traceback.print_exc()
            input("\nStlačte Enter pre pokračovanie...")


if __name__ == '__main__':
    main()

