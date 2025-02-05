import csv

from Backend import Constantes
from Frontend import EjecutadorCMD


class EjecutadorExcel:

    def __init__(self,pathExcel,tipo):
        self.path = pathExcel
        self.tipo = tipo

    def leerInstruccion(self):

        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:

                if line_count != 0:
                    comando_parseado = (row[0].split(';'))
                    comando = [0, 0] + comando_parseado
                    if self.tipo == "simular" or self.tipo == "Simular":
                        for i in range(len(comando)):
                            if comando[i] == "":
                                comando[i] = Constantes.CARACTER_NULO_CMD
                        print(comando)
                        EjecutadorCMD.simularCMD(comando)
                        print("Simulación de la fila " + str(line_count) + " terminada")
                    else:
                        if self.tipo == "analizar" or self.tipo == "Analizar":
                            for i in range(len(comando)):
                                if comando[i] == "":
                                    comando[i] = Constantes.CARACTER_NULO_CMD
                            print(comando)
                            EjecutadorCMD.analizarCMD(comando)
                            print("Simulación de la fila " + str(line_count) + " terminada")

                else:
                    line_count+=1
