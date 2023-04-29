import helpers
from menu import *
from MODELO.filosofos import *
from VISTA.myviewer import *



def vista():
    print("· Vista")
    main_viewer()

#
#   I N I C I O    P R O G R A M A
#
helpers.clear()  # Limpia la terminal

mi_menu = Menu("MODELO VISTA CONTROLADOR ")
mi_menu.addOption("Representación gráfica de la cena de los filosofos y programa por consola",   vista)

                  
