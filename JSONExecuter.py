# This class represents the backend interface for JSON files.
## The structure of this JSON file is the following:

#{
#  "input_directory": "C:\\ruta\\de\\entrada",
#  "output_directory": "C:\\ruta\\de\\salida",
#  "delta_time": 0,
#   "stress" : 0.5,
#   "stress_stations" : "0;1;2.... / All"
# "stress_type": "0",
#  "cost_of_walking": 0,
#  "apply_to_stations": ""
#   "days_extracted":"0;1;2;3..."
#}

import json

import pandas as pd
from os.path import join

import wx
from Backend import Constantes
from Backend.Auxiliares import Extractor, auxiliar_ficheros, auxiliaresCalculos
from Backend.GuardarCargarDatos import GuardarCargarMatrices
from Backend.Manipuladores import Agrupador
from Backend.Manipuladores.Filtrador import Filtrador
from Backend.Representacion.ManejadorMapas.manejar_Voronoi import manejar_Voronoi
from Backend.Representacion.ManejadorMapas.manejar_densidad import Manejar_Densidad
from Backend.Representacion.ManejadorMapas.manejar_mapaCirculos import manejar_mapaCirculos
from Backend.estadisticasOcupacionHorarias import estadisticasOcupacionHorarias
from bike_simulator5 import bike_simulator5
from ux_html2 import MyFrame

def simulateScenario(json_string:str):
    
    configuration = (json_string)

    ## We should split the must and not-must configurations.

    try:
        input_directory = configuration["input_directory"]
        output_directory = configuration["output_directory"]
        delta_time = int(configuration["delta_time"])
        stress = float(configuration["stress"])
        stress_stations = configuration["stress_station"]
        stress_type = int(configuration["stress_type"])
        cost_of_walking = int(configuration["cost_of_walking"])
        days_extracted = configuration["days_extracted"]
    except:
        print("Invalid format")

    
    if stress_stations != "All":
        stress_stations = list(map(int,stress_stations.split(';')))

    Constantes.DELTA_TIME = delta_time
    Constantes.COSTE_ANDAR = cost_of_walking
    Constantes.PORCENTAJE_ESTRES = stress
    Constantes.RUTA_SALIDA = output_directory

        ##We should change all this logic with more modern options / more robust.
    ficheros,ficheros_distancia = GuardarCargarMatrices.cargarDatosParaSimular(input_directory)
    archivoCapacidad = auxiliar_ficheros.buscar_archivosEntrada(input_directory, ["capacidades"])[0]
    pd.read_csv(archivoCapacidad).to_csv("capacidades.csv",index=False) ## change this aswell.

    ##Extract days.
    if days_extracted != "":  # optional
        dias = list(map(int, days_extracted.split(";")))
        path_fichero = join(output_directory, auxiliar_ficheros.formatoArchivo("Extraccion_" + str(dias), "csv"))
        Extractor.extraerDias(ficheros[0], delta_time, dias, path_fichero, mantenerPrimeraFila=True)
        ficheros[0] = path_fichero

    ##CHECK IF EVEYTHING HERE IS CORRECT AND ADJUST AUXIAR FUNCTION WITH FIXED TYPO.s
    if stress > 0:

        ficheroDelta_salidaStress = join(output_directory, auxiliar_ficheros.formatoArchivo("Dstress", "csv"))
        Extractor.extraerStressAplicado(ficheros[0], ficheroDelta_salidaStress, stress, tipoStress=int(stress_type),listaEstaciones=stress_stations)
        ficheroTendencias_salidaStress = join(output_directory, auxiliar_ficheros.formatoArchivo("Tendencias_stress", "csv"))
        Extractor.extraerStressAplicado(ficheros[5], ficheroTendencias_salidaStress, stress, tipoStress=int(stress_type),listaEstaciones=stress_stations)
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
    archivoCapacidad = auxiliar_ficheros.buscar_archivosEntrada(input_directory, ["capacidades"])[0]
    pd.read_csv(archivoCapacidad).to_csv(join(output_directory, "capacidades.csv"), index=False)

##Common load matrix method.
#
def __loadInputData__(json_file) -> pd.DataFrame:
    try:
        input_directory = json_file["input_directory"]
        matrix_list_str = json_file["matrix_list"]
        delta_origin = int(json_file["delta_origin"])
        delta_obj = int(json_file["delta_objetive"])
        delta_transformation_type = json_file["delta_transformation_type"]
    except:
        print("Error loading basic data from matrix")
    matrix_data,resumentxt = GuardarCargarMatrices.cargarSimulacionesParaAnalisis(input_directory)
    matrix_list = list(map(int, matrix_list_str.split(";")))
    if len(matrix_list) < 1:
        raise "Exception, no matrix provided"
    #Acumulate the matrixs:

    ##TODO: if matrix_custom is provided, we should introduce in the position 0 of the array matrix_list.
    if Constantes.MATRIZ_CUSTOM == None:
        wantedMatrix = matrix_data[Constantes.LISTA_MATRICES[matrix_list[0]]].matrix
        inicio = 1
    else:
        wantedMatrix = Constantes.MATRIZ_CUSTOM
        inicio = 0
    for i in range(inicio,len(matrix_list)):
        wantedMatrix = Agrupador.agruparMatrices(wantedMatrix, matrix_data[Constantes.LISTA_MATRICES[matrix_list[i]]].matrix)
    
    ##Delta conversion:

    if delta_transformation_type == "mean":
        wantedMatrix = Agrupador.colapsarDeltasMedia(wantedMatrix, deltaActual=delta_origin, deltaDeseado=delta_obj)
    else:
        wantedMatrix = Agrupador.colapsarDeltasAcumulacion(wantedMatrix, deltaActual=delta_origin, deltaDeseado=delta_obj)

    wantedMatrix = auxiliaresCalculos.rellenarFilasMatrizDeseada(wantedMatrix,
                                                                          matrix_data[Constantes.OCUPACION].matrix.shape[0] - 1)
    return wantedMatrix
    

##TODO: Add Custom matrix.
#{ Fixed delta to 60 (one hour)
#  "input_directory": "C:\\ruta\\de\\entrada",
#  "output_directory": "C:\\ruta\\de\\salida"
#  "matrix_list": "0;1;2;3..."
#  "graph_type" : "Accumulated graph of a station"
#  "graph_param" : Depending of the graph.
#   "delta_hour_transform" : "mean" or "accumulate"
#}
def stadistics(json_string):
    configuration = json_string
    try:
        wantedMatrix = __loadInputData__(json_string)
        output_directory = configuration["output_directory"] #Is this necesary?.
        graph_type = configuration["graph_type"]
        graph_param : str = configuration["graph_param"]

    except:
        print("Error in analyzer")

    ##Delta conversion: Always to 60 (1 hour ticks)


    days_wantedMatrix = int(wantedMatrix.shape[0] / 24)

    stadistics_class = estadisticasOcupacionHorarias(wantedMatrix, 60)

    ## I miss switch statements :(
    
    if graph_type == "Accumulated graph of a station":
        #param= 0-All or 0-1;2;3;4...
        params = graph_param.split('-')
        if (params[0] != 'All'):
            days = list(map(int, params[1].split(';')))
        else:
            days = list(range(days_wantedMatrix))
        stadistics_class.HistogramaAcumulacion(int(params[0]), days)

    if graph_type == "Average graph of a station":
        #param= 0-All or 0-1;2;3;4...
        params = graph_param.split('-')
        if (params[1] != 'All'):
            days = list(map(int, params[1].split(';')))
        else:
            days = list(range(days_wantedMatrix))
        stadistics_class.HistogramaPorEstacion(estacion=int(params[0]),dias=days)

    if graph_type == "Bar graph Average of all stations":
        #param= All-M / All-A / 0;1;2...-A / 0;1;2-A-Frec
        params = graph_param.split('-')
        if (params[0] != 'All'):
            days = list(map(int, params[1].split(';')))
        else:
            days = list(range(days_wantedMatrix))
        
        stadistics_class.HistogramaOcupacionMedia(days, frecuencia=graph_param.__contains__("Frec"),
                                                     media=graph_param.__contains__("M"))
    if graph_type == "Graph comparing stations":
        ##TODO: Code this
        None
    if graph_type == "Graph comparing matrices":
        ##TODO: Code this
        None


##In construction:


##TODO: We should implement the sumary of simulator execution as JSON aswell.
#{ Fixed delta to 60 (one hour)
#  "input_directory": "C:\\ruta\\de\\entrada",
#  "output_directory": "C:\\ruta\\de\\salida"
#   "station_list":"0;1;2..." or "All"
#   "map_type" : "Density Map" / "Voronoi Map" / "Circles Map"
#  TODO: Add colors for positive and negative.
#}
def maps(configuration):

    try:
        wantedMatrix = __loadInputData__(configuration)
        station_list = configuration["station_list"]
        map_type = configuration["map_type"]
    except:
        print("Error in map handling")

    if (station_list != 'All'):
        station_list = list(map(int, station_list.split(';')))
    else:
        station_list = list(range(wantedMatrix.shape[1]-1))
    

    handler = None
    if map_type == "Density Map":
        handler = Manejar_Densidad(wantedMatrix, Constantes.COORDENADAS,listaEstaciones=station_list)
    if map_type == "Voronoi Map":
        handler = manejar_Voronoi(wantedMatrix, Constantes.COORDENADAS)
    if map_type == "Circles Map":
        handler = manejar_mapaCirculos(wantedMatrix, Constantes.COORDENADAS, listaEstaciones=station_list)

    ######TODO: Rethink this to aislate functionality SOLID principes.
    app = wx.App()
    frame = MyFrame(None,handler)
    app.MainLoop()


##TESTS:

with open("test-maps.json", "r", encoding="utf-8") as file:
    json_test = json.load(file)

maps(json_test)
