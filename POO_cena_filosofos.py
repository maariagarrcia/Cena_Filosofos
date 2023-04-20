from colorama import Fore
import threading
import time
import random

# ORIENTADO A OBJETOS PERO DPS SEPARARLO EN MODELO VISTA CONTROLADOR COOMO SIEMPRE

# CREAMOS DOS CLASE: Tenedor y Filosofo

# FILOSOFO
# ----------
# CADA FILOSOFO ES UN HILO: IDENTIFICADOR(NUMERO DE CADA FILOSOFO), TENEDOR IZQUIERDO Y TENEDOR DERECHO.
# CADA FILOSOFO TIENE QUE COMER
# COMER ---->  PRIMERO COGEMOS EL TENEDOR IZQ SI DPS NO CONSEGUIMOS EL DER DESBLOQUEAMOS EL IZQ
# CUANDO EL FILOSOFO CONSIGUE LOS DOS TENEDORES COME Y LOS DEJA LIBRES PARA QUE OTRO LOS PUEDA USAR
# TENER EN CUENTA QUE HAY Q PONER UN TIEMPO DE SIMULACION PARA COMER Y DPS DE COMER


# TENEDOR
# ----------
# CADA TENEDOR TIENE UN IDENTIFICADOR Y UNA VBLE FILÓSOFO PARA SABER QUIEN LO ESTA USANDO
# DOS METODOS: USAR Y DEJAR DE USAR
# USAR: CUANDO USAMOS UN TENENDOR LO BLOQUEAMOS PARA QUE OTRO NO PUEDA USARLO
# SI NO CONSIGUE BLOQUEARLO PQ LO DEBE D TENER OTRO ---> PENSAR (TIEMPO DE SIMULACION)
# Los max intentos son 5 para evitar un Deadlock

# DEJAR DE USAR: CUANDO EL FILOSOFO DEJA DE COMER LIBERA EL TENEDOR PARA QUE OTRO LO PUEDA USAR --->
# NINGUN FILOOSOFO LO ESTA USANDO ---> FILÓSOFO = NONE, DESBLOQUEAMOS EL TENEDOR


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

        self.id:str = id
        self.tenedor_izq: Tenedor = tenedor_izq
        self.tenedor_der: Tenedor = tenedor_der

    def comer(self):
        if not self.tenedor_izq.usar(self):
            print(
                Fore.WHITE + "· Filosofo: [" + self.id + "]  No consigue tenedor iquierdo ...")
            return True  # ===============================>

        if not self.tenedor_der.usar(self):
            # no se ha conseguido usar el tenedor
            # dejar de usar tenedor izq
            self.tenedor_izq.dejar_de_usar()

            print(
                "· Filosofo: [" + self.id + "]  liberando tenedor izquierdo (prevención Deadlock)...")

            return False  # ===============================>

        # conseguimos comer
        print(Fore.LIGHTGREEN_EX + "· Filosofo: [" + self.id + "]  C O M E R")
        time.sleep(2)  # tiempo para comer
        print(Fore.LIGHTGREEN_EX +
              "· Filosofo: [" + self.id + "]  D E J A R    D E   C O M E R")

        self.tenedor_izq.dejar_de_usar()
        self.tenedor_der.dejar_de_usar()

        return True

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
