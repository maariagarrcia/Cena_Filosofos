from colorama import Fore
import threading
import time
import random
from VISTA.myviewer import *
import enum
from CONTROLADOR.controlador import *


# CREAMOS DOS CLASES: Tenedor y Filosofo

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

class PhilosopherStatus(enum.Enum):
    RESTING = 0     # After eating do nothing for a while
    EATING = 1      # Time to consume de meals
    THINKING = 4    # Waiting for fork


class ForkStatus(enum.Enum):
    FREE = 0
    BLOCKED = 1


class Fork():
    def __init__(self, id: int, status_changed_callback):
        self.id: int = id
        self.Philosopher = None
        self.lock: threading.Lock = threading.Lock()
        self.status = ForkStatus.FREE
        self.status_changed_callback = status_changed_callback

    def set_status(self, new_status):
        self.status = new_status

        if self.status_changed_callback != None:
            self.status_changed_callback(self.id, new_status)

    def usar(self, Philosopher, max_reintentos: int = 5) -> bool:
        intento = 1
        while not self.lock.acquire(blocking=False):
            if (intento > max_reintentos):
                return False  # No se ha conseguido usar el Fork

            # No ha conseguido el bloqueo => Nos ponemos a pensar
            # print(colorama.Fore.RED +
            #       "· Philosopher [" + Philosopher.id + "]  Pensando ... ", intento)
            time.sleep(0.5)  # Tiempo para pensar
            intento += 1

        self.set_status(ForkStatus.BLOCKED)
        self.Philosopher = Philosopher

        return True

    def dejar_de_usar(self):
        self.Philosopher = None
        self.lock.release()
        self.set_status(ForkStatus.FREE)


class Philosopher(threading.Thread):
    def __init__(self, id: int = None, fork_left: Fork = None, fork_right: Fork = None, status_changed_callback=None):

        super(Philosopher, self).__init__()

        self.id: int = id
        self.fork_left: Fork = fork_left
        self.fork_right: Fork = fork_right
        self.status = PhilosopherStatus.THINKING
        self.status_changed_callback = status_changed_callback

    def set_status(self, new_status):
        self.status = new_status

        if self.status_changed_callback != None:
            self.status_changed_callback(self.id, new_status)

    def comer(self):
        # Usar Fork izquierda
        # print("· Philosopher [" + self.id + "]  usar Fork iquierdo")
        self.set_status(PhilosopherStatus.THINKING)
        if not self.fork_left.usar(self):
            print(Fore.WHITE +
                  "· Philosopher [" + str(self.id) + "]  No consigue Fork iquierdo ...")
            return True   # ================================>

        # Usar Fork derecha
        # print("· Philosopher [" + self.id + "]  usar Fork derecho")
        self.set_status(PhilosopherStatus.THINKING)
        if not self.fork_right.usar(self):
            self.fork_left.dejar_de_usar()
            print(Fore.WHITE + "· Philosopher [" + str(self.id) +
                  "]  liberando Fork izquierdo (prevención Deadlock)...")
            return False  # ==================================>

        # Comer
        self.set_status(self.status.EATING)
        time.sleep(2)  # Tiempo para comer

        # Dejar de usar Fork derecha
        self.fork_left.dejar_de_usar()

        # Usar Fork iquierda
        self.fork_right.dejar_de_usar()

        return True

    def run(self) -> None:
        while True:
            self.comer()

            self.set_status(self.status.RESTING)
            time.sleep(random.random()*10)  # Descanso entre comidas


class Simulator():
    def __init__(self,
                 philosopher_status_changed_callback,
                 fork_status_changed_callback):

        # Crear cinco Forks
        self.Forks = [None]*5
        for i in range(0, 5):
            self.Forks[i] = Fork(
                i, fork_status_changed_callback)

        # Crear cinco Philosophers
        self.Philosophers = [None]*5
        for i in range(0, 5):
            self.Philosophers[i] = Philosopher(
                i, self.Forks[i], self.Forks[i-1], philosopher_status_changed_callback)

    def run(self):
        # Arrancar los 5 filosoos para que empiecen a comer
        for i in range(0, 5):
            self.Philosophers[i].start()


def main_modelo():
    sim = Simulator(philosopher_callback, fork_callback)
    sim.run()


if __name__ == '__main__':
    main_modelo()

