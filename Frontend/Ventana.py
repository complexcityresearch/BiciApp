
from abc import ABC
import customtkinter as tk

#Clase abstracta para la base de la creación de ventanas.
class Ventana(ABC):

    def __init__(self,titulo:str):
        self.ventana = tk.CTk()
        self.ventana.title(titulo)
        self.ventana.geometry("800x800")
        self.ventana.minsize(500, 500)

    #función para devolver el atributo ventana, ya que no puedo acceder desde super()
    def getVentanaAttribute(self):
        return self.ventana

    #función que ejecuta la ventana.
    def ejecutarVentana(self):
        self.ventana.mainloop()
