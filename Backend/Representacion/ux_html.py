
import sys


from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


from Backend.Representacion.Interfaz_Representacion import Interfaz_Representacion


# Clase encargada de hacer una interfaz basada en un archivo html.
class InterfazHTML():

    def __init__(self, interfaz_representacion: Interfaz_Representacion):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()

        self.instanteActual = 0
        self.textBox = QtWidgets.QSpinBox()
        self.textBox.setMaximum(2 ** 31 - 1)
        self.ficheroMapa = interfaz_representacion.getFichero()
        self.representacion = interfaz_representacion
        #self.interfazWeb()


    def botonPulsado(self):
        self.instanteActual = int(self.textBox.text())
        self.representacion.cargarMapaInstante(self.instanteActual)
        self.mainWindow.load(QtCore.QUrl().fromLocalFile(self.ficheroMapa))

    def navegacion(self, opcion):

        if opcion == -1:
            self.instanteActual -= 1


        else:
            if opcion == 1:
                self.instanteActual += 1
        self.textBox.setValue(self.instanteActual)
        self.botonPulsado()

    def interfazWeb(self):
        view = QtWebEngineWidgets.QWebEngineView()
        view.load(QtCore.QUrl().fromLocalFile(self.ficheroMapa))
        view.resize(800, 800)

        view.show()

        main_window = QtWidgets.QMainWindow()
        main_window.resize(800, 800)
        main_window.setCentralWidget(view)
        main_window.show()

        control_frame = QtWidgets.QFrame()
        control_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        control_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        control_layout = QtWidgets.QHBoxLayout()
        control_frame.setLayout(control_layout)

        # ----------------------#
        instancias_max = self.representacion.getInstanciasMax()

        label = QtWidgets.QLabel("/" + instancias_max)

        self.textBox.setValue(self.instanteActual)
        button = QtWidgets.QPushButton("Reload Map")
        boton_navegacion_atras = QtWidgets.QPushButton("<")
        boton_navegacion_delante = QtWidgets.QPushButton(">")
        boton_cerrar = QtWidgets.QPushButton("Delete Objects")

        boton_navegacion_atras.clicked.connect(lambda: self.navegacion(-1))
        button.clicked.connect(lambda: self.botonPulsado())
        boton_navegacion_delante.clicked.connect(lambda: self.navegacion(1))
        boton_cerrar.clicked.connect(self.cerrarApp)
        # Agregar los widgets al frame

        control_layout.addWidget(self.textBox)
        control_layout.addWidget(label)
        control_layout.addWidget(button)
        control_layout.addWidget(boton_navegacion_atras)
        control_layout.addWidget(boton_navegacion_delante)
        control_layout.addWidget(boton_cerrar)

        # Agregar el frame al dock widget
        dock = QtWidgets.QDockWidget("Controls", main_window)
        dock.setWidget(control_frame)
        main_window.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)

        self.mainWindow = view
        self.representacion.cargarMapaInstante(self.instanteActual)
        self.mainWindow.load(QtCore.QUrl().fromLocalFile(self.ficheroMapa))
        self.app.exec_()

    def cerrarApp(self):

        self.main_window.hide()