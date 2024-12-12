#Función que devuelve en que delta corresponde el inicio de un dia de comienzo y el dinal de un dia final.
import pandas as pd


def diaToDelta(diaComienzo:int,diaFinal:int,delta:int):

    delta_dia = (60/delta) * 24
    indice_comienzo_dia = (diaComienzo * delta_dia)
    indice_final_dia = (diaFinal * delta_dia) + delta_dia - 1


    if indice_final_dia < 0:
        return delta_dia,delta_dia

    return ( indice_comienzo_dia, indice_final_dia)



def devolverInstante(matriz:pd.DataFrame, instante):


    return matriz[matriz.iloc[:,0] == instante]

