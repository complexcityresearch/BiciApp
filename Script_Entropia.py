import math

import pandas as pd

rutaArchivoOcupacion = './Resultados_Simulador/Marzo_Reales/20230530_120627_Ocupacion_Original_ResultadoD15S0.0C1.0.csv'
rutaArchivoOcupacion = './Resultados_Simulador/Marzo_Capacidad_21_Reales/20230531_112509_Ocupacion_Original_ResultadoD15S0.0C1.0.csv'
rutaArchivoCapacidades = './Datos/MarzoCapacidad21_Reales/Seville_2021-03-01_2021-03-31_15min_capacidades.csv'
datos = pd.read_csv(rutaArchivoOcupacion)
capacidades = pd.read_csv(rutaArchivoCapacidades)
nuevosDatos = datos.copy()
def formulaEntropia(bicicletas,capacidad):
    hueco = capacidad - bicicletas

    if bicicletas == 0 or capacidad == 0 or hueco == 0:
        return 0
    return - (bicicletas/capacidad * math.log2(bicicletas/capacidad) + hueco/capacidad * math.log2(hueco/capacidad))


for j in range(1,datos.shape[1]):
    columna = datos.iloc[:,j]
    capacidad = capacidades.iloc[j-1,0]
    nuevosDatos.iloc[:,j] = columna.apply(lambda x: formulaEntropia(x, capacidad))



'''
for i in range(0,datos.shape[0]):
    for j in range(1,datos.shape[1]):
        bicicletas = datos.iloc[i,j]

        entropia = formulaEntropia(bicicletas,capacidades.iloc[j-1,0])
        nuevosDatos.iloc[i,j] = entropia'''

nuevosDatos.to_csv('./matrizEntropiaCapacidad21.csv',index=False)