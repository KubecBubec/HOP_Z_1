"""
Ukážkové problémy pre testovanie kooperatívneho koevolučného algoritmu

Obsahuje dva problémy:
1. Rastrigin funkcia - má veľa lokálnych optim
2. Optimalizácia parametrov matematického modelu
"""

import numpy as np


# ============================================================================
# PROBLÉM 1: Rastrigin funkcia
# ============================================================================

def rastrigin_function(x):
    """
    Rastrigin funkcia - má veľa lokálnych optim (vrcholov a dolinek)
    Globálne optimum (najlepšie riešenie) je v bode [0, 0, 0, ..., 0]
    
    Vzorec: f(x) = 10*n + sum(x_i^2 - 10*cos(2*pi*x_i))
    Minimum: f(0, ..., 0) = 0
    """
    n = len(x)  # počet dimenzií
    A = 10
    
    # Vypočítame hodnotu funkcie
    result = A * n
    for i in range(n):
        result += x[i]**2 - A * np.cos(2 * np.pi * x[i])
    
    return result


def get_rastrigin_problem(dimensions=30):
    """
    Vráti Rastrigin problém s daným počtom dimenzií
    
    Parametre:
    - dimensions: koľko dimenzií má problém (napr. 30)
    
    Vráti:
    - fitness_function: funkcia na hodnotenie (čím väčšie, tým lepšie)
    - dimensions: počet dimenzií
    - bounds: hranice pre hodnoty (min, max)
    """
    def fitness(x):
        # Vypočítame hodnotu Rastrigin funkcie
        value = rastrigin_function(x)
        # Vrátime negatívnu hodnotu, lebo algoritmus maximalizuje
        # (čím menšia hodnota Rastrigin, tým lepšie)
        return -value
    
    # Hranice pre hodnoty (štandardné pre Rastrigin)
    bounds = (-5.12, 5.12)
    
    return fitness, dimensions, bounds


# ============================================================================
# PROBLÉM 2: Optimalizácia parametrov matematického modelu
# ============================================================================

def mathematical_model(x):
    """
    Optimalizácia parametrov matematického modelu
    
    Model: y = sum(a_i * sin(b_i * x_i) + c_i * cos(d_i * x_i))
    kde a_i, b_i, c_i, d_i sú parametre, ktoré chceme optimalizovať
    
    Cieľ: Minimalizovať chybu medzi modelom a cieľovou hodnotou
    """
    n = len(x) // 4  # Každá skupina má 4 parametre (a, b, c, d)
    
    # Ak sa nedelí rovnomerne, doplníme nulami
    if len(x) % 4 != 0:
        # Pridáme nuly na koniec
        x = np.pad(x, (0, 4 - (len(x) % 4)), mode='constant')
        n = len(x) // 4
    
    # Cieľová hodnota, ktorú chceme dosiahnuť
    target_value = 100.0
    
    # Vypočítame hodnotu modelu
    model_value = 0.0
    for i in range(n):
        # Zoberieme 4 parametre pre túto skupinu
        a = x[i * 4]      # parameter a
        b = x[i * 4 + 1]  # parameter b
        c = x[i * 4 + 2]  # parameter c
        d = x[i * 4 + 3]  # parameter d
        
        # Použijeme pevné vstupné hodnoty pre model
        input_val = i + 1
        
        # Vypočítame príspevok tejto skupiny
        contribution = a * np.sin(b * input_val) + c * np.cos(d * input_val)
        model_value += contribution
    
    # Vypočítame chybu (RMSE - Root Mean Square Error)
    error = (model_value - target_value) ** 2
    
    return error


def get_model_optimization_problem(dimensions=20):
    """
    Vráti problém optimalizácie parametrov modelu
    
    Parametre:
    - dimensions: koľko dimenzií má problém (napr. 20)
    
    Vráti:
    - fitness_function: funkcia na hodnotenie (čím väčšie, tým lepšie)
    - dimensions: počet dimenzií
    - bounds: hranice pre hodnoty (min, max)
    """
    def fitness(x):
        # Vypočítame chybu modelu
        error = mathematical_model(x)
        # Vrátime negatívnu hodnotu, lebo algoritmus maximalizuje
        # (čím menšia chyba, tým lepšie)
        return -error
    
    # Hranice pre hodnoty parametrov
    bounds = (-10.0, 10.0)
    
    return fitness, dimensions, bounds


# ============================================================================
# Pomocné funkcie pre evaluáciu
# ============================================================================

def get_optimal_value_rastrigin(dimensions):
    """
    Vráti optimálnu hodnotu Rastrigin funkcie
    
    Pre Rastrigin funkciu je optimálna hodnota vždy 0
    (keď sú všetky hodnoty 0)
    """
    return 0.0


def get_optimal_value_model(dimensions):
    """
    Vráti približnú optimálnu hodnotu pre model
    
    Pre tento model je optimálna hodnota približne 0
    (minimálna chyba)
    """
    return 0.0
