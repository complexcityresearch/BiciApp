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
        simular_parser = subparsers.add_parser("simular", help="Simular algo")

        simular_parser.add_argument("--rutaEntrada", required=True)
        simular_parser.add_argument("--rutaSalida", required=True)
        simular_parser.add_argument("--comando_stress", required=True)
        simular_parser.add_argument("--tipoStress", required=True)
        simular_parser.add_argument("--coste_andar", required=True)
        simular_parser.add_argument("--delta", required=True)
        # Esto crea una variable "dias" de tipo list[Any]
        simular_parser.add_argument("--dias", action="extend", nargs="+")

        analizar_parser = subparsers.add_parser("analizar",
                                                help="Analizar algo")
        analizar_parser.add_argument("--pathEntrada", required=True)
        analizar_parser.add_argument("--pathSalida", required=True)
        analizar_parser.add_argument("--seleccionAgregacion_matriz",
                                     required=True)
        analizar_parser.add_argument("--deltaDeseado_media", required=True)
        analizar_parser.add_argument("--deltaDeseado_acumulado", required=True)
        analizar_parser.add_argument("--histograma_medio_estacion",
                                     required=True)
        analizar_parser.add_argument("--histograma_acumulado_estacion",
                                     required=True)
        analizar_parser.add_argument("--histograma_dia", required=True)
        analizar_parser.add_argument("--histograma_comparar_estaciones",
                                     required=True)
        analizar_parser.add_argument("--histograma_comparar_matrices",
                                     required=True)
        analizar_parser.add_argument("--mapa_densidad", required=True)
        analizar_parser.add_argument("--mapa_densidad_video", required=True)
        analizar_parser.add_argument("--mapa_voronoi", required=True)
        analizar_parser.add_argument("--mapa_circulo", required=True)
        analizar_parser.add_argument("--mapa_desplazamientos", required=True)
        analizar_parser.add_argument("--filtrado_EstSuperiorValor",
                                     required=True)
        analizar_parser.add_argument("--filtrado_EstSuperiorValorDias",
                                     required=True)
        analizar_parser.add_argument("--filtrado_HorasSuperiorValor",
                                     required=True)
        analizar_parser.add_argument(
            "--filtrado_PorcentajeHoraEstacionMasValor", required=True)

        simulador_delta_parser = subparsers.add_parser(
            "simuladorDeltasEstadistico", help="Simular deltas estadísticos")
        simulador_delta_parser.add_argument("--rutaDeltas")
        simulador_delta_parser.add_argument("--rutaSalida")
        simulador_delta_parser.add_argument("--deltaActual")
        simulador_delta_parser.add_argument("--diasAsimular")
        simulador_delta_parser.add_argument("--ruleta")

        auxiliar_parser = subparsers.add_parser("auxiliar", help="Comando auxiliar")
        auxiliar_parser.add_argument("rutaDirectorio1")
        auxiliar_parser.add_argument("rutaDirectorio2")
        auxiliar_parser.add_argument("rutaDirectorioSalida")

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

        if namespace.command == "simular":
            # Support for ';' separated list.
            if len(namespace.dias) == 1:
                namespace.dias = namespace.dias[0].split(";")

            EjecutadorCMD.simularCMD(comando, namespace)

        if namespace.command == "analizar":
            EjecutadorCMD.analizarCMD(comando, namespace)

        if namespace.command == "simuladorDeltasEstadistico":
            EjecutadorCMD.simuladorEstadistico(comando, namespace)

        if namespace.command == "auxiliar":
            EjecutadorCMD.restarDirectorios(comando, namespace)

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
