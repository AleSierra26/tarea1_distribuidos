# Solo puedes importar las siguientes librerías y ninguna otra
from xmlrpc.server import SimpleXMLRPCServer
from sys import argv
import os, json, math, threading, time


class Servel:
    def __init__(self, archivo_configuacion: str, archivo_log: str) -> None:
        pass

    def recibir_votos(self, sucursal: str, votos: dict) -> None:
        pass

    def ganador(self, id_votacion: str) -> None:
        pass

    def log(self, id_votacion: str, opcion: str) -> None:
        pass

    def new_subscriber(self, subscriptor: str) -> None:
        pass

    def subscribe(self, subscriptor: str, sucursal: str, evento: str) -> None:
        pass

    def unsubscribe(self, subscriptor: str, sucursal: str, evento: str) -> None:
        pass

    # Puedes agregar métodos adicionales si lo consideras necesario


if __name__ == "__main__":
    if len(argv) != 4 or not argv[1].isdigit():
        texto = """
        El comando debe ser ejecutado con el siguiente formato:
        <COMANDO_PYTHON> main.py <PUERTO> <CONFIGURACION> <LOGS>

        Donde:
         - <COMANDO_PYTHON> es el comando para ejecutar Python en tu sistema operativo.
         - <PUERTO> es el puerto en el que se ejecutará el servidor RPC.
         - <CONFIGURACION> es el nombre de un archivo JSON con la configuración de la votación.
         - <LOGS> es el nombre de un archivo TXT donde se guardarán los logs de la votación.
        """
        print(texto)
        exit(1)

    PUERTO = int(argv[1])
    CONFIGURACION = argv[2]
    LOGS = argv[3]

    # DEBES dejar IP_TAREA como "127.0.0.1"
    # porque como "localhost" es un poco más lenta la comunicación
    # para los que tienen sistema Windows
    # Link de interés: https://superuser.com/a/595324
    IP_TAREA = "127.0.0.1"

    servel_votaciones = Servel(CONFIGURACION, LOGS)
    # Completar con lo que falta
