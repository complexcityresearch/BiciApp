import random


import pandas as pd

from Backend.Auxiliares import auxiliar_tiempo, auxiliaresCalculos


#Función que extraer unos días y genera un archivo con el nombre indicado
def extraerDias(direccionFicheroOrigen:str, utemporal:int, dias:list, direccionFicheroFinal, mantenerPrimeraFila = False):

    ficheroOrigen = pd.read_csv(direccionFicheroOrigen).to_numpy()
    ficheroOrigen = auxiliaresCalculos.rellenarCon0(ficheroOrigen)
    nuevoFichero = []

    if mantenerPrimeraFila == True:
        if 0 != dias[0]:
            dias.insert(0,0)

    for i in range(len(dias)):

        indice_inicio,indice_final = auxiliar_tiempo.diaToDelta(diaComienzo=dias[i],diaFinal=dias[i],delta=utemporal)

        deltas = ficheroOrigen[int(indice_inicio):int(indice_final+1),:]

        for j in range(deltas.shape[0]):#Para cada fila
            nuevoFichero.append(deltas[j,:])

    pd.DataFrame(nuevoFichero).to_csv(direccionFicheroFinal, index=False)

def extraerStressAplicado(direccionFicheroOrigen:str, direccionFicheroFinal:str,stress:float,tipoStress = 3,listaEstaciones = "All"):

    ficheroOrigen = pd.read_csv(direccionFicheroOrigen).to_numpy()
    ficheroSalida = ficheroOrigen.copy()



    comienzo = 0
    fin = len(ficheroOrigen)

    if tipoStress == 1:
        comienzo = 0
        fin = 0
    if tipoStress == 2:
        comienzo = 1
        fin = len(ficheroOrigen)

    estaciones = []
    if listaEstaciones != "All":
        estaciones = listaEstaciones
    else:
        estaciones = list(range(0,len(ficheroOrigen[0])))


    for row in range(0,len(ficheroOrigen)):
        fila = []
        for estacion in estaciones:
            movimiento = ficheroOrigen[row,estacion]

            # STRESS:
            if stress > 0 and row >= comienzo and row <= fin:

                for m in range(abs(movimiento)):
                    dado = random.uniform(0, 1)
                    if dado < stress:
                        if movimiento > 0:

                            ficheroSalida[row,estacion] += 1

                        else:
                            ficheroSalida[row,estacion] -= 1
            # END STRESS

    pd.DataFrame(ficheroSalida).to_csv(direccionFicheroFinal, index=False)