import math
import operator
import shutil
from os.path import join
import numpy as np
import pandas as pd
from argparse import Namespace
from matplotlib.pyplot import clf
from Backend import Constantes
from Backend.Auxiliares import auxiliar_ficheros, Extractor, auxiliaresCalculos
from Backend.GuardarCargarDatos import GuardarCargarMatrices
from Backend.OperacionesDeltas.SimuladorDeltasEstadistico import SimuladorDeltasEstadistico
from Backend.Manipuladores import Agrupador
from Backend.Manipuladores.Filtrador import Filtrador
from Backend.Representacion.ManejadorMapas.Manejar_Desplazamientos import Manejar_Desplazamientos
from Backend.Representacion.Mapas.MapaDensidad import MapaDensidad2
from Backend.Representacion.ManejadorMapas.manejar_Voronoi import manejar_Voronoi
from Backend.Representacion.ManejadorMapas.manejar_mapaCirculos import manejar_mapaCirculos
from Backend.estadisticasOcupacionHorarias import estadisticasOcupacionHorarias
from bike_simulator5 import bike_simulator5


def simularCMD(comando: [str], args: None | Namespace = None):
    if args is None:
        rutaEntrada = comando[2]
        rutaSalida = comando[3]
        comando_stress = (comando[4])
        tipoStress = float(comando[5])
        coste_andar = float(comando[6])
        delta = int(comando[7])
    else:
        rutaEntrada = args.rutaEntrada
        rutaSalida = args.rutaSalida
        comando_stress = args.comando_stress
        tipoStress = args.tipoStress
        coste_andar = args.coste_andar
        delta = args.delta

    if '+' in comando_stress:
        estaciones_stress = comando_stress.split('+')[1]
        estaciones_stress = list(map(int,estaciones_stress.split(';')))
        stress = float(comando_stress.split('+')[0])
    else:
        stress = float(comando_stress)
        estaciones_stress = 'All'

    Constantes.DELTA_TIME = delta
    Constantes.COSTE_ANDAR = coste_andar
    Constantes.PORCENTAJE_ESTRES = stress
    Constantes.RUTA_SALIDA = rutaSalida

    ficheros,ficheros_distancia = GuardarCargarMatrices.cargarDatosParaSimular(rutaEntrada)
    archivoCapacidad = auxiliar_ficheros.buscar_archivosEntrada(rutaEntrada, ["capacidades"])[0]
    pd.read_csv(archivoCapacidad).to_csv("capacidades.csv",index=False)
    # Intercambio deltas con la extracción de días.

    if len(comando) > 8 and comando[-1] != Constantes.CARACTER_NULO_CMD:  # Extraer dias es optativo.
        dias = args.dias #list(map(int, comando[8].split(";")))
        path_fichero = join(rutaSalida, auxiliar_ficheros.formatoArchivo("Extraccion_" + str(dias), "csv"))
        Extractor.extraerDias(ficheros[0], delta, dias, path_fichero, mantenerPrimeraFila=True)
        ficheros[0] = path_fichero

    # Intercambio los deltas con el stress.
    if stress > 0:

        ficheroDelta_salidaStress = join(rutaSalida, auxiliar_ficheros.formatoArchivo("Dstress", "csv"))
        Extractor.extraerStressAplicado(ficheros[0], ficheroDelta_salidaStress, stress, tipoStress=int(tipoStress),listaEstaciones=estaciones_stress)

        ficheroTendencias_salidaStress = join(rutaSalida, auxiliar_ficheros.formatoArchivo("Tendencias_stress", "csv"))
        Extractor.extraerStressAplicado(ficheros[5], ficheroTendencias_salidaStress, stress, tipoStress=int(tipoStress),listaEstaciones=estaciones_stress)

        ficheros[0] = ficheroDelta_salidaStress
        ficheros[5] = ficheroTendencias_salidaStress

    bs = bike_simulator5()
    nearest_stations_idx, nearest_stations_distance, initial_movements, real_movements, capacidadInicial, coordenadas = bs.load_data(
        directorios=ficheros, directorios_DiastanciasAndarBicicleta=ficheros_distancia)
    coste, matricesSalida = bs.evaluate_solution(capacidadInicial, initial_movements, real_movements,
                                                 nearest_stations_idx, nearest_stations_distance)
    resumen = auxiliar_ficheros.hacerResumenMatricesSalida(matricesSalida)

    auxiliar_ficheros.guardarMatricesEnFicheros(matricesSalida, resumen,Constantes.RUTA_SALIDA)

    pd.DataFrame(Constantes.COORDENADAS).to_csv(join(Constantes.RUTA_SALIDA, "coordenadas" + ".csv"), index=False)
    archivoCapacidad = auxiliar_ficheros.buscar_archivosEntrada(rutaEntrada, ["capacidades"])[0]
    pd.read_csv(archivoCapacidad).to_csv(join(rutaSalida, "capacidades.csv"), index=False)


def analizarCMD(comando: [str], args: None | Namespace = None):
    if args is None:
        pathEntrada = comando[2]
        pathSalida = comando[3]
        seleccionAgregacion_matriz = comando[4]
        deltaDeseado_media = comando[5]
        deltaDeseado_acumulado = comando[6]
        histograma_medio_estacion = comando[7]
        histograma_acumulado_estacion = comando[8]
        histograma_dia = comando[9]
        histograma_comparar_estaciones = comando[10]
        histograma_comparar_matrices = comando[11]
        mapa_densidad = comando[12]
        mapa_densidad_video = comando[13]
        mapa_voronoi = comando[14]
        mapa_circulo = comando[15]
        mapa_desplazamientos = comando[16]
        filtrado_EstSuperiorValor = comando[17]
        filtrado_EstSuperiorValorDias = comando[18]
        filtrado_HorasSuperiorValor = comando[19]
        filtrado_PorcentajeHoraEstacionMasValor = comando[20]
    else:
        pathEntrada = args.pathEntrada
        pathSalida = args.pathSalida
        seleccionAgregacion_matriz = args.seleccionAgregacion_matriz
        deltaDeseado_media = args.deltaDeseado_media
        deltaDeseado_acumulado = args.deltaDeseado_acumulado
        histograma_medio_estacion = args.histograma_medio_estacion
        histograma_acumulado_estacion = args.histograma_acumulado_estacion
        histograma_dia = args.histograma_dia
        histograma_comparar_estaciones = args.histograma_comparar_estaciones
        histograma_comparar_matrices = args.histograma_comparar_matrices
        mapa_densidad = args.mapa_densidad
        mapa_densidad_video = args.mapa_densidad_video
        mapa_voronoi = args.mapa_voronoi
        mapa_circulo = args.mapa_circulo
        mapa_desplazamientos = args.mapa_desplazamientos
        filtrado_EstSuperiorValor = args.filtrado_EstSuperiorValor
        filtrado_EstSuperiorValorDias = args.filtrado_EstSuperiorValorDias
        filtrado_HorasSuperiorValor = args.filtrado_HorasSuperiorValor

    matrices, resumentxt = GuardarCargarMatrices.cargarSimulacionesParaAnalisis(pathEntrada)

    Constantes.DELTA_TIME = float(resumentxt[0])
    Constantes.PORCENTAJE_ESTRES = float(resumentxt[1])
    Constantes.COSTE_ANDAR = float(resumentxt[2])
    Constantes.RUTA_SALIDA = pathSalida


    operacion = 1
    if '(-)' in seleccionAgregacion_matriz:
        seleccionAgregacion_matriz = seleccionAgregacion_matriz.split(')')[1]
        operacion = -1

    id_matrices = list(map(int, seleccionAgregacion_matriz.split(";")))

    listaMatrices = Constantes.LISTA_MATRICES

    inicio = 0
    if Constantes.MATRIZ_CUSTOM == None or not -1 in id_matrices:
        matrizDeseada = matrices[listaMatrices[id_matrices[0]]].matrix
        inicio = 1
    else:
        matrizDeseada = Constantes.MATRIZ_CUSTOM.matrix

        inicio = 0

    if len(id_matrices) > 1:
        for i in range(inicio, len(id_matrices)):
            if id_matrices[i] != -1:
                matrizAsumar = matrices[listaMatrices[id_matrices[i]]].matrix

                if operacion == 1:
                    matrizDeseada = Agrupador.agruparMatrices(matrizDeseada, matrizAsumar)
                else:
                    matrizDeseada = Agrupador.sustraerMatrices(matrizDeseada, matrizAsumar)

    matrizDeseada = auxiliaresCalculos.rellenarFilasMatrizDeseada(matrizDeseada,
                                                                  matrices[Constantes.OCUPACION].matrix.shape[0] - 1)

    # Conversion de deltas:

    if deltaDeseado_media != Constantes.CARACTER_NULO_CMD:
        deltaDeseado_media = int(deltaDeseado_media)
        matrizDeseada = Agrupador.colapsarDeltasMedia(matrizDeseada, Constantes.DELTA_TIME, deltaDeseado_media)
        Constantes.DELTA_TIME = deltaDeseado_media

    if deltaDeseado_acumulado != Constantes.CARACTER_NULO_CMD:
        deltaDeseado_acumulado = int(deltaDeseado_acumulado)
        matrizDeseada = Agrupador.colapsarDeltasAcumulacion(matrizDeseada, Constantes.DELTA_TIME,
                                                            deltaDeseado_acumulado)
        Constantes.DELTA_TIME = deltaDeseado_acumulado

    diasMatrizDeseada = int(matrizDeseada.shape[0] / 24)  # En caso de que estén en horas.
    # Guardar matriz delta.
    nombre = auxiliar_ficheros.formatoArchivo("ficheroMatrizDeseada", "csv")
    matrizDeseada.to_csv(join(Constantes.RUTA_SALIDA, nombre), index=False)

    filtrador = Filtrador(matrizDeseada, Constantes.DELTA_TIME)
    # Histogramas:
    eoc = estadisticasOcupacionHorarias(matrizDeseada, Constantes.DELTA_TIME)

    if histograma_medio_estacion != Constantes.CARACTER_NULO_CMD:
        aux_cadena = histograma_medio_estacion.split("-")
        titulo = auxiliar_ficheros.formatoArchivo("GraficaMedia_Estacion" + str(aux_cadena[0]), "png")

        if aux_cadena[1] == 'all':
            dias = list(range(diasMatrizDeseada))
        else:
            dias = list(map(int, aux_cadena[1].split(";")))

        eoc.HistogramaPorEstacion(int(aux_cadena[0]), dias, nombreGrafica=titulo)
    clf()
    if histograma_acumulado_estacion != Constantes.CARACTER_NULO_CMD:
        aux_cadena = histograma_acumulado_estacion.split("-")
        titulo = auxiliar_ficheros.formatoArchivo("GraficaAcumulado_Estacion" + str(aux_cadena[0]), "png")
        if aux_cadena[1] == 'all':
            dias = list(range(diasMatrizDeseada))
        else:
            dias = list(map(int, aux_cadena[1].split(";")))
        eoc.HistogramaAcumulacion(int(aux_cadena[0]), dias, titulo)
    clf()
    if histograma_dia != Constantes.CARACTER_NULO_CMD:
        caracter_media = histograma_dia.split('-')[1]
        if caracter_media == 'M':
            media = True
        else:
            media= False

        frecuencia = False
        if 'Frec' in histograma_dia:
            histograma_dia = histograma_dia.split('-')[0]
            frecuencia = True

        if "all" in histograma_dia:
            dias = list(range(0, int(matrizDeseada.shape[0] / 24)))
        else:

            dias = list(map(int, histograma_dia.split(";")))
        titulo = auxiliar_ficheros.formatoArchivo("Grafica_Dias_" + str(dias), "png")
        eoc.HistogramaOcupacionMedia(dias,frecuencia=frecuencia,media=media)
    clf()
    if histograma_comparar_estaciones != Constantes.CARACTER_NULO_CMD:

        aux_cadena = histograma_comparar_estaciones.split("-")
        estaciones = list(map(int, aux_cadena[0].split(";")))

        titulo = auxiliar_ficheros.formatoArchivo("Grafica_Comparacion_Estaciones_" + str(estaciones), "png")

        diasComparacion = []
        for i in range(len(estaciones)):
            dias_aux = aux_cadena[1].split("#")[i]
            if dias_aux == "all":
                lista_dias = list(range(0, int(matrizDeseada.shape[0] / 24)))
            else:
                lista_dias = list(map(int, dias_aux.split(";")))
            diasComparacion.append(lista_dias)

        eoc.HistogramaCompararEstaciones(estaciones, diasComparacion, nombreGrafica=titulo,
                                         media=deltaDeseado_media != Constantes.CARACTER_NULO_CMD)
    clf()

    if histograma_comparar_matrices != Constantes.CARACTER_NULO_CMD:
        if Constantes.MATRIZ_CUSTOM != None:
            cadenas = histograma_comparar_matrices.split("-")
            deltaMatriz = int(cadenas[0])
            estaciones1 = list(map(int, cadenas[1].split(";")))
            estaciones2 = list(map(int, cadenas[2].split(";")))
            media = cadenas[3] == 'M'

            eoc = estadisticasOcupacionHorarias(matrizDeseada, Constantes.DELTA_TIME)
            titulo = auxiliar_ficheros.formatoArchivo("Grafica_CompararMatrices_", "png")
            eoc.HistogramaCompararMatrices(Constantes.MATRIZ_CUSTOM.matrix, deltaMatriz, estaciones1, estaciones2,
                                           media=media, nombreGrafica=titulo)

    if mapa_densidad != Constantes.CARACTER_NULO_CMD:

        # Compruebo si aplico algun filtro.
        if "+" in mapa_densidad:
            cadena = mapa_densidad.split("+")[0]
            estaciones = list(map(int, mapa_densidad.split("+")[1].split(";")))
        else:
            cadena = mapa_densidad
            estaciones = []

        mapas = list(map(int, cadena.split(";")))
        mapa = MapaDensidad2(Constantes.COORDENADAS)
        mapa.cargarDatos(matrizDeseada, lista_estaciones=estaciones)
        for mapa_representar in mapas:
            instancias_max = matrizDeseada.shape[0]
            instante = int(mapa_representar)
            mapa.representarHeatmap(instante=instante)

    if mapa_densidad_video != Constantes.CARACTER_NULO_CMD:
        if "+" in mapa_densidad_video:
            momentos = mapa_densidad_video.split("+")[0]
            estaciones = list(map(int, mapa_densidad_video.split("+")[1].split(";")))
            texto_estaciones = str(estaciones)
        else:
            momentos = mapa_densidad_video
            estaciones = []
            texto_estaciones = "TODAS"

        momentos = momentos.split(":")

        momentoInicio = int(momentos[0])
        if momentos[1] != "end":
            momentoFinal = int(momentos[1])
        else:
            momentoFinal = len(matrizDeseada) - 1

        mapa = MapaDensidad2(Constantes.COORDENADAS)
        mapa.cargarDatos(matrizDeseada, lista_estaciones=estaciones)
        nombre = auxiliar_ficheros.formatoArchivo(
            "video_densidad" + str(momentoInicio) + "__" + str(momentoFinal) + "_" + texto_estaciones, "mp4")
        print("Generar video con " + str(momentoInicio)+ " " + str(momentoFinal) + " " + str(join(Constantes.RUTA_SALIDA, nombre)))
        mapa.realizarVideoHeatmap(momentoInicio, momentoFinal, rutaSalida=join(Constantes.RUTA_SALIDA, nombre))

    if mapa_voronoi != Constantes.CARACTER_NULO_CMD:
        mapas = list(map(int, mapa_voronoi.split(";")))

        for mapa_representar in mapas:
            man_vor = manejar_Voronoi(matrizDeseada, Constantes.COORDENADAS)
            man_vor.cargarMapaInstante(mapa_representar)
            nombrePNG = auxiliar_ficheros.formatoArchivo("MapaVoronoi_instante" + str(mapa_representar), "png")
            man_vor.realizarFoto(join(Constantes.RUTA_SALIDA, nombrePNG))

    if mapa_circulo != Constantes.CARACTER_NULO_CMD:
        mostrar = False
        if "-" in mapa_circulo:
            mapa_circulo = mapa_circulo.split("-")[0]
            mostrar = True

        if "+" in mapa_circulo:
            cadena = mapa_circulo.split("+")[0]
            estaciones = list(map(int, mapa_circulo.split("+")[1].split(";")))
        else:
            cadena = mapa_circulo
            estaciones = None

        mapas = list(map(int, cadena.split(";")))

        for mapa_representar in mapas:
            man_circulos = manejar_mapaCirculos(matrizDeseada, Constantes.COORDENADAS, mostrarLabels=mostrar, listaEstaciones=estaciones)
            man_circulos.cargarMapaInstante(mapa_representar, listaEstaciones=estaciones)
            nombrePNG = auxiliar_ficheros.formatoArchivo("MapaCirculo_instante" + str(mapa_representar), "png")
            man_circulos.realizarFoto(join(Constantes.RUTA_SALIDA, nombrePNG))

    if mapa_desplazamientos != Constantes.CARACTER_NULO_CMD:
        arrayOpciones = mapa_desplazamientos.split(";")
        matrizDeseada = matrices[Constantes.DESPLAZAMIENTOS].matrix
        deltaOrigen = int(arrayOpciones[1])
        deltaTransformacion = int(arrayOpciones[2])
        if deltaOrigen < deltaTransformacion:
            matrizDeseada = Agrupador.colapsarDesplazamientos(matrizDeseada,deltaOrigen,deltaTransformacion)



        md = Manejar_Desplazamientos(matrizDeseada,Constantes.COORDENADAS,accion=int(arrayOpciones[3]),tipo=int(arrayOpciones[4]))
        md.cargarMapaInstante(int(arrayOpciones[0]))
        nombrePNG = auxiliar_ficheros.formatoArchivo("MapaDensidad_instante" + str((arrayOpciones[0])), "png")
        md.realizarFoto(join(Constantes.RUTA_SALIDA, nombrePNG))


    if filtrado_EstSuperiorValor != Constantes.CARACTER_NULO_CMD:
        # parametros = list(map(int, filtrado_EstSuperiorValor.split(";")))

        parametros = filtrado_EstSuperiorValor.split(";")

        operador, valor, nombreOperador = __obtenerOperador(parametros[0])

        resultado = filtrador.consultarEstacionesSuperioresAUnValor(float(valor), int(parametros[1]),
                                                                    int(parametros[2]), operador=operador)
        auxiliar_ficheros.guardarFicheroFiltrado(texto=str(resultado),
                                                 tipo_filtrado="Estaciones" + nombreOperador + "Valor",
                                                 parametrosConsulta=nombreOperador + str(valor) + "_" + parametros[
                                                     1] + "_" + parametros[2])

    if filtrado_EstSuperiorValorDias != Constantes.CARACTER_NULO_CMD:
        parametros = filtrado_EstSuperiorValorDias.split(";")

        operador, valor, nombreOperador = __obtenerOperador(parametros[0])
        veces = int(parametros[1])

        if parametros[2] != "all":
            dias = list(map(int, parametros[2].split(";")))
        else:
            diasEnMatriz = math.trunc(matrizDeseada.shape[0] / ((60 / Constantes.DELTA_TIME) * 24))
            dias = list(range(0, diasEnMatriz))
            print("Dias seleccionados : " + str(dias))
        diaPerdon = int(parametros[3])

        resultado = filtrador.consultarEstacionesSuperioresAUnValorEnVariosDias(float(valor), int(parametros[1]), dias,
                                                                                diasPerdon=diaPerdon, operador=operador)
        auxiliar_ficheros.guardarFicheroFiltrado(texto=str(resultado),
                                                 tipo_filtrado="Estaciones" + nombreOperador + "Valor",
                                                 parametrosConsulta=nombreOperador + str(valor) + "_" + str(
                                                     veces) + "_" + str(dias) + "_" + str(diaPerdon))

    if filtrado_HorasSuperiorValor != Constantes.CARACTER_NULO_CMD:
        # parametros = list(map(int, filtrado_HorasSuperiorValor.split(";")))
        parametros = filtrado_HorasSuperiorValor.split(";")
        operador, valor, nombreOperador = __obtenerOperador(parametros[0])

        resultado = filtrador.consultarHorasEstacionesSuperioresAUnValor(int(valor), int(parametros[1]),
                                                                         operador=operador)
        auxiliar_ficheros.guardarFicheroFiltrado(texto=str(resultado),
                                                 tipo_filtrado="Horas" + nombreOperador + "PorcEstaciones",
                                                 parametrosConsulta=nombreOperador + str(valor) + "_" + parametros[1])

    if filtrado_PorcentajeHoraEstacionMasValor != Constantes.CARACTER_NULO_CMD:
        cadenas = filtrado_PorcentajeHoraEstacionMasValor.split("-")
        operador, valor, nombreOperador = __obtenerOperador(cadenas[0])
        estaciones = list(map(int, cadenas[1].split(";")))
        resultado = filtrador.consultarPorcentajeTiempoEstacionSuperiorAUnValor(int(valor), estaciones,
                                                                                operador=operador)

        auxiliar_ficheros.guardarFicheroFiltrado(texto=str(resultado),
                                                 tipo_filtrado="PorcentajeTiempo",
                                                 parametrosConsulta=nombreOperador + str(valor) + "-" + str(estaciones))


def simuladorEstadistico(comando: [str], args: None | Namespace = None):
    if args is None:
        rutaDeltas = comando[2]
        rutaSalida = comando[3]
        deltaActual = comando[4]
        diasAsimular = comando[5]
        ruleta = comando[6]
    else:
        rutaDeltas = args.rutaDeltas
        rutaSalida = args.rutaSalida
        deltaActual = args.deltaActual
        diasAsimular = args.diasAsimular
        ruleta = args.ruleta

    Constantes.RUTA_SALIDA = str(rutaSalida)
    Constantes.DELTA_TIME = int(deltaActual)
    rutaDeltas = auxiliar_ficheros.buscar_archivosEntrada(rutaDeltas, ['deltas'])

    matrizDeltas = pd.read_csv(rutaDeltas[0])
    simuladorDE = SimuladorDeltasEstadistico(matrizDeltas, int(deltaActual))
    #nuevoFicheroDeltas = simuladorDE.simularDatosEstadisticos_PeriodoTotal(int(diasAsimular))


    if int(ruleta) == 1:
        nuevoFicheroDeltas = simuladorDE.simularDatosEstadisticos_PeriodoTotal(int(diasAsimular))
    else:
        dias = list(range(0,int(diasAsimular)))
        nuevoFicheroDeltas = simuladorDE.simularDatosEstadisticos_Horas(dias)
    nombre = auxiliar_ficheros.formatoArchivo("deltasGeneradosEstadistica", "csv")

    nuevoFicheroDeltas.to_csv(join(rutaSalida,nombre), index=False)


def restarDirectorios(comando: [str], args: None | Namespace = None):
    if args is None:
        rutaDirectorio1 = comando[2]
        rutaDirectorio2 = comando[3]
        rutaDirectorioSalida = comando[4]
    else:
        rutaDirectorio1 = args.rutaDirectorio1
        rutaDirectorio2 = args.rutaDirectorio2
        rutaDirectorioSalida = args.rutaDirectorioSalida

    print("Restando las matrices del directorio " + str(rutaDirectorio1) + " menos las matrices del directorio " + str(rutaDirectorio2))

    directorios_resta = [Constantes.OCUPACION,
                         Constantes.OCUPACION_RELATIVA,
                         Constantes.PETICIONES_RESUELTAS_COGER_BICI,
                         Constantes.PETICIONES_RESUELTAS_SOLTAR_BICI,
                         Constantes.PETICIONES_RESUELTAS_FICTICIAS_COGER_BICI,
                         Constantes.PETICIONES_RESUELTAS_FICTICIAS_DEJAR_BICI,
                         Constantes.PETICIONES_NORESUELTAS_COGER_BICI,
                         Constantes.PETICIONES_NORESUELTAS_SOLTAR_BICI,
                         Constantes.PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI,
                         Constantes.PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI,
                         Constantes.KMS_COGER_BICI,
                         Constantes.KMS_DEJAR_BICI,
                         Constantes.KMS_FICTICIOS_COGER,
                         Constantes.KMS_FICTICIOS_DEJAR]

    restoFicheros = auxiliar_ficheros.buscar_archivosEntrada(rutaDirectorio1, ['Desplazamientos', 'coordenadas'])
    resumen1 = auxiliar_ficheros.buscar_archivosEntrada(rutaDirectorio1, ['ResumenEjecucion'])
    resumen2 = auxiliar_ficheros.buscar_archivosEntrada(rutaDirectorio2, ['ResumenEjecucion'])
    shutil.copy(restoFicheros[0], join(rutaDirectorioSalida, 'Desplazamientos.csv'))
    shutil.copy(restoFicheros[1], join(rutaDirectorioSalida, 'coordenadas.csv'))

    with open(resumen1[0], "r") as archivo:
        contenido = archivo.read()
    contenido_archivoResumen1 = contenido.split(",")

    with open(resumen2[0], "r") as archivo:
        contenido = archivo.read()
    contenido_archivoResumen2 = contenido.split(",")

    diferenciaResumenes = (np.array(list(map(float, contenido_archivoResumen1)))[2:] - np.array(
        list(map(float, contenido_archivoResumen2)))[2:]).tolist()
    resumenDiferencia = str((list(map(float, contenido_archivoResumen1)))[:2] + diferenciaResumenes)[1:-1]

    with open(join(rutaDirectorioSalida, 'DIFERENCIA_ResumenEjecucion.txt'), "w") as archivo:
        archivo.write(resumenDiferencia)

    capacidades1 = auxiliar_ficheros.buscar_archivosEntrada(rutaDirectorio1, ['capacidades'])
    capacidades2 = auxiliar_ficheros.buscar_archivosEntrada(rutaDirectorio2, ['capacidades'])

    if capacidades1 != [] and capacidades2 != []:
        nombre = auxiliar_ficheros.formatoArchivo("DIFERENCIA_CAPACIDADES", "csv")
        (pd.read_csv(capacidades1[0]) - pd.read_csv(capacidades2[0])).transpose().to_csv(
            join(rutaDirectorioSalida, nombre), index=False)

    for archivo in directorios_resta:
        fichero1 = auxiliar_ficheros.buscar_archivosEntrada(rutaDirectorio1, [archivo])
        fichero2 = auxiliar_ficheros.buscar_archivosEntrada(rutaDirectorio2, [archivo])
        matriz1 = pd.read_csv(fichero1[0])
        matriz2 = pd.read_csv(fichero2[0])
        archivoResultante = (Agrupador.sustraerMatrices(matriz1, matriz2))
        nombre = auxiliar_ficheros.formatoArchivo("DIFERENCIA " + archivo, "csv")
        archivoResultante.to_csv(join(rutaDirectorioSalida, nombre), index=False)

# Dado un texto, detecta que operador contiene.
def __obtenerOperador(string: str):
    if ">=" in string:
        return operator.ge, string.replace(">=", ""), "MAYIGUAL"

    if "<=" in string:
        return operator.le, string.replace("<=", ""), "MENIGUAL"

    if ">" in string:
        return operator.gt, string.replace(">", ""), "MAY"

    if "<" in string:
        return operator.lt, string.replace("<", ""), "MAY"

    # Operador por defecto en caso de que no se identifique la cadena o no se introduzca.
    return operator.ge, string.replace(">=", ""), "MAYIGUAL"
