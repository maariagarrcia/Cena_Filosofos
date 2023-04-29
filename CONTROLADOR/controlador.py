from colorama import Fore


# SOLO CUANDO HAY UN CAMBIO DE ESTADO SE LLAMA A LA FUNCIÓN CALLBACK
def philosopher_callback(id, new_status):
    print(Fore.YELLOW, id, new_status)


def fork_callback(id, new_status):
    print(Fore.LIGHTGREEN_EX, id, new_status)