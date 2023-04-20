from colorama import Fore
import threading
import time
import random

# ORIENTADO A OBJETOS PERO DPS SEPARARLO EN MODELO VISTA CONTROLADOR COOMO SIEMPRE


class Tenedor():
    def __init__(self, id: str):
        self.id = id
        self.filosofo = None
        self.lock: threading.Lock = threading.Lock()

    def usar(self):
        pass

    def dejar_de_usar(self):
        pass


class Filosofo(threading.Thread):
    def __init__(self, id: str, tenedor_izq: Tenedor, tenedor_der: Tenedor):
        super(Filosofo, self).__init__()

        self.id = id
        self.tenedor_izq: Tenedor = tenedor_izq
        self.tenedor_der: Tenedor = tenedor_der

    def comer(self):
        pass

    def run(self):
        while True:
            self.comer()
            time.sleep(random.random())



def main():
    # crer los 5 tenedores
    tenedores=[None]*5
    for i in range(0,5):
        tenedores[i]=Tenedor(str(i))

    # crear los 5 filosofos
    filosofos=[None]*5
    for i in range(0,5):
        filosofos[i]=Filosofo(str(i),tenedores[i],tenedores[i+1])

    # Arrancar los 5 filosoos para que empiecen a comer
    for i in range(0,5):
        filosofos[i].start()


if __name__ == '__main__':
    main()
