from abc import ABC, abstractmethod

from selenium import webdriver


#Clase interfaz
class Interfaz_Representacion(ABC):

    @abstractmethod
    def cargarMapaInstante(self,instante,listaEstaciones=None,accion=None,tipo=None):
        pass

    @abstractmethod
    def getFichero(self):
        pass
    @abstractmethod
    def getInstanciasMax(self):
        pass

    def realizarFoto(self,rutaSalida):
        DRIVER = 'cromedriver'
        driver = webdriver.Chrome(DRIVER)
        driver.set_window_size(3000, 1000)  # choose a resolution
        driver.get("file://"+self.getFichero())
        driver.refresh()
        screenshot = driver.save_screenshot(rutaSalida)
