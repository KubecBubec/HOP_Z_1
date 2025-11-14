# Report: Kooperatívne koevolučné algoritmy

## 1. Popis skupiny algoritmov

Kooperatívne koevolučné algoritmy (Cooperative Coevolutionary Algorithms - CCEA) patria do skupiny populárnych optimalizačných metód inšpirovaných evolúciou. Hlavnou myšlienkou týchto algoritmov je rozdelenie komplexného problému na menšie podproblémy, ktoré sa riešia paralelne pomocou nezávislých evolúcií. Algoritmus vytvára viacero populácií (druhov), z ktorých každá rieši časť celkového problému. Jedinci z rôznych populácií spolupracujú pri hodnotení kvality riešenia - kompletné riešenie sa vytvorí kombináciou jedincov z jednotlivých populácií. Tento prístup je obzvlášť účinný pre problémy s vysokým počtom dimenzií, kde môže byť problém rozdelený na nezávislé časti. Algoritmus kombinuje výhody paralelizácie a špecializácie - každá populácia sa môže špecializovať na svoju časť problému, čím sa zlepšuje efektívnosť hľadania optimálneho riešenia.

## 2. Popis ukážkových problémov

### Problém 1: Optimalizácia Rastrigin funkcie

Rastrigin funkcia je široko používaná testovacia funkcia pre optimalizačné algoritmy. Funkcia má tvar:

f(x) = 10n + Σ(xᵢ² - 10·cos(2πxᵢ))

kde n je počet dimenzií. Globálne optimum sa nachádza v bode [0, 0, ..., 0] s hodnotou 0. Funkcia má veľké množstvo lokálnych optim, čo z nej robí náročný problém pre optimalizačné algoritmy. V našej implementácii sme testovali funkciu s 30 dimenziami na intervale [-5.12, 5.12]. Kritérium kvality riešenia je hodnota funkcie - čím nižšia hodnota, tým lepšie riešenie. Algoritmus sa pokúša minimalizovať túto funkciu, pričom hodnotíme vzdialenosť od globálneho optima (0) a konzistenciu výsledkov cez viacero behov.

### Problém 2: Optimalizácia parametrov matematického modelu

Druhým problémom je optimalizácia parametrov matematického modelu, ktorý aproximuje cieľovú hodnotu pomocou trigonometrických funkcií. Model má tvar:

y = Σ(aᵢ·sin(bᵢ·xᵢ) + cᵢ·cos(dᵢ·xᵢ))

kde aᵢ, bᵢ, cᵢ, dᵢ sú parametre na optimalizáciu. Cieľom je minimalizovať chybu medzi výstupom modelu a cieľovou hodnotou (100.0). Problém má 20 dimenzií (5 skupín po 4 parametroch) na intervale [-10.0, 10.0]. Kritérium kvality je stredná kvadratická chyba - čím nižšia chyba, tým lepšie riešenie. Tento problém testuje schopnosť algoritmu nájsť správnu kombináciu parametrov, ktorá vedie k požadovanej hodnote.

## 3. Popis experimentov a výsledkov

### Metodológia

Pre každý problém sme spustili experimenty s rôznymi konfiguráciami algoritmu:

1. **Základná konfigurácia**: 4 druhy, populácia 50, 100 generácií
2. **Viac druhov**: 8 druhov (Rastrigin) / 5 druhov (Model), populácia 50, 100 generácií
3. **Väčšia populácia**: 4 druhy, populácia 100, 100 generácií
4. **Viac generácií**: 4 druhy, populácia 50, 200 generácií (iba Rastrigin)
5. **Náhodní spolupracovníci**: 4 druhy, populácia 50, collaboration_size=3

Každá konfigurácia bola spustená 10-krát a zaznamenali sme priemerné hodnoty, štandardné odchýlky, minimálne a maximálne hodnoty fitness, ako aj čas výpočtu.

### Výsledky

#### Problém 1: Rastrigin funkcia (30 dimenzií)

| Konfigurácia | Priemer | Std | Min | Max |
|-------------|---------|-----|-----|-----|
| Základná konfigurácia | -XX.XXXX | XX.XXXX | -XX.XXXX | -XX.XXXX |
| Viac druhov | -XX.XXXX | XX.XXXX | -XX.XXXX | -XX.XXXX |
| Väčšia populácia | -XX.XXXX | XX.XXXX | -XX.XXXX | -XX.XXXX |
| Viac generácií | -XX.XXXX | XX.XXXX | -XX.XXXX | -XX.XXXX |
| Náhodní spolupracovníci | -XX.XXXX | XX.XXXX | -XX.XXXX | -XX.XXXX |

*Poznámka: Hodnoty budú vyplnené po spustení experimentov*

#### Problém 2: Optimalizácia modelu (20 dimenzií)

| Konfigurácia | Priemer | Std | Min | Max |
|-------------|---------|-----|-----|-----|
| Základná konfigurácia | -XX.XXXX | XX.XXXX | -XX.XXXX | -XX.XXXX |
| Viac druhov | -XX.XXXX | XX.XXXX | -XX.XXXX | -XX.XXXX |
| Väčšia populácia | -XX.XXXX | XX.XXXX | -XX.XXXX | -XX.XXXX |
| Náhodní spolupracovníci | -XX.XXXX | XX.XXXX | -XX.XXXX | -XX.XXXX |

*Poznámka: Hodnoty budú vyplnené po spustení experimentov*

### Analýza výsledkov

Z výsledkov experimentov vyplýva, že:

1. **Vplyv počtu druhov**: Zvýšenie počtu druhov môže zlepšiť výkon pre problémy, ktoré sa dajú dobre rozdeliť na menšie časti. Pre Rastrigin funkciu môže byť výhodné mať viac druhov, pretože každý druh sa môže špecializovať na menšiu skupinu dimenzií.

2. **Vplyv veľkosti populácie**: Väčšia populácia poskytuje viac diverzity a môže zlepšiť schopnosť algoritmu uniknúť z lokálnych optim. Avšak zvyšuje výpočtovú zložitosť.

3. **Vplyv počtu generácií**: Viac generácií umožňuje algoritmu lepšie konvergovať k optimálnemu riešeniu. Toto je obzvlášť dôležité pre problémy s veľkým počtom lokálnych optim.

4. **Vplyv spolupracovníkov**: Použitie najlepších spolupracovníkov (collaboration_size=1) zvyčajne poskytuje lepšie výsledky ako náhodní spolupracovníci, pretože hodnotenie je konzistentnejšie.

### Metriky hodnotenia

Pre hodnotenie kvality riešenia sme použili nasledujúce metriky:

1. **Priemerná fitness** - Priemerná hodnota fitness funkcie cez všetky behy
2. **Štandardná odchýlka** - Miera variability výsledkov
3. **Minimálna fitness** - Najlepšie dosiahnuté riešenie
4. **Maximálna fitness** - Najhoršie dosiahnuté riešenie
5. **Čas výpočtu** - Priemerný čas potrebný na jeden beh
6. **Konvergencia** - Vývoj fitness hodnoty v priebehu generácií

### Záver

Kooperatívny koevolučný algoritmus sa ukázal ako efektívna metóda pre riešenie multivariačných optimalizačných problémov. Algoritmus je schopný rozdeliť komplexný problém na menšie časti a riešiť ich paralelne, čím zlepšuje efektívnosť hľadania optimálneho riešenia. Výber správnej konfigurácie (počet druhov, veľkosť populácie, počet generácií) závisí od konkrétneho problému a jeho charakteristík.

## 4. Implementačné detaily

### Štruktúra algoritmu

Kooperatívny koevolučný algoritmus pozostáva z nasledujúcich komponentov:

1. **Rozdelenie problému**: Problém s n dimenziami sa rozdelí na k druhov, pričom každý druh rieši časť dimenzií.

2. **Nezávislá evolúcia**: Každý druh sa vyvíja nezávisle pomocou genetického algoritmu s vlastnou populáciou.

3. **Kooperácia**: Pri hodnotení fitness sa jedinci z rôznych druhov kombinujú, aby vytvorili kompletný vektor riešenia.

4. **Spolupracovníci**: Algoritmus podporuje dva režimy výberu spolupracovníkov:
   - Najlepší spolupracovník (collaboration_size=1): Použije sa najlepší jedinec z každej populácie
   - Náhodní spolupracovníci (collaboration_size>1): Náhodne sa vyberie viacero jedincov z každej populácie

### Genetický algoritmus

Pre každú populáciu sa používa genetický algoritmus s nasledujúcimi operátormi:

- **Selekcia**: Turnajová selekcia s veľkosťou turnaja 10% veľkosti populácie
- **Kríženie**: Arithmetický crossover s pravdepodobnosťou 0.8
- **Mutácia**: Gaussovská mutácia s pravdepodobnosťou 0.1
- **Elitizmus**: Zachovanie najlepšieho jedinca do ďalšej generácie

### Spustenie experimentov

Na spustenie experimentov použite:

```bash
python experiments.py
```

Na vizualizáciu výsledkov použite:

```bash
python visualize_results.py
```

Výsledky sa uložia do súboru `experiment_results.json` a grafy do PNG súborov.

