# Clase que contiene los poligonos de las regiones de voronoi.

class Poligonos:
    def __init__(self, indicePunto, poligono: list):
        self.color = None
        self.indicePunto = indicePunto
        self.poligono = poligono
        self.ocupacion = None
