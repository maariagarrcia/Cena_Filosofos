#  CENA DE LOS FILOSOFOS
<img width="491" alt="image" src="https://user-images.githubusercontent.com/93185415/235310183-ffe78aa5-ae5d-4a3a-afb0-19381fe8b435.png">

El problema de la cena de los filósofos es un problema clásico de concurrencia en informática que se utiliza para ilustrar los problemas que pueden surgir al coordinar varios procesos que compiten por recursos compartidos. En este caso, el problema implica a cinco filósofos sentados en una mesa redonda, cada uno con un tenedor a su izquierda y derecha y un plato de espaguetis frente a ellos. Los filósofos pasan su tiempo alternando entre comer y pensar, pero solo pueden hacer una actividad a la vez y necesitan dos tenedores para comer.

El problema surge cuando todos los filósofos intentan tomar el tenedor de su izquierda y el de su derecha simultáneamente, lo que lleva a un bloqueo mutuo en el que nadie puede comer. La solución a este problema implica el uso de hilos. 

Para evitar el bloqueo mutuo, hacemos uso de Locks, que son mecanismos de sincronización que permiten a los procesos o hilos acceder a recursos compartidos de manera exclusiva. 

En resumen, el algoritmo usado para la resolución de este problema es el siguiente: 
- Si consigue el tenedor izquierdo se bloquea y se mira si el tenedor derecho puede bloquearse.
- Si lo consigue empezará a comer ---> cuando acabe se liberaran los dos para que otro pueda usarlo
- Si no consigue el tenedor derecho liberará el tenedor izquierdo.

""

self.set_status(PhilosopherStatus.THINKING)
if not self.fork_left.usar(self):
    print(Fore.WHITE +
          "· Philosopher [" + str(self.id) + "]  No consigue Fork iquierdo ...")
    return True   # ================================>
Usar Fork derecha
self.set_status(PhilosopherStatus.THINKING)
if not self.fork_right.usar(self):
    self.fork_left.dejar_de_usar()
    print(Fore.WHITE + "· Philosopher [" + str(self.id) +
          "]  liberando Fork izquierdo (prevención Deadlock)...")
    return False  # ==================================>
Comer
self.set_status(self.status.EATING)
time.sleep(2)  # Tiempo para comer
Dejar de usar Fork derecha
self.fork_left.dejar_de_usar()
Usar Fork iquierda
self.fork_right.dejar_de_usar()
return True

""
