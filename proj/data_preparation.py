#Przygotowanie danych do analizy

#Ładowanie pakietów i modułów
import csv
from config import Params as p
from operations import *
import numpy as np
import matplotlib.pyplot as plt

#A. Wczytanie daych
# Tworzę puste listy, do których będę wczytywał kolumny danych z pliku csv
Date = []
Time = []
CO_GT = []
PT08_S1_CO = []
NMHC_GT	= []
C6H6_GT = []
PT08_S2_NMHC = []
Nox_GT = []
PT08_S3_Nox	= []
NO2_GT = []
PT08_S4_NO2 = []
PT08_S5_O3 = []
T = []
RH= []
AH = []
CO_level = []

# Tworzę uchwyt na plik
df = open(p.data_file, 'rt')
air_quality = csv.reader(df, delimiter=';')

#Opuszczam pierwszą obserwację (nagłówek)
next(air_quality)

# Iteruję po poszczególnych observationch i dołączam do list
for observation in air_quality:
    Date.append(observation[0])
    Time.append(observation[1])
    CO_GT.append(float(observation[2].replace(',', '.')))
    PT08_S1_CO.append(float(observation[3].replace(',', '.')))
    NMHC_GT.append(float(observation[4].replace(',', '.')))
    C6H6_GT.append(float(observation[5].replace(',', '.')))
    PT08_S2_NMHC.append(float(observation[6].replace(',', '.')))
    Nox_GT.append(float(observation[7].replace(',', '.')))
    PT08_S3_Nox.append(float(observation[8].replace(',', '.')))
    NO2_GT.append(float(observation[9].replace(',', '.')))
    PT08_S4_NO2.append(float(observation[10].replace(',', '.')))
    PT08_S5_O3.append(float(observation[11].replace(',', '.')))
    T.append(float(observation[12].replace(',', '.')))
    RH.append(float(observation[13].replace(',', '.')))
    AH.append(float(observation[14].replace(',', '.')))
#Zamykam uchwyt na plik
df.close()

#B. Podstawowe statystyki
# Tworzę słownik: kluczem jest nazwa zmiennej a wartością - zmienna
variables = {"CO_GT":CO_GT, "PT08_S1_CO":PT08_S1_CO, "NMHC_GT":NMHC_GT, "C6H6_GT":C6H6_GT, "PT08_S2_NMHC":PT08_S2_NMHC, "Nox_GT":Nox_GT, "PT08_S3_Nox": PT08_S3_Nox, "NO2_GT":NO2_GT,
             "PT08_S4_NO2":PT08_S4_NO2, "PT08_S5_O3":PT08_S5_O3, "T":T, "RH":RH, "AH":AH}
histo(variables)

#C. Czyszczenie danych
#Dla brakujących danych w datasecie przyjęto wartość -200.0.
#Na potrzeby ninejszej analizy, zastąpimy tę wartość medianą.

#Tworzę kopię pomocniczą słownika, którą będę poprawiał
variables_corr = variables
corrections(variables_corr)

#Ponieważ w przypadku zmiennej NMHC_GT wartości niepoprawnych jest więcej niż połowa obserwacji - zastąpienie wartości nic nie daje
#W przypadku innych zmiennych zastąpienie błędnej wartości przesuwa wynik w kierunku bardziej zbliżonego do realnego
#Idealnie wartości błędne zostaną zastąpione meedianą liczoną bez wartości błędnej -200.0
#variables_corr_final = {"NMHC_GT":NMHC_GT}
variables_corr_final = variables
corrections_final(variables_corr_final)
histo(variables_corr_final)


#Badanie korelacji
variables_correlation = variables_corr_final
test_correlation(variables_correlation)

#Wizualizacja T i CO_GT na wspólnym wykresie
variables_CO = {"CO_GT":CO_GT}
variables_T = {"T":T}
common_visualisation_2_variables(variables_T, variables_CO)



# Przeprowadzam regresję liniową tylko dla zmiennych silnie skorelowanych dodatnie
#Silne korelacje dodatnie między
#1) PT08_S2_NMHC a: C6H6_GT : 0.981673245516 / PT08_S1_CO : 0.893069642991 / PT08_S4_NO2 : 0.777016978588 / CO_GT : 0.790321338488 / PT08_S5_O3 : 0.880710257499
#2) C6H6_GT a: PT08_S1_CO : 0.88397896334 / PT08_S4_NO2 : 0.764774586697 / CO_GT : 0.802251581903 / PT08_S5_O3 : 0.865863834946
#3) PT08_S1_CO a: CO_GT : 0.775029012384 / PT08_S5_O3 : 0.89949290942
#4)Nox_GT a: NO2_GT : 0.768881291528 / CO_GT : 0.791624000154
#5) CO_GT a:  PT08_S5_O3 : 0.762061522303
#ad.1)
list_pom = []
list_val = ['C6H6_GT', 'PT08_S1_CO', 'PT08_S4_NO2', 'CO_GT', 'PT08_S5_O3']
index = 0
while (index < len(list_val)):
    list1, name1, list2, name2 = gather_data(variables_correlation, 'PT08_S2_NMHC', list_val[index])
    list_pom.append(list1); list_pom.append(name1); list_pom.append(list2); list_pom.append(name2)
    k = (index+1)*4
    linear_regression_simple(list_pom[k-4], list_pom[k-3], list_pom[k-2], list_pom[k-1])
    index += 1

#ad.2)
list_pom = []
list_val = ['PT08_S1_CO', 'PT08_S4_NO2', 'CO_GT', 'PT08_S5_O3']
index = 0
while (index < len(list_val)):
    list1, name1, list2, name2 = gather_data(variables_correlation, 'C6H6_GT', list_val[index])
    list_pom.append(list1); list_pom.append(name1); list_pom.append(list2); list_pom.append(name2)
    k = (index+1)*4
    linear_regression_simple(list_pom[k-4], list_pom[k-3], list_pom[k-2], list_pom[k-1])
    index += 1

#ad.3)
list_pom = []
list_val = ['CO_GT', 'PT08_S4_NO2', 'PT08_S5_O3']
index = 0
while (index < len(list_val)):
    list1, name1, list2, name2 = gather_data(variables_correlation, 'PT08_S1_CO', list_val[index])
    list_pom.append(list1); list_pom.append(name1); list_pom.append(list2); list_pom.append(name2)
    k = (index+1)*4
    linear_regression_simple(list_pom[k-4], list_pom[k-3], list_pom[k-2], list_pom[k-1])
    index += 1

#ad.4)
list_pom = []
list_val = ['NO2_GT', 'CO_GT']
index = 0
while (index < len(list_val)):
    list1, name1, list2, name2 = gather_data(variables_correlation, 'Nox_GT', list_val[index])
    list_pom.append(list1); list_pom.append(name1); list_pom.append(list2); list_pom.append(name2)
    k = (index+1)*4
    linear_regression_simple(list_pom[k-4], list_pom[k-3], list_pom[k-2], list_pom[k-1])
    index += 1

#ad.5)
list_pom = []
list_val = ['PT08_S5_O3']
index = 0
while (index < len(list_val)):
    list1, name1, list2, name2 = gather_data(variables_correlation, 'CO_GT', list_val[index])
    list_pom.append(list1); list_pom.append(name1); list_pom.append(list2); list_pom.append(name2)
    k = (index+1)*4
    linear_regression_simple(list_pom[k-4], list_pom[k-3], list_pom[k-2], list_pom[k-1])
    index += 1



