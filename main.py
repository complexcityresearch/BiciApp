import sys
from Frontend import EjecutadorCMD
from Frontend.EjecutadorExcel import EjecutadorExcel
from Frontend.VentanaSeleccionHerramienta import VentanaSeleccionHerramienta


def main_app():

    if len(sys.argv)>1:

        comando = sys.argv

        if comando[1] == "simular" or comando[1] == "Simular":
            EjecutadorCMD.simularCMD(comando)

        if comando[1] == "analizar" or comando[1] == "Analizar":
            EjecutadorCMD.analizarCMD(comando)

        if comando[1] == "simuladorDeltasEstadistico":
            EjecutadorCMD.simuladorEstadistico(comando)

        if comando[1] == "auxiliar":
            EjecutadorCMD.restarDirectorios(comando)

        if comando[1] == "macroCSV":
            tipo = comando[2]
            ruta = comando[3]
            ej_excel = EjecutadorExcel(ruta,tipo)
            ej_excel.leerInstruccion()

    else:
        a =  VentanaSeleccionHerramienta()


if __name__ == '__main__':
    main_app()
    sys.exit(1)


