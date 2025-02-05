import math
import random

import numpy as np
import pandas as pd

from Backend.Auxiliares import auxiliar_tiempo
from Backend.Manipuladores import Agrupador
from Backend.estadisticasOcupacionHorarias import estadisticasOcupacionHorarias


class SimuladorDeltasEstadistico:


    def __init__(self, matrizDeltas:pd.DataFrame, deltaTime):
        self.matrizDeltas = matrizDeltas.iloc[1:,:]
        self.primerMov = matrizDeltas.iloc[0,:]
        self.nEstaciones = matrizDeltas.shape[1]#INTRODUCIR SIN HORAS.
        self.deltaTime = deltaTime


    def simularDatosEstadisticos_Horas(self, dias: list[int]):

        DeltasPorHoras = round(60/self.deltaTime)
        matrizSoltar,matrizCoger = self.separarMatrizCogerSoltar(self.matrizDeltas)

        # Obtener el número de filas
        num_filas_soltar = len(matrizSoltar)
        num_filas_coger = len(matrizCoger)
        # Crear la nueva columna con valores del 0 al n-1
        nueva_columna_soltar = pd.Series(range(num_filas_soltar))
        nueva_columna_coger = pd.Series(range(num_filas_coger))

        # Insertar la nueva columna en la primera posición
        matrizSoltar.insert(0, 'Utemporal', nueva_columna_soltar)
        matrizCoger.insert(0, 'Utemporal', nueva_columna_coger)
        # Crear una nueva fila con valores a 0
        column_names = matrizCoger.columns
        new_row = pd.DataFrame([0] * len(column_names), index=column_names).transpose()

        # Concatenar la nueva fila al dataframe existente
        matrizSoltar = pd.concat([new_row, matrizSoltar], ignore_index=True)
        matrizCoger = pd.concat([new_row, matrizCoger], ignore_index=True)

        peticionesGeneradas:list[tuple] = [] #Tupla estacion, (hora,dia),tipo = index

        matrizSoltarHoras = Agrupador.colapsarDeltasAcumulacion(matrizSoltar, self.deltaTime, 60)
        matrizCogerHoras = Agrupador.colapsarDeltasAcumulacion(matrizCoger, self.deltaTime, 60)
        estadoInicialBicicletas = self.primerMov.to_list()
        peticionesGeneradas.append(estadoInicialBicicletas)
        for dia in dias:

            for hora in range(24):

                #Calculo indice correspondiente a la matriz horaria.
                indice = (24*dia) + hora
                #Numero de peticiones en esa hora.
                numPeticionesEnHora = (matrizSoltarHoras.iloc[indice,1:] + matrizCogerHoras.iloc[indice,1:]).sum()

                #Calculo los histogramas.
                histograma_coger = matrizCogerHoras.iloc[indice,1:].tolist()
                histograma_soltar = matrizSoltarHoras.iloc[indice, 1:].tolist()


                #Para cada delta que exista en un ahora:
                for delta in range(DeltasPorHoras):

                    if numPeticionesEnHora != 0:
                        porcentaje_Coger = matrizCogerHoras.iloc[indice,1:].sum() / numPeticionesEnHora
                        peticionesPorDelta = round(numPeticionesEnHora/DeltasPorHoras)
                    else:
                        porcentaje_Coger = 0
                        peticionesPorDelta = 0

                    nuevaFila = [0] * self.nEstaciones

                    for peticion in range(peticionesPorDelta):
                        dado = random.uniform(0,1)
                        if dado < porcentaje_Coger:#Simulo peticion de coger.
                            indice_estacion = self.__ruletaProporcional(histograma_coger)
                            nuevaFila[indice_estacion] -=1
                        else:#Simulo peticion de soltar
                            indice_estacion = self.__ruletaProporcional(histograma_soltar)
                            nuevaFila[indice_estacion] += 1
                    peticionesGeneradas.append(nuevaFila)

        return pd.DataFrame(peticionesGeneradas)

    def simularDatosEstadisticos_PeriodoTotal(self, dias):

        matrizSoltar,matrizCoger = self.separarMatrizCogerSoltar(self.matrizDeltas)

        soltar_colapsado = self.colapsarMatriz(matrizSoltar,self.deltaTime)
        cogerCopalsado = self.colapsarMatriz(matrizCoger,self.deltaTime)

        peticionesGeneradas=[]
        # Calculo los histogramas.
        estadoInicialBicicletas = self.primerMov.to_list()
        peticionesGeneradas.append(estadoInicialBicicletas)
        DeltasPorHoras = int(60 / self.deltaTime)
        for dia in range(dias):

            for hora in range(24):
                histograma_coger = cogerCopalsado[hora]
                histograma_soltar = soltar_colapsado[hora]
                porcentaje_Coger = histograma_coger.sum() / (histograma_coger.sum() + histograma_soltar.sum())

                numPeticionesEnHora = histograma_coger.sum()+histograma_soltar.sum()
                peticionesPorDelta = round(numPeticionesEnHora / DeltasPorHoras)

                #Para cada delta que exista en un ahora:
                for delta in range(DeltasPorHoras):


                    nuevaFila = [0] * self.nEstaciones

                    for peticion in range(peticionesPorDelta):
                        dado = random.uniform(0, 1)

                        if dado < porcentaje_Coger:#Simulo peticion de coger.
                            indice_estacion = self.__ruletaProporcional(histograma_coger)
                            nuevaFila[indice_estacion] -=1
                            #peticionesGeneradas.append((indice_estacion,indice_delta,-1))

                        else:#Simulo peticion de soltar
                            indice_estacion = self.__ruletaProporcional(histograma_soltar)
                            nuevaFila[indice_estacion] += 1
                            #peticionesGeneradas.append((indice_estacion, indice_delta, 1))
                    peticionesGeneradas.append(nuevaFila)

        return pd.DataFrame(peticionesGeneradas)

    #Función dada una matriz y su delta colapsa la matriz a un único día (24*nEstaciones)
    def colapsarMatriz(self,matriz:pd.DataFrame,delta):

        horaDelta = 60 / delta
        nEstaciones = matriz.shape[1]

        diasEnMatriz = math.trunc((matriz.shape[0]/horaDelta) / 24)
        horaColapsado = np.array([[0.0]*nEstaciones] * 24)


        for dia in range(diasEnMatriz):
            indice_comienzo_dia,indice_comienzo_final = auxiliar_tiempo.diaToDelta(dia,dia,delta)
            indice_comienzo_final +=1 #El método es para SQL que se comporta diferente.

            for hora in range(24):#Para cada hora del día.

                hora_comienzo_index = int(((horaDelta*hora)) + indice_comienzo_dia)
                hora_final_index = int(hora_comienzo_index + horaDelta)##Comprobar
                horaColapsado[hora] += (matriz.iloc[hora_comienzo_index:hora_final_index].sum())/diasEnMatriz


        return horaColapsado





    # Dado una ruleta con pesos, devuelve un índice aleatorio, este algoritmo fue encontrado en el enlace de wikipedia:
    # https://en.wikipedia.org/wiki/Fitness_proportionate_selection dado que parece facil de entender y aplicar, aunque no es
    # el algoritmo inicial de la ruleta.
    '''
    #Cuando hay 0s, no se muy bien como actuar.
    def __ruletaProporcional(self, pesos):

        probab = []
        prob_anterior = 0.0
        suma_fitness = np.array(pesos).sum()

        for i in range(len(pesos)):  # Recorro todos los pesos para calcular las probabilidades combinadas
            valor = prob_anterior + (pesos[i] / suma_fitness)#RuntimeWarning: invalid value encountered in double_scalars
            #valor = prob_anterior + (pesos[i] / suma_fitness)
            prob_anterior = valor
            probab.append(valor)

        randomNumber = random.random()  # Numero entre 0 e 1.

        j = 0
        indice = 0
        encontrado = False
        while j < len(pesos) and encontrado == False:

            if randomNumber < probab[j]:
                encontrado = True
                indice = j
            j += 1

        return indice
'''

    def __ruletaProporcional(self, pesos):
        np_pesos = np.array(pesos)
        pesos_ruleta = np_pesos/np_pesos.sum()
        return np.random.choice(range(len(pesos_ruleta)), p=pesos_ruleta)

    #Función que sapara en dos matrices la matriz de deltas, para sacar el coger y el sacar.
    def separarMatrizCogerSoltar(self,matriz:pd.DataFrame):
        matrizSoltar =  matriz[matriz > 0].fillna(0)
        matrizCoger = abs(matriz[matriz < 0].fillna(0))
        #matrizCoger.insert(0, 'uTemporal', range(len(matrizCoger))) Pa que he hecho esto????
        #matrizSoltar.insert(0, 'uTemporal', range(len(matrizCoger)))
        return matrizSoltar,matrizCoger

    #Devuelve el histograma medio de varios días en una lista con longitud de la sestaciones.
    def obtenerHistograma(self,matriz:pd.DataFrame,dias:list[int],media):

        eOc = estadisticasOcupacionHorarias(matriz,self.deltaTime)
        return eOc.getOcupacionTodasEstaciones(dias,media=media)

