import folium
import pandas as pd


class Representar_desplazamientos:

    def __init__(self, coordenadas,matrizDesplazamientos:pd.DataFrame):
        self.coordenadas = coordenadas
        self.mapa = folium.Map([coordenadas[172][1], coordenadas[172][2]], zoom_start=13)
        self.matrizDesplazamientos = matrizDesplazamientos

        self.colorCoger = "blue"
        self.colorSoltar = "black"

    # Función que representa un mapa con círculos que representan las estaciones.
    def __representacionBasica(self):
        for i in range(len(self.coordenadas)):
            self.__dibujarCirculo(self.coordenadas[i][1], self.coordenadas[i][2], 50, "red",
                                  "Station " + str(i))
        self.mapa.save("mapa.html")

    # Función auxiliar que representa un circulo dado sus coordenadas, el radio y el color deseado.
    def __dibujarCirculo(self, lat, long, radio, color, label=""):
        folium.Circle(
            radius=radio,
            location=[lat, long],
            color=color,
            fill=True
        ).add_child(folium.Popup(label)).add_to(self.mapa)

    def representar_instante(self,instante):
        self.__representacionBasica()
        np_desplazamientos = self.matrizDesplazamientos.to_numpy()
        desplazamientos_filtrados=np_desplazamientos[np_desplazamientos[:, 3] == instante]

        for i in range(desplazamientos_filtrados.shape[0]):
            radio, color = self.__calcularColorTamanoCirculo(desplazamientos_filtrados[i, 2],
                                                             desplazamientos_filtrados[i, 3])

            #En el caso de que la petición se realice a ella misma, entonces lo representaremos con un circulo
            #El tamaño del circulo dependerá del número de peticiones.
            if desplazamientos_filtrados[i,0] == desplazamientos_filtrados[i,1]:
                estacion = int(desplazamientos_filtrados[i,0])
                self.__dibujarCirculo(self.coordenadas[estacion,1], self.coordenadas[estacion,2], float(radio), color,"Estacion " + str(estacion))
            else:
                index_estacionInicio = int(desplazamientos_filtrados[i, 0])
                index_estacionFinal = int(desplazamientos_filtrados[i, 1])

                coordenadas_estacionInicio = self.coordenadas[index_estacionInicio,[1,2]]
                coordenadas_estacionFinal = self.coordenadas[index_estacionFinal, [1, 2]]


                self.__pintarLinea(coordenadas_estacionInicio,coordenadas_estacionFinal,color,radio/2)

        self.mapa.save("MapaDesplazamientos.html")


    def __pintarLinea(self,coordenadaInicio:tuple,coordenadaFinal:tuple,color,tammano):

        folium.PolyLine([coordenadaInicio,coordenadaFinal],
                        color=color,
                        weight = tammano,
                        no_clip=True
                        ).add_to(self.mapa)


    def __calcularColorTamanoCirculo(self,tipoPeticion,cantidad):
        radio = cantidad * 2 + 50
        color = None
        if tipoPeticion == 1:
            color = self.colorSoltar
        else:
            color = self.colorCoger
        return radio,color


