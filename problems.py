"""
Ukážkové problémy pre testovanie kooperatívneho koevolučného algoritmu
"""

import numpy as np
from typing import Callable, Tuple


# ============================================================================
# PROBLÉM 1: Optimalizácia multivariačnej funkcie (Rastrigin)
# ============================================================================

def rastrigin_function(x: np.ndarray) -> float:
    """
    Rastrigin funkcia - má veľa lokálnych optim, globálne optimum je v bode [0, 0, ..., 0]
    
    f(x) = 10*n + sum(x_i^2 - 10*cos(2*pi*x_i))
    Minimum: f(0, ..., 0) = 0
    """
    n = len(x)
    A = 10
    return A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x))


def get_rastrigin_problem(dimensions: int = 30) -> Tuple[Callable, int, Tuple[float, float]]:
    """
    Vráti Rastrigin problém s daným počtom dimenzií
    
    Returns:
        (fitness_function, dimensions, bounds)
    """
    def fitness(x):
        # Minimalizácia - vrátiť negatívnu hodnotu pre maximalizáciu v GA
        return -rastrigin_function(x)
    
    bounds = (-5.12, 5.12)
    return fitness, dimensions, bounds


# ============================================================================
# PROBLÉM 2: Optimalizácia parametrov matematického modelu
# ============================================================================

def mathematical_model(x: np.ndarray) -> float:
    """
    Optimalizácia parametrov matematického modelu
    
    Model: y = sum(a_i * sin(b_i * x_i) + c_i * cos(d_i * x_i))
    kde a_i, b_i, c_i, d_i sú parametre na optimalizáciu
    
    Cieľ: Minimalizovať chybu medzi modelom a cieľovou funkciou
    """
    n = len(x) // 4  # Každá skupina 4 parametrov (a, b, c, d)
    
    if len(x) % 4 != 0:
        # Doplniť nulami ak je to potrebné
        x = np.pad(x, (0, 4 - (len(x) % 4)), mode='constant')
        n = len(x) // 4
    
    # Cieľová funkcia (čo chceme aproximovať)
    target_value = 100.0
    
    # Vypočítať hodnotu modelu
    model_value = 0.0
    for i in range(n):
        a = x[i * 4]
        b = x[i * 4 + 1]
        c = x[i * 4 + 2]
        d = x[i * 4 + 3]
        
        # Použiť pevné vstupné hodnoty pre model
        input_val = i + 1
        model_value += a * np.sin(b * input_val) + c * np.cos(d * input_val)
    
    # Chyba (RMSE)
    error = (model_value - target_value) ** 2
    
    return error


def get_model_optimization_problem(dimensions: int = 20) -> Tuple[Callable, int, Tuple[float, float]]:
    """
    Vráti problém optimalizácie parametrov modelu
    
    Returns:
        (fitness_function, dimensions, bounds)
    """
    def fitness(x):
        # Minimalizácia - vrátiť negatívnu hodnotu pre maximalizáciu v GA
        return -mathematical_model(x)
    
    bounds = (-10.0, 10.0)
    return fitness, dimensions, bounds


# ============================================================================
# Pomocné funkcie pre evaluáciu
# ============================================================================

def get_optimal_value_rastrigin(dimensions: int) -> float:
    """Vráti optimálnu hodnotu Rastrigin funkcie"""
    return 0.0


def get_optimal_value_model(dimensions: int) -> float:
    """Vráti približnú optimálnu hodnotu pre model (závisí od problému)"""
    # Pre tento model je optimálna hodnota približne 0 (minimálna chyba)
    return 0.0

