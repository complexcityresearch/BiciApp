import sys
import argparse
from Frontend import EjecutadorCMD
from Frontend.EjecutadorExcel import EjecutadorExcel
from Frontend.VentanaSeleccionHerramienta import VentanaSeleccionHerramienta


def main_app():
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(prog="BiciApp",
                                         description="BiciApp desc",
                                         usage="%(prog)s [command]")

        subparsers = parser.add_subparsers(dest="command",
                                           help="Comandos disponibles")
        subparsers.add_parser("simular", help="Simular algo")
        subparsers.add_parser("analizar", help="Analizar algo")
        subparsers.add_parser("simuladorDeltasEstadistico",
                              help="Simular deltas estadísticos")
        subparsers.add_parser("auxiliar", help="Comando auxiliar")

        macros_csv_parser = subparsers.add_parser("macrosCSV",
                                                  help="Procesar macros CSV")
        macros_csv_parser.add_argument("--tipo",
                                       required=True,
                                       help="Tipo de macro")
        macros_csv_parser.add_argument("--ruta",
                                       required=True,
                                       help="Ruta del archivo CSV")

        namespace = parser.parse_args()
        comando = namespace.command

        if namespace.command == "simular" or namespace.command == "Simular":
            EjecutadorCMD.simularCMD(comando)

        if namespace.command == "analizar" or namespace.command == "Analizar":
            EjecutadorCMD.analizarCMD(comando)

        if namespace.command == "simuladorDeltasEstadistico":
            EjecutadorCMD.simuladorEstadistico(comando)

        if namespace.command == "auxiliar":
            EjecutadorCMD.restarDirectorios(comando)

        if namespace.command == "macroCSV":
            tipo = namespace.tipo
            ruta = namespace.ruta
            ej_excel = EjecutadorExcel(ruta, tipo)
            ej_excel.leerInstruccion()

    else:
        VentanaSeleccionHerramienta()


if __name__ == '__main__':
    main_app()
    sys.exit(1)
