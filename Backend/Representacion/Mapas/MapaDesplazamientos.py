
from os.path import join

import pandas as pd
import openrouteservice
import folium


from Backend import Constantes
from Backend.Auxiliares import auxiliar_ficheros


class MapaDesplazamientos:

    def __init__(self, coordenadas, matrizDesplazamientos: pd.DataFrame):
        self.coordenadas = coordenadas
        self.matrizDesplazamientos = matrizDesplazamientos

    def representarInstante(self,instante,accion=1,tipo=True):
        matrizDesp = self.filtrarMatriz_Desplazamientos(instante,accion,tipo)
        if not matrizDesp.empty:

            tipo_accion = None
            if accion == 1:
                tipo_accion = 'cycling-regular'
            else:
                tipo_accion = 'foot-walking'

            listaCoordenadas = []
            listaID = []
            listaPeso=[]
            for i in range(matrizDesp.shape[0]):

                estacionOrigen = self.obtenerCoordenadasEstacion(matrizDesp.iloc[i,0])
                estacionDestino = self.obtenerCoordenadasEstacion(matrizDesp.iloc[i,1])
                listaID.append((matrizDesp.iloc[i,0],matrizDesp.iloc[i,1]))
                listaCoordenadas.append([estacionOrigen,estacionDestino])
                listaPeso.append(matrizDesp.iloc[i,4])

            mapa= self.generar_mapa(listaCoordenadas,tipo_accion,listaID,listaPeso=listaPeso)
        else:
            mapa = folium.Map(location=[Constantes.COORDENADAS[round(Constantes.COORDENADAS.shape[0]/2),1],Constantes.COORDENADAS[round(Constantes.COORDENADAS.shape[0]/2),2]] , zoom_start=12)

        if Constantes.RUTA_SALIDA != "":
            nombre = auxiliar_ficheros.formatoArchivo("MapaDesplazamientos_instante" + str(instante), "html")
            mapa.save(join(Constantes.RUTA_SALIDA, nombre))
        else:
            mapa.save("MapaDesplazamientos.html")

    def generar_mapa(self,lista_coordenadas, modo_conduccion,listaId,API_KEY='5b3ce3597851110001cf62484732354d82964f0491b986aeb994386d',listaPeso = []):
        # API_KEY = '5b3ce3597851110001cf62484732354d82964f0491b986aeb994386d'  # Introducir la KEY generada
        client = openrouteservice.Client(key=API_KEY)

        lat = lista_coordenadas[0][0][1]
        lon = lista_coordenadas[0][0][0]

        m = folium.Map(location=[lat, lon], zoom_start=12)

        i = 1
        index = 0

        color_linea = 'red'
        if modo_conduccion == 'foot-walking':
            color_linea= 'blue'


        for coord in lista_coordenadas:

            ruta = client.directions(coordinates=coord, profile=modo_conduccion, format='geojson')

            camino = ruta['features'][0]['geometry']['coordinates']

            coordinates = [[coord_camino[1], coord_camino[0]] for coord_camino in camino]

            lineWeight = 5

            if listaPeso != []:
                lineWeight = round(5 * listaPeso[index])




            route = folium.PolyLine(locations=coordinates, weight=lineWeight, color=color_linea, name=f'Rute {i}')

            # Se añade la ruta a un grupo, lo que permite poder seleccionarla en el desplegable (arriba derecha)
            route_group = folium.FeatureGroup(name=f'Rute {i}')
            route_group.add_child(route)

            # Se incluye el grupo en el mapa
            m.add_child(route_group)

            # Se añaden los marcadores
            folium.Marker(location=coordinates[0], popup=f'Start of Route {i} ' + 'Station ' + str(listaId[index][0])).add_to(m)
            folium.Marker(location=coordinates[-1],icon=folium.Icon(color='red'), popup=f'End of route {i} ' + 'Station ' + str(listaId[index][1])).add_to(m)

            i += 1
            index += 1

        folium.LayerControl().add_to(m)
        return m
        #m.show_in_browser()

    #Función que filtra la matriz desplazamientos para obtener una submatriz constituida del instante seleccionado y del tipo de petición
    #y de acción
    def filtrarMatriz_Desplazamientos(self,instante,accion,tipo):
        #self.matrizDesplazamientos[(self.matrizDesplazamientos['Utemporal'] > 0) & (self.matrizDesplazamientos['Utemporal'] < 10)]
        filtrado_tiempo = self.matrizDesplazamientos[self.matrizDesplazamientos['Utemporal'] == instante]
        filtrado_accion = filtrado_tiempo[filtrado_tiempo['tipo de peticion'] == accion]
        filtrado_tipo = filtrado_accion[filtrado_accion['RealFicticio'] == tipo]
        filtrar_desp = filtrado_tipo[filtrado_tipo['Estacion origen'] != filtrado_tipo['Estacion final']]

        return filtrar_desp

    def obtenerCoordenadasEstacion(self,estacionID):
        return (self.coordenadas[estacionID][2],self.coordenadas[estacionID][1])