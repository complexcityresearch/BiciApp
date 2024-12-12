
PETICION_SOLICITAR_BICI = "-1"
PETICION_DEJAR_BICI = "1"

KMS_DEJAR_BICI = 'Kilometros_Dejar'
KMS_COGER_BICI = 'Kilometros_Coger'
PETICIONES_NORESUELTAS_COGER_BICI = 'Peticiones_NoResueltas_Coger'
PETICIONES_NORESUELTAS_SOLTAR_BICI = 'Peticiones_NoResueltas_Dejar'

PETICIONES_RESUELTAS_COGER_BICI = 'Peticiones_Resueltas_Coger'
PETICIONES_RESUELTAS_SOLTAR_BICI = 'Peticiones_Resueltas_Dejar'


OCUPACION = 'Ocupacion_Original'
OCUPACION_RELATIVA = 'Ocupacion_Relativa'


DESPLAZAMIENTOS = 'Desplazamientos'

KMS_FICTICIOS_COGER = 'Kilometros_Ficticios_Coger'
KMS_FICTICIOS_DEJAR = 'Kilometros_Ficticios_Dejar'

PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI = 'Peticiones_NoResueltas_Ficticia_Coger'
PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI = 'Peticiones_NoResueltas_Ficticia_Dejar'

PETICIONES_RESUELTAS_FICTICIAS_COGER_BICI = 'Peticiones_Resueltas_Ficticias_Coger'
PETICIONES_RESUELTAS_FICTICIAS_DEJAR_BICI = 'Peticiones_Resueltas_Ficticias_Dejar'


LISTA_MATRICES = [OCUPACION,OCUPACION_RELATIVA,KMS_COGER_BICI,KMS_DEJAR_BICI,PETICIONES_RESUELTAS_COGER_BICI,PETICIONES_RESUELTAS_SOLTAR_BICI,
                  PETICIONES_NORESUELTAS_COGER_BICI,PETICIONES_NORESUELTAS_SOLTAR_BICI,KMS_FICTICIOS_COGER,KMS_FICTICIOS_DEJAR,
                  PETICIONES_RESUELTAS_FICTICIAS_COGER_BICI,PETICIONES_RESUELTAS_FICTICIAS_DEJAR_BICI,
                  PETICIONES_NORESUELTAS_FICTICIAS_COGER_BICI,PETICIONES_NORESUELTAS_FICTICIAS_DEJAR_BICI,DESPLAZAMIENTOS]

DELTA_TIME = 15

MATRIZDESPLAZAMIENTOS_PETICIONES = 4
MATRIZDESPLAZAMIENTOS_UTEMPORAL = 3

CAPACIDAD_MAXIMA_INICIAL = 5068

COORDENADAS = []

COSTE_ANDAR = 1

PORCENTAJE_ESTRES = 0.0

ZOOM_MAPAS_PLOT = 12
ZOOM_MAPAS_PLOT_VIDEO = 12.5
ZOOM_MAPAS_FOLIUM = 14


ACCIONES = ['ComandoPrevio','CargarAnterior','CargarDeltas','CargarCoordenadas','CargarIndicesCercanos','CargarKmsCercanos',
            'CargarCapacidades','CargarTendencia','Deltas','AgruparMatrices','MatrizSeleccionada','DeltaDeseadoMedia','DeltaDeseadoAcumulado','HistogramaMedioEstacion',
            'HistogramaAcumuladoEstacion','HistogramaDia','CompararEstaciones','MapaDensidad','MapaVoronoi','EstacionesSuperioresValor',
            'EstacionesSuperioresValorEnDias','HorasSuperioresValor','TiempoEstacionMasDeValor']

RUTA_SALIDA = ""

CARACTER_NULO_CMD = "_"

MATRIZ_CUSTOM = None

DiastanciasAndarBicicleta = False